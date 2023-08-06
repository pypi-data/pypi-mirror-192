import asyncio
import re
from dataclasses import dataclass

from adb_shell.adb_device_async import AdbDeviceTcpAsync
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen

from googletv.constants import (
    ADB_MAX_RETRIES,
    ADB_RETRY_INTERVAL,
    APPS,
    CMD_DUMPSYS_ACTIVITY,
    CMD_DUMPSYS_DISPLAY,
    CMD_DUMPSYS_ERROR,
    CMD_DUMPSYS_MEDIA_SESSION,
    CMD_DUMPSYS_POWER,
    REGEX_ACTIVITY_RESUMED,
    REGEX_ACTIVITY,
    REGEX_ASLEEP,
    REGEX_AWAKE,
    REGEX_PLAYBACK_STATE,
    REGEX_SCREEN_OFF,
    REGEX_SCREEN_ON,
    REGEX_SESSION,
)
from googletv.exception import GoogleTvException
from googletv.search import search_nested


class AdbKey:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

        self._public_key: str | None = None
        self._private_key: str | None = None

    @property
    def public_key(self) -> str:
        if self._public_key is None:
            with open(f"{self._file_path}.pub", "r") as f:
                self._public_key = f.read()

        return self._public_key

    @property
    def private_key(self) -> str:
        if self._private_key is None:
            with open(self._file_path, "r") as f:
                self._private_key = f.read()

        return self._private_key

    @staticmethod
    def generate(file_path: str) -> "AdbKey":
        keygen(file_path)
        return AdbKey(file_path)


@dataclass(frozen=True)
class DeviceState:
    awake: bool | None = None
    screen_on: bool | None = None
    app: str | None = None
    playback_state: int | None = None


class GoogleTv:
    def __init__(self, adb_key: AdbKey, host: str, port: int = 5555) -> None:
        self._adb = AdbDeviceTcpAsync(host, port)
        self._adb_key = adb_key

        self._state = DeviceState()

    @property
    def state(self) -> DeviceState:
        return self._state

    async def connect(self) -> None:
        signer = PythonRSASigner(self._adb_key.public_key, self._adb_key.private_key)
        await self._adb.connect(rsa_keys=[signer])

    async def close(self) -> None:
        await self._adb.close()

    async def update(self) -> None:
        dumpsys_power = await self._adb.shell(CMD_DUMPSYS_POWER)
        awake = self._parse_awake(dumpsys_power)
        if not awake:
            new_state = DeviceState(awake=awake)
        else:
            dumpsys_display = await self._send_command(CMD_DUMPSYS_DISPLAY)
            dumpsys_activity = await self._send_command(CMD_DUMPSYS_ACTIVITY)
            dumpsys_media_session = await self._send_command(CMD_DUMPSYS_MEDIA_SESSION)

            app = self._parse_current_app(dumpsys_activity)
            if app:
                playback_state = self._parse_playback_state(dumpsys_media_session, app)
            else:
                playback_state = None

            new_state = DeviceState(
                awake=self._parse_awake(dumpsys_power),
                screen_on=self._parse_screen_on(dumpsys_display),
                app=app,
                playback_state=playback_state,
            )

        self._state = new_state

    async def _send_command(
        self,
        command: str,
        retries: int = ADB_MAX_RETRIES,
        retry_interval: float = ADB_RETRY_INTERVAL,
    ) -> str:
        for _ in range(retries):
            result = await self._adb.shell(command)
            if CMD_DUMPSYS_ERROR not in result:
                return result

            await asyncio.sleep(retry_interval)

        raise GoogleTvException(f"Failed to send command {command}")

    def _parse_awake(self, dumpsys_power: str) -> bool | None:
        if re.search(REGEX_AWAKE, dumpsys_power):
            return True
        if re.search(REGEX_ASLEEP, dumpsys_power):
            return False
        return None

    def _parse_screen_on(self, dumpsys_display: str) -> bool | None:
        if re.search(REGEX_SCREEN_ON, dumpsys_display):
            return True
        if re.search(REGEX_SCREEN_OFF, dumpsys_display):
            return False
        return None

    def _parse_current_app(self, dumpsys_activity: str) -> str | None:
        matches = search_nested(
            (REGEX_ACTIVITY, REGEX_ACTIVITY_RESUMED), dumpsys_activity
        )
        if matches:
            app = matches[0].group("app")
            return APPS.get(app, app)

        return None

    def _parse_playback_state(self, dumpsys_media_session: str, app: str) -> int | None:
        matches = search_nested(
            (REGEX_SESSION, app, REGEX_PLAYBACK_STATE), dumpsys_media_session
        )
        if matches:
            return int(matches[2].group("state"))

        return None
