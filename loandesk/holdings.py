class Holdings:

    def __init__(self, holdings):
        """
        constructor
        """
        self.holdings = holdings



    def _resolve_title(self, title):
        """
        return the key in 'holdings' that matches 'title', or none if 'title' doesnt exist
        """
        if title in self.holdings:
            return title

        lowered = title.lower()

        for stored_title in self.holdings:
            if stored_title.lower() == lowered:
                return stored_title

        return None



    def now_on_shelf(self, title):
        """
        return how many copies of the given title are currently on the shelf. if a title is missing, then  0 copies.
        """
        resolved = self._resolve_title(title)

        if resolved is None:
            return 0

        copies = self.holdings[resolved]["copies"]
        borrowed = self.holdings[resolved]["borrowed"]

        return copies - borrowed



    def add_book(self, title, quantity):
        """
        add the 'quantity' to the 'title' and if 'title' isnt in holdings yet, create it and set borrowed to 0
        """
        resolved = self._resolve_title(title)

        if resolved is None:
            self.holdings[title] = {
                "copies": 0,
                "borrowed": 0
            }
            resolved = title

        self.holdings[resolved]["copies"] += quantity



    def borrow_book(self, title, quantity):
        """
        increase the borrowed ammount ('quantity') of 'title'  and returns true
        if there arent enough copies, returns false and doesnt do anything else
        """
        resolved = self._resolve_title(title)

        if resolved is None:
            return False

        if self.now_on_shelf(resolved) < quantity:
            return False

        self.holdings[resolved]["borrowed"] += quantity
        return True



    def return_book(self, title, quantity):
        """
        decrease the borrowed ammount ('quantity') of 'title'  and returns true
        if you try to return more copies, than there are borrowed, returns false
        """
        resolved = self._resolve_title(title)

        if resolved is None:
            return False

        if self.holdings[resolved]["borrowed"] < quantity:
            return False

        self.holdings[resolved]["borrowed"] -= quantity
        return True


    