from pathlib import Path
from getpass import getpass
import sql_ast
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.schema import CreateTable
import urllib.parse
import disk
try:
    import cPickle as pickle
except:
    import pickle

DB_HEADER = 0x00
_REMOTE_TYPE = 0x01
_SQL_FILE_TYPE = 0x02

_ACTIVE_DB_SYMLINK = ".active_db"

def activate(name):
    if disk.exists(_ACTIVE_DB_SYMLINK):
        disk.delete(_ACTIVE_DB_SYMLINK)
    disk.symlink(_ACTIVE_DB_SYMLINK, name)

def get_active():
    if not disk.exists(_ACTIVE_DB_SYMLINK):
        raise Exception("No active database configuration")
    return disk.get_resolved_name(_ACTIVE_DB_SYMLINK)

def _save(name: str, data, sub_type: int):
    pickled = pickle.dumps(data)
    data = bytes([DB_HEADER, sub_type]) + pickled
    disk.write_bytes(name, data)
    if not disk.exists(_ACTIVE_DB_SYMLINK):
        activate(name)

def _load(name: str):
    data = disk.read_bytes(name)
    header = data[0]
    if header == DB_HEADER:
        sub_type = data[1]
        return sub_type, pickle.loads(data[2:])
    else:
        raise Exception("Unsupported database header: {}".format(header))

def create_cli():
    config_type = input("Enter database type (remote, file): (remote)") or "remote"
    name = input("Enter a name for this configuration: (default_db)") or "default_db"
    if disk.exists(name):
        raise Exception("Database configuration {} already exists".format(name))
    if config_type == "remote":
        _create_remote_cli(name)
    elif config_type == "file":
        _create_file_cli(name)
    else:
        raise Exception("Unsupported database type: {}".format(config_type))

def _create_remote_cli(name: str):
    engine = input("Enter database engine: (postgresql)") or "postgresql"
    host = input("Enter database host: (localhost)") or "localhost"
    port = input("Enter database port: (5432)") or 5432
    database_name = input("Enter database name: (postgres)") or "postgres"
    user = input("Enter database user name: (postgres)") or "postgres"
    password = getpass(prompt="Enter database user password: (postgres)") or "postgres"
    default_run = input("Run queries by default? (y/n): (y)") or "y"

    url = "{}://{}:{}@{}:{}/{}".format(engine, user, password, host, port, database_name)
    config = {
        "url": url,
        "default_run": default_run == "y",
    }

    _save(name, config, _REMOTE_TYPE)

def _create_file_cli(name: str):
    path = input("Enter sql file path: (.)") or "."
    if not Path(path).exists():
        raise Exception("File {} does not exist".format(path))
    
    config = {
        "path": path
    }

    _save(name, config, _SQL_FILE_TYPE)

def run_query(name: str, query: str):
    sub_type, config = _load(name)
    if sub_type != _REMOTE_TYPE:
        raise Exception("Cannot run query on non-remote database configurations")

    if not config["default_run"]:
        raise Exception("Database {} is not set to run queries by default".format(name))
    
    if not sql_ast.is_query(query):
        raise Exception("SQL statement is not a query")

    query = sql_ast.standardize(query)
    query_text = text(query)

    engine = create_engine(config["url"])
    with engine.connect() as conn:
        result = conn.execute(query_text)
        for row in result:
            yield row._asdict()

def _reflect_remote(config, schemas: list[str], includes: list[str] = None):
    engine = create_engine(config["url"])
    structures = []
    with engine.connect() as conn:
        for schema in schemas:
            metadata = MetaData()
            metadata.reflect(bind=conn, schema=schema, only=includes)
            for table in metadata.tables.values():
                ddl = CreateTable(table).compile(engine).string.strip()
                structures.append(ddl)
    
    return {
        "structures": structures,
    }

def _reflect_file(config, schemas: list[str], includes: list[str]):
    raise Exception("Not implemented")

def reflect(name: str, schemas: list[str], includes: list[str]):
    sub_type, config = _load(name)

    if sub_type == _REMOTE_TYPE:
        return _reflect_remote(config, schemas, includes)
    elif sub_type == _SQL_FILE_TYPE:
        return _reflect_file(config, schemas, includes)
    else:
        raise Exception("Unsupported database configuration type: {}".format(sub_type))