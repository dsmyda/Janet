from cryptography.fernet import Fernet
from pathlib import Path
import bz2
import keyring

_default_base_path = Path.home().joinpath(".openquery")

class Resource:
    
    def __init__(self, name: str, **kwargs):
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
        encrypted_data = self.path.read_bytes()
        key = keyring.get_password("openquery", "encryption_key")
        if not key:
            raise Exception("Encryption key not found in keyring service. All previously stored configuration is lost. Please run 'openquery init' again.")
        decrypted_data = Fernet(key).decrypt(encrypted_data)
        decompressed_data = bz2.decompress(decrypted_data)
        return decompressed_data

    def write_bytes(self, data: bytes):
        compressed_binary = bz2.compress(data)
        key = keyring.get_password("openquery", "encryption_key")
        if not key:
            raise Exception("Encryption key not found in keyring service. All previously stored configuration is lost. Please run 'openquery init' again.")
        encrypted = Fernet(key).encrypt(compressed_binary)
        self.path.write_bytes(encrypted)

    def delete(self):
        self.path.unlink()

    def symlink(self, resource):
        other_path = resource.path
        self.path.symlink_to(other_path)

    def resolve(self):
        self.path = self.path.resolve()

    def get_name(self):
        return self.path.name

    def list_dirs(self):
        return [child.name for child in self.path.iterdir() if child.is_dir()]
