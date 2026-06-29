import csv
import os

from Transaction import Transaction
from Expense import Expense
from Income import Income

class DataManager:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self.headers = ["Type", "Amount", "Description", "Category", "Date"]

    def save_data(self, account):
        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
                for t in account.get_all_transactions():
                    writer.writerow([ type(t).__name__,t.amount,t.description,getattr(t, 'category', 'General'),t.date])
        except IOError as e:
            raise IOError(f"Failed to save data to CSV file: {e}")

    def load_data(self, account):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                try:
                    header = next(reader)
                except StopIteration:
                    return
                for row in reader:
                    if not row or len(row) < 5:
                        continue
                    t_type, amount, description, category, date = row
                    if t_type == "Expense":
                        t = Expense(amount, description, category, date)
                    elif t_type == "Income":
                        t = Income(amount, description, category, date)
                    else:
                        t = Transaction(amount, description, date)
                    account.add_transaction(t)
        except (IOError, ValueError) as e:
            print(f"Warning: Could not fully read data file ({e}). Starting fresh.")