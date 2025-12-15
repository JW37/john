import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from decimal import Decimal
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="John@12",
)


cursor = db.cursor()
cursor.execute("USE track")
db.commit()

class atm():
    def __init__(self,root):
        self.root = root
        self.root.title("Bank ATM Simulation")
        self.acEntry = tk.StringVar()
        self.amEntry = tk.DoubleVar()
        self.pEntry = tk.StringVar()
        self.username = tk.StringVar()
        self.pin = tk.StringVar()
        self.cpin = tk.StringVar()

        self.bank()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_inputs(self):
        self.acEntry.set("")
        self.pEntry.set("")
        self.amEntry.set("")
        self.username.set("")
        self.acEntry.set("")
        self.pin.set("")
        self.cpin.set("")


    def deposit(self):
        account = self.acEntry.get()
        amount = float(self.amEntry.get())
        balance = float(self.get_balance(account))
        new_balance = balance + amount
        self.set_balance(account, new_balance)

        messagebox.showinfo("Success",f"deposited {amount}")

    def withdraw(self):
        account = float(self.acEntry.get())
        amount = Decimal(self.amEntry.get())
        balance = Decimal(self.get_balance(account))
        if amount <= balance:
            new_balance = balance - amount
            messagebox.showinfo("Success", f"Withdrawn {amount}")
        else:
            messagebox.showerror("Error", "Insufficiant balance")
        self.set_balance(account, new_balance)
        self.clear_inputs()

    def get_balance(self, account):
        cursor.execute("SELECT balance FROM accounts WHERE account_number=%s", (account,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def set_balance(self, account, new_balance):
        cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s", (new_balance, account))
        db.commit()


    def update(self):
        
        account = self.acEntry.get()

        balance = self.get_balance(account)

        self.clear_frame()
        bal_label = tk.Label(self.root, text=f"Balance: ${balance}", font=("Arial", 20))
        bal_label.pack()

        entryFrame = ttk.Frame(self.root)
        entryFrame.pack(pady=10)

        exitButton = tk.Button(entryFrame, text="Exit", bg="gray", relief="groove", font=("Arial",12,"bold"), width=12, command=self.bank)
        exitButton.grid(row=5, column=0, padx=10, columnspan=2, pady=5)

        cursor.execute("UPDATE accounts SET balance=%s WHERE account_number=%s", (balance, account))
        db.commit()


    def create_ac(self):
        user = self.username.get().strip()
        aco = self.acEntry.get()
        pin = self.pin.get()
        cpin = self.cpin.get()

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "Pin must be a 4 digin number")
            return
        if not user or not aco or not pin or not cpin:
            messagebox.showerror("Error", "All fields are required")
            return 
        if pin != cpin:
            messagebox.showerror("Error", "Pin does not match")
            return
        
        cursor.execute("INSERT INTO accounts (username, account_number, pin, balance) VALUES (%s, %s, %s, %s)",
                   (user, aco, pin, 0))
        db.commit()
        self.bank()

        

    def bank(self):
        self.clear_inputs()
        self.clear_frame()

        label = tk.Label(self.root, background="black", bd=3, foreground="white", relief="groove", text="Bank ATM Simulation", font=("Arial",50,"bold"))
        label.pack(side="top", fill="x")

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        entryFrame = ttk.Frame(self.root)
        entryFrame.pack(pady=10)

        accountLabel = ttk.Label(entryFrame, text="Account Number", font=("Arial",12))
        accountLabel.grid(row=0, column=0, padx=5)

        self.accountEntry = tk.Entry(entryFrame, textvariable=self.acEntry, font=("Arial",12))
        self.accountEntry.grid(row=0, column=1)

        pinLabel = ttk.Label(entryFrame, text="PIN", font=("Arial",12))
        pinLabel.grid(row=1, column=0, padx=5)

        self.pinEntry = tk.Entry(entryFrame, textvariable=self.pEntry, font=("Arial",12), show="*")
        self.pinEntry.grid(row=1, column=1)

        amountLabel = ttk.Label(entryFrame, text="Amount", font=("Arial",12))
        amountLabel.grid(row=2, column=0, padx=5)

        self.amountEntry = tk.Entry(entryFrame, textvariable=self.amEntry, font=("Arial",12))
        self.amountEntry.grid(row=2, column=1)

        WithdrawButton = tk.Button(entryFrame, text="Withdraw", bg="gray", relief="groove", font=("Arial",12,"bold"), width=20, command=self.withdraw)
        WithdrawButton.grid(row=3, column=0, padx=10, columnspan=2, pady=5)

        DepositButton = tk.Button(entryFrame, text="Deposit", bg="gray", relief="groove", font=("Arial",12,"bold"), width=20, command=self.deposit)
        DepositButton.grid(row=4, column=0, padx=10, columnspan=2, pady=5)

        CheckButton = tk.Button(entryFrame, text="Check Balance", bg="gray", relief="groove", font=("Arial",12,"bold"), width=20, command=self.update)
        CheckButton.grid(row=5, column=0, padx=10, columnspan=2, pady=5)

        addButton = tk.Button(entryFrame, text="Create User Account", bg="gray", relief="groove", fg="black", font=("Arial",12,"bold"), width=20, command=self.create_account)
        addButton.grid(row=6, column=0, padx=10, columnspan=2, pady=5)


    

    def create_account(self):
        self.clear_frame()
        self.clear_inputs()

        label = tk.Label(self.root, background="black", bd=3, foreground="white", relief="groove", text="Create User Account", font=("Arial",20,"bold"))
        label.pack(side="top", fill="x")

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        entryFrame = ttk.Frame(self.root)
        entryFrame.pack(pady=10)

        nameLabel = ttk.Label(entryFrame, text="User Name", font=("Arial",12))
        nameLabel.grid(row=0, column=0, padx=5)

        self.nameEntry = ttk.Entry(entryFrame, textvariable=self.username, font=("Arial",12))
        self.nameEntry.grid(row=0, column=1)

        accLabel = ttk.Label(entryFrame, text="Account Number", font=("Arial",12))
        accLabel.grid(row=1, column=0, padx=5)

        self.accEntry = ttk.Entry(entryFrame, textvariable=self.acEntry, font=("Arial",12))
        self.accEntry.grid(row=1, column=1)

        pin1Label = ttk.Label(entryFrame, text="PIN", font=("Arial",12))
        pin1Label.grid(row=2, column=0, padx=5)

        self.pin1Entry = ttk.Entry(entryFrame, textvariable=self.pin, font=("Arial",12), show="*")
        self.pin1Entry.grid(row=2, column=1)

        cpinLabel = ttk.Label(entryFrame, text="Confirm PIN", font=("Arial",12))
        cpinLabel.grid(row=3, column=0, padx=5)

        self.cpinEntry = ttk.Entry(entryFrame, textvariable=self.cpin, font=("Arial",12), show="*")
        self.cpinEntry.grid(row=3, column=1)

        addButton = tk.Button(entryFrame, text="Create Account", bg="gray", relief="groove", fg="black", font=("Arial",12,"bold"), width=22, command=self.create_ac)
        addButton.grid(row=5, column=0, padx=10, columnspan=2, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    obj = atm(root)
    root.mainloop()
