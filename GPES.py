import numpy as np
from prettytable import PrettyTable

class Split:
    def __init__(self, names):
        self.names = names
        self.n = len(names)
        self.net = np.zeros(self.n)          # positive = will receive, negative = owes
        self.expenses = []                   # store each expense with description

    def add(self, payer, amount, description, *involved):
        
        if not involved:
            involved = self.names

        share = amount / len(involved)
        payer_idx = self.names.index(payer)


        self.net[payer_idx] += amount - share
        for p in involved:
            if p == payer:
                continue
            idx = self.names.index(p)
            self.net[idx] -= share

        self.expenses.append({
            'payer': payer,
            'amount': amount,
            'description': description,
            'involved': list(involved),
            'share_per_person': share
        })

        # Display shared amount information
        print(f"\nExpense added: {description}")
        print(f"   Paid by {payer}: ₹{amount:.2f}")
        print(f"   Shared among {len(involved)} people → ₹{share:.2f} each")
        if involved != self.names:
            print(f"   (Only: {', '.join(involved)})")
        print()

    def summary(self):
        """Show net balances for all users."""
        t = PrettyTable(["Person", "Net Balance (₹)"])
        for name, val in zip(self.names, self.net):
            t.add_row([name, round(val, 2)])
        print("\n Summary of balances:")
        print(t)
        print("   + = will receive money, - = owes money\n")

    def settle(self):
        #Suggest minimal cash settlements.
        t = PrettyTable(["From (owes)", "To (receives)", "Amount (₹)"])
        pos = [(i, self.net[i]) for i in range(self.n) if self.net[i] > 0]
        neg = [(i, -self.net[i]) for i in range(self.n) if self.net[i] < 0]

        i = j = 0
        while i < len(pos) and j < len(neg):
            amt = min(pos[i][1], neg[j][1])
            t.add_row([self.names[neg[j][0]], self.names[pos[i][0]], round(amt, 2)])
            pos[i] = (pos[i][0], pos[i][1] - amt)
            neg[j] = (neg[j][0], neg[j][1] - amt)
            if pos[i][1] < 1e-9:
                i += 1
            if neg[j][1] < 1e-9:
                j += 1

        print("\n Suggested settlements:")
        print(t)

    def show_expenses(self):
        #list all recorded expenses
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        t = PrettyTable(["Payer", "Amount (₹)", "Description", "Shared among"])
        for e in self.expenses:
            t.add_row([
                e['payer'],
                round(e['amount'], 2),
                e['description'],
                ', '.join(e['involved'])
            ])
        print("\n Expense history:")
        print(t)


#example
if __name__ == "__main__":
    group = Split(["Alice", "Bob", "Ravi", "Harsha"])

    group.add("Alice", 1200, "Dinner at restaurant")                     # everyone shares
    group.add("Bob", 600, "Movie tickets", "Bob", "Ravi")             # only Bob & Ravi
    group.add("Ravi", 900, "Groceries")                               # everyone
    group.add("Harsha", 400, "Taxi ride", "Alice", "Bob", "Harsha")        # three people

    # Show summary and settlements
    group.summary()
    group.settle()

    # to show all expenses
    group.show_expenses()
