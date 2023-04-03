from abc import ABC

_module_path = Path.home().joinpath(".openquery", "language_modules")
# configure with pii protection

class LanguageModule(ABC):

    @abstractmethod
    def init():
        pass
    
    @abstractmethod
    def save():
        pass

    @staticmethod
    @abstractmethod
    def delete(name: ResourceName):
        pass

    @staticmethod
    @abstractmethod
    def load(name: ResourceName):
        pass

    @staticmethod
    def get_active() -> LanguageModule:
        pass

    @abstractmethod
    def generate_sql(synth: DatabaseSynth, query: NaturalLanguageQuery) -> str[]:
        pass

    def generate_asts(synth: DatabaseSynth, query: NaturalLanguageQuery):
        queries = self.generate_sql(synth, query)
        pass
    
    @staticmethod
    def exists(name: ResourceName) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def create_cli():
        pass

    @staticmethod
    def list() -> list[ResourceName]:
        pass
