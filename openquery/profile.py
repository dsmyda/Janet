from pathlib import Path
from resource import Resource
from getpass import getpass
from sql_ast import AST
#from database_synth import Synth
try:
    import cPickle as pickle
except:
    import pickle
import bz2

_profile_dir = Path("profiles")

class Profile:

    def __init__(self, **kwargs):
        self._name = kwargs["name"]
        self._user = kwargs["user"]
        self._password = kwargs["password"]
        self._host = kwargs["host"]
        self._port = kwargs["port"]
        self._engine = kwargs["engine"]
        self._default_run = kwargs["default_run"]
        self._database_name = kwargs["database_name"]
        self._path = _profile_dir.joinpath(kwargs["name"])

    @staticmethod
    def create_cli():
        name = input("Enter profile name: ")
        engine = input("Enter database engine: ")
        host = input("Enter database host: ")
        port = input("Enter database port: ")
        database_name = input("Enter database name: ")
        user = input("Enter database user name: ")
        password = getpass(prompt="Enter database user password: ")
        default_run = input("Run queries by default? (y/n): ")
        profile = Profile(
            name=name,
            engine=engine,
            user=user,
            password=password,
            port=port,
            database_name=database_name,
            host=host,
            default_run=True if default_run == "y" else False
        )
        profile.save()
        active_symlink = Profile._sym() 
        if not active_symlink.exists():
            active_symlink.create()
            profile.set_active() 

    def get_synth(self, name: str):
        pass

    def query(sql: AST):
        pass

    def save(self):
        resource = Resource(self._name, relative_path=self._path) 
        resource.create()
        data = pickle.dumps(self)
        resource.write_bytes(data)

    def __str__(self):
        return """
Profile: {}

Database Engine: {},
Database User: {},
Database Password: {},
Database Host: {},
Database Port: {},
Database Name: {},
Run queries by default: {}
""".format(
        self._name, 
        self._engine, 
        self._user, 
        "*"*len(self._password), 
        self._host, 
        self._port, 
        self._database_name, 
        self._default_run
    )

    @staticmethod
    def delete(name: str):
        path = _profile_dir.joinpath(name)
        resource = Resource(name, relative_path=path) 
        resource.delete()
        if len(Profile.list()) == 0:
            active_symlink = Profile._sym() 
            active_symlink.delete() 

    def set_active(self):
        me = Resource(self._name, relative_path=self._path)
        active_symlink = Profile._sym() 
        active_symlink.delete()
        active_symlink.symlink(me)

    @staticmethod
    def _sym():
        return Resource("active", relative_path=_profile_dir)

    @staticmethod
    def get_active():
        active = Profile._sym() 
        if not active.exists():
            raise Exception("There is no active profile set, create a profile using 'openquery profile -c'")
        active.resolve()
        active_name = active.get_name()
        return Profile.fromName(active_name)

    @staticmethod
    def exists(name: str) -> bool:
        path = _profile_dir.joinpath(name)
        resource = Resource(name, relative_path=path) 
        return resource.exists()

    @staticmethod
    def list() -> list[any]:
        profile_dir = Resource(".", relative_path=_profile_dir)
        return [Profile.fromName(name) for name in profile_dir.list_dirs()]

    @staticmethod
    def fromName(name: str):
        if not Profile.exists(name):
            raise Exception("Profile %s does not exist" % name)
        path = _profile_dir.joinpath(name)
        resource = Resource(name, relative_path=path) 
        data = resource.read_bytes()
        profile = pickle.loads(data)
        return profile

    def get_engine():
        return self._engine
