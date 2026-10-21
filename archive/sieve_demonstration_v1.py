import tkinter as tk
import math
from tkinter import font



def make_grid(width, amount):
    # def color_cell(num, color):
    #     labels[num].config(bg=color)
    #     root.update_idletasks() // didn't need this function. I did it in sieves() instead.

    paned_main = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_main.pack(fill="both", expand="yes")

    left_frame = tk.Frame(paned_main)
    right_frame = tk.Frame(paned_main)

    paned_main.add(left_frame)
    paned_main.add(right_frame)

    labels = {}
    for num in range(2, amount+1):
        labels[num] = tk.Button(left_frame, text=str(num), activebackground="lightgray", activeforeground="black", width=5, height=2)

    for i, num in enumerate(range(2, amount+1)):
        row = i // width
        col = i % width
        labels[num].grid(row=row, column=col)

    root.update()  # Ensure the window appears before animation starts

    text_widget = tk.Text(right_frame, height=4, width=20)
    text_widget.pack(fill=tk.BOTH, expand=True)

    def on_sieve_done(Prime_boolians):
        primes = []
        text_widget.insert(tk.END, "Confirmed Primes:\n")
        for num in range(2, amount+1):
            if Prime_boolians[num-2]:
                primes.append(str(num))
        for item in primes:
            text_widget.insert(tk.END, item + "\n")

        def turn_green(i):
            if i >= len(primes):
                return
            labels[int(primes[i])].config(bg="green")
            root.update_idletasks()
            root.after(200, lambda: turn_green(i + 1))
        turn_green(0)

    sieves(amount, labels, on_sieve_done)




def sieves(amount, labels, callback):
    A = [True] * (amount+1)
    A[0] = False
    A[1] = False

    def next_i(i):
        if i > int(math.sqrt(amount)):
            callback(A[2:])
            return
        if A[i]:
            labels[i].config(bg="green")
            root.update_idletasks()
            def next_j(j):
                if j > amount:
                    root.after(100, lambda: next_i(i + 1))
                    return
                A[j] = False
                labels[j].config(bg="red")
                labels[j].config(font=strikethrough_font, fg='gray')
                root.update_idletasks()
                root.after(100, lambda: next_j(j + i))
            root.after(100, lambda: next_j(i * i))
            
        else:
            root.after(100, lambda: next_i(i + 1))
    
    root.after(100, lambda: next_i(2))

root = tk.Tk()
root.geometry("600x400")
root.title("Prime Number Sieve Visualization with Confirmed Primes")

strikethrough_font = font.Font(overstrike=1)  # overstrike=1 means strikethrough

try:
    width = int(input('Enter a width for the grid: '))
    amount = int(input('Enter an upper limit: '))
    if width <= 0 or amount < 1:
        raise ValueError("Width must be a positive integer and amount must be at least 1.")
except ValueError as e:
    print(f"Invalid input: {e}. Using defaults (width=5, amount=25).")
    width, amount = 5, 25


make_grid(width, amount)

root.mainloop()
