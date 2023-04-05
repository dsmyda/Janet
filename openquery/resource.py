from pathlib import Path

_default_base_path = Path.home().joinpath(".openquery")

class Resource:
    
    def __init__(self, name: str, **kwargs):
        if len(name) > 64:
            raise Exception("Resource name must be less than 64 characters")
        if not name.isalnum():
            raise Exception("Resource name must be alphanumeric")

        relative_path = kwargs.get("relative_path", ".")
        base_path = kwargs.get("base_path", _default_base_path)

        self._name = name
        self.path = base_path.joinpath(relative_path, name)

    def exists(self):
        return self.path.exists()

    def create(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch()

    def read_bytes(self) -> bytes:
        return self.path.read_bytes()

    def write_bytes(self, data: bytes):
        self.path.write_bytes(data)

    def delete(self):
        self.path.unlink()

    def symlink(self, resource):
        other_path = resource.path
        self.path.symlink_to(other_path)

    def resolve(self):
        self.path = self.path.resolve()
