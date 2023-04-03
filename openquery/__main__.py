import argparse
import sys

class CLI:
    def __init__(self):

        parser = argparse.ArgumentParser(
            prog="openquery",
            description="Automatically generate and run SQL queries using natural language",
            usage="""openquery <command> [<args>]

The most commonly used openquery commands are:
    ask         Ask a question
    synth       Synthesize the database  connected to this profile
    profile     Manage and switch between different profiles
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
    
    def synth(self):
        parser = argparse.ArgumentParser(
            prog="openquery synth",
            description="Create a database synthesis using the connected profile"
        )

        parser.add_argument(
            "name",
            help="The unique name of this synth, which you'll use when calling other commands."
        )

        parser.add_argument(
            "-s",
            "--schema",
            metavar="schema",
            action="append",
            nargs=1,
            help="Synth only the specified schema. Multiple schemas can be selected by writing multiple -s switches.",
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
        
        args = parser.parse_args(sys.argv[2:])
    
    def ask(self):
        print('ask called')

    def profile(self):
        print('profile called')

if __name__ == '__main__':
   CLI() 
