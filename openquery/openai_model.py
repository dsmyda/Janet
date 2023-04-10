# from natural_language_query import NaturalLanguageQuery
from getpass import getpass
import synth
import openai
import disk
import pickle
import json

OPENAI_HEADER = 0x02

_ACTIVE_MODEL_SYMLINK = ".active_model"

def _create_prompt(question: str, synth_name: str):
    ddl = synth.get_for_question(synth_name)

    prompt =  """
Write a SQL query that answers the following question given the schema below. You must only return SQL. Use relevant views/indexes to make the query efficient.
schema \"\"\"
{}
\"\"\"
question \"\"\"
{}
\"\"\"
    """.format(
        '\n'.join(ddl),
        question
    )
    return prompt.strip()

def activate(name):
    if disk.exists(_ACTIVE_MODEL_SYMLINK):
        disk.delete(_ACTIVE_MODEL_SYMLINK)
    disk.symlink(_ACTIVE_MODEL_SYMLINK, name)

def _save(name: str, data):
    pickled = pickle.dumps(data)
    data = bytes([OPENAI_HEADER]) + pickled
    disk.write_bytes(name, data)
    if not disk.exists(_ACTIVE_MODEL_SYMLINK):
        activate(name)

def _load(name: str):
    data = disk.read_bytes(name)
    header = data[0]
    if header != OPENAI_HEADER:
        raise Exception("Unsupported openai model header: {}".format(header))
    return pickle.loads(data[1:])

def create_cli():
    name = input("Enter a name for this openai model: (default_openai)") or "default_openai"
    if disk.exists(name):
        raise Exception("Model {} already exists".format(name))

    model = input("Enter the OpenAI model: (text-davinci-003)") or "text-davinci-003" 
    n = input("Enter number of queries to generate: (3)") or 3
    max_tokens = input("Enter maximum number of tokens per query: (2000)") or 2000
    key = getpass(prompt="Enter your OpenAI API key: ")

    config = {
        "model": model,
        "n": n,
        "key": key,
        "max_tokens": max_tokens,
    }

    _save(name, config)

def get_active():
    if not disk.exists(_ACTIVE_MODEL_SYMLINK):
        raise Exception("No active openai model configuration")
    return disk.get_resolved_name(_ACTIVE_MODEL_SYMLINK)

def ask(question: str):
    active_synth = synth.get_active()
    model = _load(get_active())
    openai.api_key = model["key"]
    prompt = _create_prompt(question, active_synth)
    queries = openai.Completion.create(model=model["model"], prompt=prompt, n=model["n"], max_tokens=model["max_tokens"])
    return queries.choices

def save_training_data(question: str, completion: str):
    active_synth = synth.get_active()
    model = _load(get_active())
    prompt = _create_prompt(question, active_synth)
    data = {
        "prompt": prompt,
        "completion": completion,
    }
    
    disk.write_incremental(".training_data.jsonl", json.dumps(data) + "\n")