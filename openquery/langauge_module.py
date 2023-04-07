from abc import ABC

_module_path = Path.home().joinpath(".openquery", "language_modules")

class LanguageModule(ABC):

    def save(self):
        # handle this automatically
        pass

    @staticmethod
    def fromName(self, name: str):
        pass

    @staticmethod
    @abstractmethod
    def create_cli():
        pass

    @staticmethod
    def delete(name: str):
        pass

    @staticmethod
    def get_active():
        pass

    def set_active(self):
        pass

    @abstractmethod
    def generate_sql(self, synth: DatabaseSynth, query: NaturalLanguageQuery) -> str[]:
        pass

    def generate_asts(synth: DatabaseSynth, query: NaturalLanguageQuery):
        queries = self.generate_sql(synth, query)
        pass
    
    @staticmethod
    def exists(name: str) -> bool:
        pass

    @staticmethod
    def list() -> list[any]:
        pass

    @staticmethod
    @abstractmethod
    def name():
        pass
