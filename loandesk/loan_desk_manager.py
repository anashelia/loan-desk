import json

class LoanDeskManager:
    """
    all command and title/name matching is case-insensitive.
    """

    def __init__(self, requests, holdings, holdings_file, report_file):
        """
        constructor
        """
        self.requests = requests
        self.holdings = holdings
        self.holdings_file = holdings_file
        self.report_file = report_file



    def save_holdings(self):
        with open(self.holdings_file, "w") as file:
            json.dump(self.holdings.holdings, file, indent=4) #extra whitespaces
            
            


    def find_request(self, name):
        """
        returt the request whose name matches 'name' case-insensitively.
        """
        for request in self.requests:
            if request.name.lower() == name.lower():
                return request

        return None



    def list_requests(self):
        """
        print a numbered list of all request names
        """
        for i, request in enumerate(self.requests, start=1):
            print(f"{i}. {request.name}")



    def view_request(self, name):
        """
        print the requests name and the books it needs.
        """
        request = self.find_request(name)

        if request is None:
            print(f"Request '{name}' not found.")
            return

        print(f"Request: {request.name}")
        print("Books:")

        for title, quantity in request.books.items():
            print(f"- {title}: {quantity}")



    def gap_analysis(self, name):
        """
        print the missing copies for a single request.
        """
        request = self.find_request(name)

        if request is None:
            print(f"Request '{name}' not found.")
            return

        missing = {}

        for title, quantity in request.books.items():
            on_shelf = self.holdings.now_on_shelf(title)

            if on_shelf < quantity:
                missing[title] = quantity - on_shelf

        if len(missing) == 0:
            print(f"No missing copies for '{request.name}'.")
            return

        print(f"Missing copies for '{request.name}':")

        for title, quantity in missing.items():
            print(f"- {title}: {quantity}")



    def plan(self):
        """
        print every request that can be lent from the current shelf.
        """
        available_requests = []

        for request in self.requests:
            can_lend = True

            for title, quantity in request.books.items():
                on_shelf = self.holdings.now_on_shelf(title)

                if on_shelf < quantity:
                    can_lend = False
                    break

            if can_lend:
                available_requests.append(request.name)

        if len(available_requests) == 0:
            print("No request can be lent with the current shelves.")
            return

        print("Requests the desk can lend:")

        for name in available_requests:
            print(f"- {name}")

    def lend_request(self, name):
        """
        lend a request if the shelf can give out every title, so if all books are available
        """
        request = self.find_request(name)

        if request is None:
            print(f"Request '{name}' not found.")
            return False

        for title, quantity in request.books.items():
            on_shelf = self.holdings.now_on_shelf(title)

            if on_shelf < quantity:
                print(f"Cannot lend '{request.name}'.")
                print(f"Missing {quantity - on_shelf} copies of '{title}'.")
                return False


        for title, quantity in request.books.items():
            self.holdings.borrow_book(title, quantity)

        self.save_holdings()

        print(f"Successfully lent '{request.name}'.")
        return True



    def add_book_command(self, title, quantity):
        """
        execute a 'books add' command.
        if quantity isnt an integer, or isnt positive, it raises ValueError
        """
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        self.holdings.add_book(title, quantity)
        self.save_holdings()

        print(f"Successfully added {quantity} copies of '{title}'.")



    def return_book_command(self, title, quantity):
        """
        executes a 'books return' command.
        if quantity isnt an integer, or isnt positive, it raises ValueError
        """
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if not self.holdings.return_book(title, quantity):
            raise ValueError(
                f"Cannot return {quantity} copies of '{title}'."
            )

        self.save_holdings()

        print(f"Successfully returned {quantity} copies of '{title}'.")



    def split_command(self, line):
        """
        splits the command into individual words, and returns the list of those words
        """
        words = []
        current_word = ""
        inside_quotes = False

        for character in line:
            if character == '"':
                inside_quotes = not inside_quotes

            elif character == " " and not inside_quotes:
                if current_word != "":
                    words.append(current_word)
                    current_word = ""

            else:
                current_word += character

        if current_word != "":
            words.append(current_word)

        return words



    def process_batch(self, filepath):
        """
        executes every line of a batch file sequentially.
        """
        report = []

        try:
            with open(filepath, "r") as file:
                lines = file.readlines()

        except FileNotFoundError:
            print(f"File '{filepath}' not found.")
            return

        for line in lines:
            line = line.strip()

            if line == "":
                continue

            words = self.split_command(line)

            try:
                if len(words) != 3:
                    raise ValueError("Invalid command format.")

                command = words[0].upper()
                title = words[1]
                quantity = int(words[2])

                if quantity <= 0:
                    raise ValueError("Quantity must be a positive integer.")

                if command == "ADD":
                    self.holdings.add_book(title, quantity)

                elif command == "RETURN":
                    if not self.holdings.return_book(title, quantity):
                        raise ValueError(
                            f"Cannot RETURN {quantity} of '{title}'."
                        )

                else:
                    raise ValueError(f"Unknown command '{command}'.")

                report.append(f"SUCCESS: {line}")

            except ValueError as error:
                report.append(f"ERROR: {error}")

        self.save_holdings()

        with open(self.report_file, "w") as file:
            for result in report:
                file.write(result + "\n")

        print(f"Batch processing complete. See '{self.report_file}' for details.")

    def execute(self, arguments):
        """
        commands: plan; request list/view/gap/lend; books add/return 
        when reading anything other than those words, a message is outputed

        """
        if len(arguments) == 0:
            print("Please enter a command.")
            return

        command = arguments[0].lower()

        if command == "plan":
            self.plan()

        elif command == "request":

            if len(arguments) == 2 and arguments[1].lower() == "list":
                self.list_requests()

            elif len(arguments) == 3:
                action = arguments[1].lower()
                name = arguments[2]

                if action == "view":
                    self.view_request(name)

                elif action == "gap":
                    self.gap_analysis(name)

                elif action == "lend":
                    self.lend_request(name)

                else:
                    print("Invalid request command.")

            else:
                print("Invalid request command.")

        elif command == "books":

            try:
                if len(arguments) == 4:
                    action = arguments[1].lower()
                    title = arguments[2]
                    quantity = arguments[3]

                    if action == "add":
                        self.add_book_command(title, quantity)

                    elif action == "return":
                        self.return_book_command(title, quantity)

                    else:
                        print("Invalid books command.")

                elif len(arguments) == 3 and arguments[1].lower() == "process":
                    self.process_batch(arguments[2])

                else:
                    print("Invalid books command.")

            except ValueError as error:
                print(f"Error: {error}")

        else:
            print(f"Invalid command '{arguments[0]}'.")