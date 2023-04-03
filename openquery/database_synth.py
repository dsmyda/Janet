class DatabaseSynth:

    def __init__(self):
        pass

    def _serialize(self) -> bytes:
        pass
    
    @staticmethod
    def _deserialize(data: bytes) -> DatabaseSynth:
        pass

    @staticmethod
    def load(name: Name) -> DatabaseSynth:
        pass

    def save(self):
        pass

    @staticmethod
    def delete(name: Name):
        pass

    def minify(self) -> str:
        pass

    @staticmethod
    def reflect(schemas, includes, excludes):
        # DatabaseProfile.get_active()
        pass
    
    @staticmethod
    def exists(name: Name) -> bool:
        pass

    @staticmethod
    def list() -> list[ResourceName]:
        pass
