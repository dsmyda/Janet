
import db
import disk
import pickle

SYNTH_HEADER = 0x01

_ACTIVE_SYNTH_SYMLINK = ".active_synth"

def activate(name):
    if disk.exists(_ACTIVE_SYNTH_SYMLINK):
        disk.delete(_ACTIVE_SYNTH_SYMLINK)
    disk.symlink(_ACTIVE_SYNTH_SYMLINK, name)

def get_active():
    if not disk.exists(_ACTIVE_SYNTH_SYMLINK):
        raise Exception("No active synth configuration")
    return disk.get_resolved_name(_ACTIVE_SYNTH_SYMLINK)

def _save(name: str, data):
    pickled = pickle.dumps(data)
    data = bytes([SYNTH_HEADER]) + pickled
    disk.write_bytes(name, data)
    if not disk.exists(_ACTIVE_SYNTH_SYMLINK):
        activate(name)

def _load(name: str):
    data = disk.read_bytes(name)
    header = data[0]
    if header != SYNTH_HEADER:
        raise Exception("Unsupported synth header: {}".format(header))

    return pickle.loads(data[1:])

def _minify(synth):
    minified = []
    for structure in synth["structures"]:
        minified.append(
            structure.replace("\n", "").replace("\t", "").replace("\"", "").replace("CREATE ", "") + "\n"
        )
    
    return {
        "structures": minified,
    }

def get_for_question(name: str):
    return _minify(_load(name))["structures"]

def create_cli():
    db_config = db.get_active()

    name = input("Enter a name for this synth: (default_synth)") or "default_synth"
    if disk.exists(name):
        raise Exception("Synth {} already exists".format(name))
    
    schemas = input("Enter schemas to reflect (comma separated): (public)") or "public"
    schemas = [s.strip() for s in schemas.split(",")]
    includes = input("Enter tables to include (comma separated): (all)") or None
    if includes:
        includes = [s.strip() for s in includes.split(",")]

    synth = db.reflect(db_config, schemas, includes)
    _save(name, synth)