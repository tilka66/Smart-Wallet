class Account:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def remove_transaction(self, transaction):
        if transaction in self.transactions:
            self.transactions.remove(transaction)

    def get_all_transactions(self):
        return self.transactions

    def get_balance(self):
        total = 0.0
        for t in self.transactions:
            total += t.get_signed_amount()
        return total

    def get_by_category(self, category):
        return [t for t in self.transactions if t.matches_category(category)]

    def get_total_income(self):
        total = 0.0
        for t in self.transactions:
            if type(t).__name__ == "Income":
                total += t.get_signed_amount()
        return total

    def get_total_expenses(self):
        total = 0.0
        for t in self.transactions:
            if type(t).__name__ == "Expense":
                total += abs(t.get_signed_amount())
        return total

    def get_savings_rate(self):
        income = self.get_total_income()
        if income == 0:
            return 0.0
        expenses = self.get_total_expenses()
        savings = income - expenses
        return (savings / income) * 100

    def filter_transactions(self, t_type="All", category=""):
        filtered = self.transactions
        if t_type != "All":
            filtered = [t for t in filtered if type(t).__name__ == t_type]
        if category.strip() != "":
            filtered = [t for t in filtered if category.lower() in getattr(t, 'category', '').lower()]
        return filtered