class Synth:

    def __init__(self):
        pass

    def _serialize(self) -> bytes:
        pass
    
    @staticmethod
    def _deserialize(data: bytes) -> Synth:
        pass

    @staticmethod
    def load(name: str) -> Synth:
        pass

    def save(self):
        pass

    @staticmethod
    def delete(name: str):
        pass

    def minify(self) -> str:
        pass

    @staticmethod
    def reflect(schemas, includes, excludes):
        # Profile.getActive()
        pass

