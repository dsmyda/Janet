from database_profile import DatabaseProfile

_synth_dir = Path("synths")

class Synth:

    def __init__(self, **kwargs):
        self._name = kwargs["name"] 
        self._schemas = kwargs["schemas"]
        self._includes = kwargs["includes"]
        self._excludes = kwargs["excludes"]
        self._parent_path = kwargs["parent_path"]
        self._path = self._parent_path.joinpath(self._name)

    def __str__(self):
        return """
Synth: {}

Schemas: {}
Includes: {}
Excludes: {}
""".format(
        self._name, 
        self._schemas, 
        self._includes, 
        self.excludes
    )

    def save(self):
        pass

    def minify(self):
        pass

    @staticmethod
    def delete(name: str):
        pass

    @staticmethod
    def exists(name: str):
        pass

    @staticmethod
    def reflect(schemas: list[str], includes: list[str], excludes: list[str]):
        pass
