import tkinter as tk
from tkinter import ttk, messagebox

from Account import Account
from Expense import Expense
from Income import Income
from InputFrame import InputFrame
from DisplayFrame import DisplayFrame
from DataManager import DataManager

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.geometry("950x520")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.account = Account()
        self.data_manager = DataManager("transactions.csv")
        self.data_manager.load_data(self.account)
        
        self.current_visible_transactions = []

        self.input_frame = InputFrame(self, on_add_callback=self.add_new_transaction, on_export_callback=self.export_backup)
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.display_frame = DisplayFrame(self, on_delete_callback=self.delete_transaction, on_filter_callback=self.apply_ui_filter)
        self.display_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.refresh_ui_view()

    def add_new_transaction(self, t_type, amount, description, category, date):
        if t_type == "Expense":
            new_item = Expense(amount, description, category, date)
        else:
            new_item = Income(amount, description, category, date)

        self.account.add_transaction(new_item)
        self.data_manager.save_data(self.account)
        self.refresh_ui_view()

    def delete_transaction(self, index):
        if 0 <= index < len(self.current_visible_transactions):
            target = self.current_visible_transactions[index]
            self.account.remove_transaction(target)
            self.data_manager.save_data(self.account)
            self.refresh_ui_view()

    def apply_ui_filter(self, t_type, category):
        self.current_visible_transactions = self.account.filter_transactions(t_type, category)
        self.display_frame.refresh_display(self.current_visible_transactions)

    def export_backup(self):
        try:
            backup_manager = DataManager("finance_backup_export.csv")
            backup_manager.save_data(self.account)
            messagebox.showinfo("Export Success", "Successfully saved finance_backup_export.csv copy!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not create file backup: {e}")

    def refresh_ui_view(self):
        all_tx = self.account.get_all_transactions()
        self.current_visible_transactions = list(all_tx)
        
        self.display_frame.refresh_display(self.current_visible_transactions)
        self.display_frame.update_statistics(self.account.get_total_income(),self.account.get_total_expenses(),self.account.get_savings_rate())
        self.update_title_balance()

    def update_title_balance(self):
        current_balance = self.account.get_balance()
        self.title(f"Personal Finance Tracker | Current Balance: {current_balance:.2f} EUR")
        if current_balance < 0:
            self.title(f"️ WARNING: OVERDRAFT! Balance: {current_balance:.2f} EUR")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()