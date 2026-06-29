from Transaction import Transaction

class Income(Transaction):
    def __init__(self, amount, description, category, date=None):
        super().__init__(amount, description, date)
        self.category = self.validate_text(category, "Category")

    def get_signed_amount(self):
        return self.amount

    def matches_category(self, category):
        return self.category == category

    def to_list(self):
        return [self.date, self.category, self.description, f"{self.get_signed_amount():.2f}"]

    def __str__(self):
        return f"{self.date} | {self.category} | {self.description} | {self.get_signed_amount():.2f} EUR"