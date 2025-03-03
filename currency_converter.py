import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from datetime import datetime, timedelta
import json

class EnhancedCurrencyConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Currency Converter")
        self.master.geometry("1000x700")
        self.master.minsize(800, 600)
        self.master.configure(bg="#2c3e50")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", foreground="#ecf0f1", background="#2c3e50", font=("Helvetica", 10))
        self.style.configure("TButton", foreground="#ecf0f1", background="#3498db", font=("Helvetica", 10))
        self.style.map("TButton", background=[('active', '#2980b9')])
        self.style.configure("TEntry", foreground="#2c3e50", font=("Helvetica", 10))
        self.style.configure("Treeview", foreground="#2c3e50", background="#ecf0f1", fieldbackground="#ecf0f1")
        self.style.map('Treeview', background=[('selected', '#3498db')])
        self.style.configure("TLabelframe", foreground="#ecf0f1", background="#34495e")
        self.style.configure("TLabelframe.Label", foreground="#ecf0f1", background="#34495e", font=("Helvetica", 12, "bold"))

        self.currencies = self.fetch_currencies()
        self.conversion_history = []
        self.favorite_conversions = []

        self.setup_ui()

    def fetch_currencies(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            return list(data['rates'].keys())
        except:
            messagebox.showerror("Error", "Failed to fetch currencies. Using default list.")
            return ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "SEK", "NZD"]

    def setup_ui(self):
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.master, padding="10", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Converter frame
        converter_frame = ttk.LabelFrame(main_frame, text="Currency Converter", padding="10", style="TLabelframe")
        converter_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        converter_frame.columnconfigure(1, weight=1)

        ttk.Label(converter_frame, text="From Currency:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.from_currency = ttk.Combobox(converter_frame, values=self.currencies, width=15)
        self.from_currency.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.from_currency.set("USD")

        ttk.Label(converter_frame, text="To Currency:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.to_currency = ttk.Combobox(converter_frame, values=self.currencies, width=15)
        self.to_currency.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.to_currency.set("EUR")

        ttk.Label(converter_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.amount = ttk.Entry(converter_frame)
        self.amount.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.amount.insert(0, "1")

        button_frame = ttk.Frame(converter_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        convert_button = ttk.Button(button_frame, text="Convert", command=self.convert)
        convert_button.grid(row=0, column=0, padx=5)

        swap_button = ttk.Button(button_frame, text="Swap Currencies", command=self.swap_currencies)
        swap_button.grid(row=0, column=1, padx=5)

        self.result_var = tk.StringVar()
        result_label = ttk.Label(converter_frame, textvariable=self.result_var, font=("Helvetica", 12, "bold"))
        result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Favorite conversions
        favorite_frame = ttk.LabelFrame(main_frame, text="Favorite Conversions", padding="10", style="TLabelframe")
        favorite_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        favorite_frame.columnconfigure(0, weight=1)
        favorite_frame.rowconfigure(0, weight=1)

        self.favorite_listbox = tk.Listbox(favorite_frame, bg="#ecf0f1", fg="#2c3e50")
        self.favorite_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=5)

        favorite_button_frame = ttk.Frame(favorite_frame)
        favorite_button_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        favorite_button_frame.columnconfigure(0, weight=1)
        favorite_button_frame.columnconfigure(1, weight=1)

        add_favorite_button = ttk.Button(favorite_button_frame, text="Add to Favorites", command=self.add_to_favorites)
        add_favorite_button.grid(row=0, column=0, padx=2, pady=5, sticky="ew")

        remove_favorite_button = ttk.Button(favorite_button_frame, text="Remove Favorite", command=self.remove_favorite)
        remove_favorite_button.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

        # Conversion history
        history_frame = ttk.LabelFrame(main_frame, text="Conversion History", padding="10", style="TLabelframe")
        history_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        self.history_tree = ttk.Treeview(history_frame, columns=("timestamp", "conversion", "result"), show="headings", height=5)
        self.history_tree.heading("timestamp", text="Timestamp")
        self.history_tree.heading("conversion", text="Conversion")
        self.history_tree.heading("result", text="Result")
        self.history_tree.column("timestamp", width=150)
        self.history_tree.column("conversion", width=200)
        self.history_tree.column("result", width=150)
        self.history_tree.grid(row=0, column=0, sticky="nsew")

        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        history_scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)

        # Rate alert
        self.alert_var = tk.StringVar()
        alert_label = ttk.Label(main_frame, textvariable=self.alert_var, font=("Helvetica", 10, "italic"))
        alert_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Graph
        graph_frame = ttk.Frame(main_frame)
        graph_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.load_favorites()
        self.update_graph("USD", "EUR")

    def convert(self):
        try:
            amount = float(self.amount.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url)
            data = response.json()
            rate = data['rates'][to_curr]

            result = amount * rate
            self.result_var.set(f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}")

            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_entry = (timestamp, f"{amount:.2f} {from_curr} to {to_curr}", f"{result:.2f} {to_curr}")
            self.history_tree.insert("", 0, values=history_entry)

            # Simulate rate alert
            self.simulate_rate_alert()

            # Update graph
            self.update_graph(from_curr, to_curr)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except KeyError:
            messagebox.showerror("Error", "Invalid currency selection")
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch exchange rate")

    def swap_currencies(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)

    def simulate_rate_alert(self):
        if random.random() < 0.2:  # 20% chance of alert
            change = random.uniform(-0.05, 0.05)
            alert_message = f"Alert: {self.from_currency.get()}/{self.to_currency.get()} rate changed by {change:.2%}"
            self.alert_var.set(alert_message)
        else:
            self.alert_var.set("")

    def update_graph(self, from_curr, to_curr):
        # Simulate historical data
        dates = [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)]
        rates = [random.uniform(0.8, 1.2) for _ in range(7)]

        self.ax.clear()
        self.ax.plot(dates, rates, color='#3498db')
        self.ax.set_title(f"{from_curr}/{to_curr} Exchange Rate Trend", color='#ecf0f1')
        self.ax.set_xlabel("Date", color='#ecf0f1')
        self.ax.set_ylabel("Exchange Rate", color='#ecf0f1')
        self.ax.tick_params(axis='x', rotation=45, colors='#ecf0f1')
        self.ax.tick_params(axis='y', colors='#ecf0f1')
        self.ax.set_facecolor('#2c3e50')
        self.figure.patch.set_facecolor('#2c3e50')
        self.figure.tight_layout()
        self.canvas.draw()

    def add_to_favorites(self):
        favorite = f"{self.from_currency.get()} to {self.to_currency.get()}"
        if favorite not in self.favorite_conversions:
            self.favorite_conversions.append(favorite)
            self.favorite_listbox.insert(tk.END, favorite)
            self.save_favorites()

    def remove_favorite(self):
        selection = self.favorite_listbox.curselection()
        if selection:
            index = selection[0]
            favorite = self.favorite_listbox.get(index)
            self.favorite_listbox.delete(index)
            self.favorite_conversions.remove(favorite)
            self.save_favorites()

    def save_favorites(self):
        with open("favorites.json", "w") as f:
            json.dump(self.favorite_conversions, f)

    def load_favorites(self):
        try:
            with open("favorites.json", "r") as f:
                self.favorite_conversions = json.load(f)
                for favorite in self.favorite_conversions:
                    self.favorite_listbox.insert(tk.END, favorite)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedCurrencyConverter(root)
    root.mainloop()

