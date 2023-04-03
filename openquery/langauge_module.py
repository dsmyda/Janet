from abc import ABC

_module_path = Path.home().joinpath(".openquery", "language_modules")
# configure with pii protection

class LanguageModule(ABC):

    def init():
        pass

    def save():
        pass

    @staticmethod
    @abstractmethod
    def delete(name: str):
        pass

    @staticmethod
    @abstractmethod
    def load(name: str):
        pass
