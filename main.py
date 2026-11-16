"""
single command mode
   python main.py plan
   python main.py request list
   python main.py request view "Monday Seminar"
   python main.py books process batch_commands.txt

   the command is executed once and then the program exits.

interactive mode
   python main.py manage

   enters a continuous command-line session. 
"""

import json
import sys

from loandesk.requests import Request
from loandesk.holdings import Holdings
from loandesk.loan_desk_manager import LoanDeskManager


def load_application():
    """
    read the config file and get paths, then read requests, holdings, while creating those objects too. create manager object
    """
    with open("config.json", "r") as file:
        config = json.load(file)

    requests_path = config["request_file"]
    holdings_path = config["holdings_file"]
    report_path = config["report_file"]

    with open(requests_path, "r") as file:
        requests_data = json.load(file)

    requests = []

    for item in requests_data:
        request = Request(item["name"], item["books"])
        requests.append(request)

    with open(holdings_path, "r") as file:
        holdings_data = json.load(file)

    holdings = Holdings(holdings_data)

    manager = LoanDeskManager(
        requests,
        holdings,
        holdings_path,
        report_path
    )

    return manager


def run_interactive(manager):
    """
    run the interactive command loop until the user types 'exit'
    """
    print("Welcome to LoanDesk!")
    print("Enter a command or type 'exit' to quit.")

    while True:
        try:
            command_line = input("> ").strip()

        except KeyboardInterrupt:
            print()
            manager.save_holdings()
            print("Holdings saved!")
            break

        except EOFError:
            print()
            manager.save_holdings()
            print("Holdings saved!")
            break

        if command_line == "":
            continue

        if command_line.lower() == "exit":
            manager.save_holdings()
            print("Holdings saved!")
            break

        arguments = manager.split_command(command_line)

        try:
            manager.execute(arguments)

        except ValueError as error:
            print(f"Error: {error}")

        except OSError as error:
            print(f"File error: {error}")


def run_single_command(manager, arguments):
    """
    executes a single parsed command. used in every command other than 'manage'
    """
    try:
        manager.execute(arguments)

    except ValueError as error:
        print(f"Error: {error}")


def main():
    """
    reads sys.argv to decide between single-command mode and
    interactive mode.
    """
    try:
        if len(sys.argv) < 2:
            print("Usage: python main.py <command>")
            print("Examples:")
            print("  python main.py plan")
            print("  python main.py manage")
            print("  python main.py request list")
            print('  python main.py request view "Monday Seminar"')
            print('  python main.py books add "The Little Prince" 2')
            print("  python main.py books process batch_commands.txt")
            return

        mode = sys.argv[1].lower()

        manager = load_application()

        if mode == "manage" and len(sys.argv) == 2:
            run_interactive(manager)
            return
        
        run_single_command(manager, sys.argv[1:])

    except FileNotFoundError as error:
        print(f"Error: File not found: {error.filename}")

    except json.JSONDecodeError:
        print("Error: One of the JSON files contains invalid data.")

    except KeyError as error:
        print(f"Error: Missing information in a JSON file: {error}")

    except KeyboardInterrupt:
        print("\nProgram interrupted.")

    except OSError as error:
        print(f"File error: {error}")


if __name__ == "__main__":
    main()