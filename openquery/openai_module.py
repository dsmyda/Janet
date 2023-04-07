from language_module import LanguageModule
from database_synth import Synth
from natural_language_query import NaturalLanguageQuery
from getpass import getpass

class OpenAILanguageModule(LanguageModule):
    
    def __init__(self, **kwargs):
        self._key = kwargs["key"]
        self._model = kwargs["model"]
        self._n = kwargs["n"]

    @staticmethod
    def create_cli():
        model = input("Enter the OpenAI model: (text-davinci-003)") or "text-davinci-003" 
        n = input("Enter number of queries to generate: (3)") or 3
        key = getpass(prompt="Enter your OpenAI API key: ")
        return OpenAILanguageModule(
            model=model,
            n=n,
            key=key
        )

    def get_prompt(self, synth: Synth, query: NaturalLanguageQuery):
        engine = Profile.get_active().get_engine()
        return '{}

Use the {} database below to create a SQL query to answer the question above. You must only return the SQL statement, do not include any additional text.
Use the indexes to make the query as efficient as possible.
    
{} database: """
{}
"""
'.format(
        query.as_text(), 
        engine, 
        engine, 
        synth.minify()
    )

    def generate_sql(self, synth: Synth, query: NaturalLanguageQuery):
        prompt = self.get_prompt(synth, query)
        pass

    @staticmethod
    def name():
        return "OpenAI"
