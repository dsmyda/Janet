import argparse
import sys

class OpenQueryCLI:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="openquery",
            description="Automagically generate and run SQL using natural language queries",
            usage="""openquery <command> [<args>]

The most commonly used openquery commands are:
    init        Initialize openquery
    ask         Ask a question
    synth       Create and manage database synths
    database    Create, manage and switch between databases profiles 
    module      Create, manage and switch between language modules
    list        List existing resources (profiles, synths, modules, etc).
""")
        parser.add_argument(
            "command",
            help="Subcommand to run"
        )
    
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)
        
        getattr(self, args.command)()

    def init(self):
        pass
    
    def synth(self):
        parser = argparse.ArgumentParser(
            prog="openquery synth",
            description="Create a database synthesis using the active database profile"
        )

        parser.add_argument(
            "name",
            help="The unique name of this synth, which you'll use when calling other commands."
        )

        parser.add_argument(
            "-i",
            "--include-table",
            metavar="table",
            action="append",
            nargs=1,
            help="Include the specified table. Multiple tables can be included by writing multiple -i switches.",
        )        
        
        parser.add_argument(
            "-e",
            "--exclude-table",
            metavar="table",
            action="append",
            nargs=1,
            help="Exclude the specified table. Multiple tables can be excluded by writing multiple -e switches.",
        )
        
        parser.add_argument(
            "-s",
            "--schema",
            metavar="schema",
            action="append",
            nargs=1,
            help="Synth only the specified schema. Multiple schemas can be selected by writing multiple -s switches.",
        )

        args = parser.parse_args(sys.argv[2:])
    
    def ask(self):
        parser = argparse.ArgumentParser(
            prog="openquery ask",
            description="Ask a question and receive a SQL query. Optionally, you can opt-in to have the query automagically run by specifiying -r or by configuring it as the default behavior in your database profile."
        )

        parser.add_argument(
            "-s",
            "--synth",
            metavar="synth",
            nargs=1,
            help="The name of the synth to attach to the question prompt.",
            required=True
        )

        parser.add_argument(
            "-r",
            "--run",
            action="store_true",
            help="Automagically run the query against the active database profile. You can configure the default behavior in the database profile."
        )

        parser.add_argument(
            "question",
            metavar="question",
            help="A natural language question for openquery to answer"
        )

        args = parser.parse_args(sys.argv[2:])

    def database(self):
        parser = argparse.ArgumentParser(
            prog="openquery database",
            description="Manage and switch between database profiles. A database profile contains connection information, cached synths and default behavior."
        )

        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "-c",
            "--create",
            action="store_true",
            help="Create a new database profile, you'll be walked through a WYSIWYG",
        )
            
        group.add_argument(
            "-d",
            "--delete",
            metavar="profile",
            help="Delete an existing database profile"
        )

        group.add_argument(
            "-s",
            "--switch",
            metavar="profile",
            help="Switch to another database profile"
        )
        
        args = parser.parse_args(sys.argv[2:])

    def module(self):
        parser = argparse.ArgumentParser(
            prog="openquery module",
            description="Configure and switch between language modules. A language module abstracts how language model(s) are invoked and how the output is parsed. Use 'openquery list -m' to list the language modules supported in this installation"
        )

        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "-c",
            "--configure",
            metavar="module",
            help="Configure a language module, you'll be walked through a WYSIWYG",
        )
            
        group.add_argument(
            "-d",
            "--delete",
            metavar="module",
            help="Delete an existing language module config"
        )

        group.add_argument(
            "-s",
            "--switch",
            metavar="module",
            help="Switch to another language module config"
        )

        args = parser.parse_args(sys.argv[2:])
    
    def list(self):
        parser = argparse.ArgumentParser(
            prog="openquery list",
            description="List existing resources (database profiles, language modules, synths)"
        ) 

        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "-d",
            "--databases",
            help="List databases profiles"
        )

        group.add_argument(
            "-m",
            "--modules",
            help="List language modules"
        )

        group.add_argument(
            "-s",
            "--synths",
            help="List database synths"
        )

        group.add_argument(
            "-a",
            "--active",
            help="List all active resources"
        )

        args = parser.parse_args(sys.argv[2:])

if __name__ == '__main__':
   OpenQueryCLI() 
