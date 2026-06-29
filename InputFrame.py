import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class InputFrame(ttk.Frame):
    def __init__(self, parent, on_add_callback, on_export_callback):
        super().__init__(parent, padding=10)
        self.on_add_callback = on_add_callback
        self.on_export_callback = on_export_callback

        title_label = ttk.Label(self, text="Add New Transaction", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(self, text="Type:").grid(row=1, column=0, sticky="w", pady=5)
        self.type_var = tk.StringVar(value="Expense")
        self.type_combo = ttk.Combobox(self, textvariable=self.type_var, values=["Expense", "Income"], state="readonly")
        self.type_combo.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Amount (EUR):").grid(row=2, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Category:").grid(row=3, column=0, sticky="w", pady=5)
        self.category_entry = ttk.Entry(self)
        self.category_entry.grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Description:").grid(row=4, column=0, sticky="w", pady=5)
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=4, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", pady=5)
        self.date_entry = ttk.Entry(self)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=5, column=1, sticky="ew", pady=5)

        self.submit_btn = ttk.Button(self, text="Add Transaction", command=self.handle_submit)
        self.submit_btn.grid(row=6, column=0, columnspan=2, pady=(15, 5))
        
        self.export_btn = ttk.Button(self, text="Export CSV Backup File", command=self.handle_export)
        self.export_btn.grid(row=7, column=0, columnspan=2, pady=5)

        self.grid_columnconfigure(1, weight=1)

    def handle_submit(self):
        t_type = self.type_var.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()
        date = self.date_entry.get()

        try:
            self.on_add_callback(t_type, amount, description, category, date)
            self.clear_inputs()
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def handle_export(self):
        self.on_export_callback()

    def clear_inputs(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))