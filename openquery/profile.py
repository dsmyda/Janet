from pathlib import Path

_profile_path = Path.home().joinpath(".openquery", "profiles")
_synth_path = _profile_path.joinpath("synths")

class Profile:

    def __init__(self, **kwargs):
        self._name = kwargs["name"] or "-"
        self._database_user = kwargs["database_user"] or "-"
        self._database_password = kwargs["database_password"] or "-"
        self._database_host = kwargs["database_host"] or "-"
        self._database_port = kwargs["database_port"] or "-"
        self._database_engine = kwargs["database_engine"] or "-"
        self._openai_key = kwargs["openai_key"] or "-"       
        self._default_run = kwargs["default_run"] or False
        self._active = kwargs["active"] or False

    @staticmethod
    def create_cli() -> Profile:
        pass
    
    @staticmethod
    def _deserialize(data: bytes) -> Profile:
        pass

    def _serialize(self) -> bytes:
        pass

    def update_cli():
        pass

    def get_synth(name: str) -> Synth:
        pass

    def save_synth(synth: Synth):
        pass

    def save(self):
        pass

    @staticmethod
    def delete(name: str):
        pass

    @staticmethod
    def load(name: str) -> Profile:
        pass

    @staticmethod
    def get_active() -> Profile:
        pass

