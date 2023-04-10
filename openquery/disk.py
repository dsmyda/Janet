import bz2
import keyring
from pathlib import Path
from cryptography.fernet import Fernet

_default_base_path = Path.home().joinpath(".openquery")
_resource_path = _default_base_path.joinpath("resources")

def _get_path(name: str):
    return _resource_path.joinpath(name)

def read_bytes(name: str):
    if not exists(name):
        raise Exception("Resource with name '{}' does not exist.".format(name))
    path = _get_path(name)
    encrypted_data = path.read_bytes()
    key = keyring.get_password("openquery", "encryption_key")
    if not key:
        raise Exception("Encryption key not found in keyring service. All previously \
        stored configuration is lost. Please run 'openquery init' again.")
    decrypted_data = Fernet(key).decrypt(encrypted_data)
    decompressed_data = bz2.decompress(decrypted_data)
    return decompressed_data

def write_bytes(name: str, data: bytes):
    compressed_binary = bz2.compress(data)
    key = keyring.get_password("openquery", "encryption_key")
    if not key:
        raise Exception("Encryption key not found in keyring service. All previously \
        stored configuration is lost. Please run 'openquery init' again.")
    encrypted = Fernet(key).encrypt(compressed_binary)
    path = _get_path(name)
    if not exists(name):
        create(name)
    path.write_bytes(encrypted)

def write_incremental(name: str, data: bytes):
    with open(_get_path(name), "a") as f:
        f.write(data)

def delete(name: str):
    path = _get_path(name)
    path.unlink()

def exists(name: str):
    path = _get_path(name)
    return path.exists()

def create(name: str):
    path = _get_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()

def symlink(name: str, other_name: str):
    path = _get_path(name)
    other_path = _get_path(other_name)
    path.symlink_to(other_path)

def get_resolved_name(name: str):
    path = _get_path(name)
    path = path.resolve()
    return path.name

def list_all():
    return [f.name for f in _resource_path.iterdir() if f.is_file() and not f.name.startswith(".")]