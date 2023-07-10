import tkinter as tk
from tkinter import ttk
import requests

# Function to fetch news headlines
def fetch_news():
    # API endpoint for news headlines
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",  # Change country code if desired
        "apiKey": "8159deac475a418596050f8f7dabfb2d"  # Replace with your News API key
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Clear any previous news headlines
    news_box.delete(1.0, tk.END)

    # Display news headlines in the text box
    for article in data['articles']:
        title = article['title']
        news_box.insert(tk.END, f"- {title}\n")

# Create the main window
root = tk.Tk()
root.title("News App")

# Create a text box to display news headlines
news_box = tk.Text(root, width=50, height=10)
news_box.pack(pady=10)

# Create a button to fetch news headlines
fetch_button = ttk.Button(root, text="Fetch News", command=fetch_news)
fetch_button.pack()

# Start the application
root.mainloop()
