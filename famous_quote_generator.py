import tkinter as tk
import requests
import random
from threading import Thread
import os
from dotenv import load_dotenv

api = "https://api.api-ninjas.com/v1/quotes"

# Lade die Umgebungsvariablen aus der .env Datei
load_dotenv()

# Hole den API-Key aus der Umgebungsvariable
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API Key nicht gefunden! Bitte in .env Datei setzen.")

quotes = []

window = tk.Tk()
window.geometry("900x300")
window.title("Quote Generator")
window.grid_columnconfigure(0, weight=1)
window.resizable(False, False)
window.configure(bg="grey")


def preload_quotes():
    global quotes
    headers = {"X-Api-Key": api_key}

    for _ in range(10):
        try:
            response = requests.get(api, headers=headers)
            response.raise_for_status()
            random_quote = response.json()
            if isinstance(random_quote, list) and random_quote:
                quote_data = random_quote[0]
                content = quote_data.get("quote")
                author = quote_data.get("author")
                if content and author:
                    quote = f"{content}\n\nBy {author}"
                    quotes.append(quote)
        except Exception:
            pass


def get_random_quote():
    if quotes:
        quote = random.choice(quotes)
        quote_label.config(text=quote)
    else:
        quote_label.config(text="Keine Zitate verfügbar.")


def start_loading_quotes():
    thread = Thread(target=preload_quotes)
    thread.daemon = True
    thread.start()


quote_label = tk.Label(
    window,
    text="Click on the Button to generate a random quote!",
    height=6,
    pady=10,
    wraplength=800,
    font=("Helvetica", 14),
)
quote_label.grid(row=0, column=0, sticky="WE", padx=20, pady=10)

button = tk.Button(
    window,
    text="Generate",
    command=get_random_quote,
    bg="#0052cc",
    fg="#ffffff",
    activebackground="grey",
    font=("Helvetica", 14),
)
button.grid(row=1, column=0, sticky="WE", padx=20, pady=10)

if __name__ == "__main__":
    start_loading_quotes()
    window.mainloop()
