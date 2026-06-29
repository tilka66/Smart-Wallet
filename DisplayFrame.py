import tkinter as tk
from tkinter import ttk

class DisplayFrame(ttk.Frame):
    def __init__(self, parent, on_delete_callback, on_filter_callback):
        super().__init__(parent, padding=10)
        self.on_delete_callback = on_delete_callback
        self.on_filter_callback = on_filter_callback
        
        filter_frame = ttk.LabelFrame(self, text="Filters & Controls", padding=5)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type_var = tk.StringVar(value="All")
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=["All", "Expense", "Income"], state="readonly", width=10)
        self.filter_type_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_cat_entry = ttk.Entry(filter_frame, width=15)
        self.filter_cat_entry.grid(row=0, column=3, padx=5, pady=5)
        
        filter_btn = ttk.Button(filter_frame, text="Apply Filter", command=self.handle_filter)
        filter_btn.grid(row=0, column=4, padx=5, pady=5)
        
        delete_btn = ttk.Button(filter_frame, text="Delete Selected", command=self.handle_delete)
        delete_btn.grid(row=0, column=5, padx=5, pady=5)
        
        columns = ("date", "category", "description", "amount")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("amount", text="Amount")
        self.tree.column("date", width=90)
        self.tree.column("category", width=100)
        self.tree.column("description", width=200)
        self.tree.column("amount", width=90, anchor="e")
        self.tree.grid(row=1, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.stats_frame = ttk.LabelFrame(self, text="Financial Breakdown Summary", padding=5)
        self.stats_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.inc_label = ttk.Label(self.stats_frame, text="Total Income: 0.00 EUR", font=("Arial", 10))
        self.inc_label.grid(row=0, column=0, padx=15, pady=5)
        self.exp_label = ttk.Label(self.stats_frame, text="Total Expenses: 0.00 EUR", font=("Arial", 10))
        self.exp_label.grid(row=0, column=1, padx=15, pady=5)
        self.rate_label = ttk.Label(self.stats_frame, text="Savings Rate: 0.0%", font=("Arial", 10))
        self.rate_label.grid(row=0, column=2, padx=15, pady=5)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def add_expense(self, expense):
        self.tree.insert("", tk.END, values=expense.to_list())
    
    def clear_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def refresh_display(self, expenses):
        self.clear_display()
        for expense in expenses:
            self.add_expense(expense)

    def update_statistics(self, total_inc, total_exp, savings_rate):
        self.inc_label.config(text=f"Total Income: {total_inc:.2f} EUR")
        self.exp_label.config(text=f"Total Expenses: {total_exp:.2f} EUR")
        self.rate_label.config(text=f"Savings Rate: {savings_rate:.1f}%")

    def handle_filter(self):
        t_type = self.filter_type_var.get()
        cat = self.filter_cat_entry.get()
        self.on_filter_callback(t_type, cat)

    def handle_delete(self):
        selected_item = self.tree.selection()
        if len(selected_item) == 0:
            return
        all_items = self.tree.get_children()
        selected_id = selected_item[0]
        idx = all_items.index(selected_id)
        self.on_delete_callback(idx)

    def get_selected_index(self):
        selected_item = self.tree.selection()
        if len(selected_item) == 0:
            return None
        all_items = self.tree.get_children()
        selected_id = selected_item[0]
        return all_items.index(selected_id)

    def get_number_of_rows(self):
        return len(self.tree.get_children())