from datetime import datetime

class Transaction:
    def __init__(self, amount, description, date=None):
        self.amount = self.validate_amount(amount)
        self.description = self.validate_text(description, "Description")
        self.date = self.validate_date(date)

    def validate_amount(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            raise ValueError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        return amount

    def validate_text(self, text, field_name):
        text = str(text).strip()
        if text == "":
            raise ValueError(field_name + " cannot be empty.")
        return text

    def validate_date(self, date):
        if date is None or str(date).strip() == "":
            return datetime.today().strftime("%Y-%m-%d")
        date = str(date).strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must have the format YYYY-MM-DD.")
        return date

    def get_signed_amount(self):
        return self.amount

    def matches_category(self, category):
        return True

    def to_list(self):

        return [self.date, "General", self.description, f"{self.get_signed_amount():.2f}"]

    def __str__(self):
        return f"{self.date} | {self.description} | {self.get_signed_amount():.2f} EUR"