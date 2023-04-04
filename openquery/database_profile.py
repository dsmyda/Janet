from pathlib import Path

_profile_path = Path.home().joinpath(".openquery", "profiles")
_synth_path = _profile_path.joinpath("synths")
_active_file = _profile_path.joinpath(".active")

class DatabaseProfile:

    def __init__(self, **kwargs):
        self._name = kwargs["name"] or "-"
        self._user = kwargs["user"] or "-"
        self._password = kwargs["password"] or "-"
        self._host = kwargs["host"] or "-"
        self._port = kwargs["port"] or "-"
        self._engine = kwargs["engine"] or "-"
        self._default_run = kwargs["default_run"] or False

    @staticmethod
    def create_cli() -> DatabaseProfile:
        pass

    @staticmethod
    def _deserialize(data: bytes) -> DatabaseProfile:
        pass

    def _serialize(self) -> bytes:
        pass

    def get_synth(self, name: ResourceName) -> DatabaseSynth:
        pass

    def save_synth(self, synth: DatabaseSynth):
        pass

    def save(self):
        pass

    @staticmethod
    def delete(name: ResourceName):
        pass

    @staticmethod
    def load(name: ResourceName) -> DatabaseProfile:
        pass

    def set_active(self):
        # replace current active file with self
        pass

    @staticmethod
    def get_active() -> DatabaseProfile:
        # follow symlink at ".active"
        pass

    @staticmethod
    def exists(name: ResourceName) -> bool:
        pass

    @staticmethod
    def list() -> list[ResourceName]:
        pass
