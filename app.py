import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pyshorteners


class URLShortener:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x230')
        self.root.title('URL Shortener')
        self.root.configure(bg="white")

        # Title
        tk.Label(self.root,
                 text="URL Shortener",
                 font=('verdana', 16, 'bold'),
                 bg="white",
                 fg="purple").place(x=160, y=5)

        # Date
        tk.Label(self.root,
                 text=datetime.now().strftime("%Y-%m-%d"),
                 font=('verdana', 9, 'bold'),
                 bg="white",
                 fg="purple").place(x=380, y=5)

        # URL Label
        tk.Label(self.root,
                 text="Paste Your URL Here:",
                 font=('verdana', 10, 'bold'),
                 bg="white",
                 fg="purple").place(x=50, y=50)

        # URL Entry
        self.url_entry = tk.Entry(self.root,
                                  width=55,
                                  bg="lightgrey",
                                  relief=tk.GROOVE,
                                  borderwidth=2)
        self.url_entry.place(x=50, y=80)

        # Create Button
        tk.Button(self.root,
                  text="Create",
                  font=('verdana', 9, 'bold'),
                  bg="purple",
                  fg="white",
                  width=10,
                  command=self.create_short_url).place(x=380, y=77)

        # Short URL Label
        tk.Label(self.root,
                 text="Shortened URL:",
                 font=('verdana', 10, 'bold'),
                 bg="white",
                 fg="purple").place(x=50, y=120)

        # Output Entry
        self.output_entry = tk.Entry(self.root,
                                     width=55,
                                     fg="purple",
                                     relief=tk.GROOVE,
                                     borderwidth=2)
        self.output_entry.place(x=50, y=150)

        # Copy Button
        tk.Button(self.root,
                  text="Copy",
                  font=('verdana', 9, 'bold'),
                  bg="purple",
                  fg="white",
                  width=10,
                  command=self.copy_to_clipboard).place(x=380, y=147)

        self.root.mainloop()

    def create_short_url(self):
        long_url = self.url_entry.get().strip()

        if not long_url:
            messagebox.showerror("Error", "Please paste a URL")
            return

        try:
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(long_url)

            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, short_url)

        except Exception:
            messagebox.showerror("Error",
                                 "Failed to shorten URL.\nCheck Internet Connection.")

    def copy_to_clipboard(self):
        short_url = self.output_entry.get()
        if short_url:
            self.root.clipboard_clear()
            self.root.clipboard_append(short_url)
            messagebox.showinfo("Copied", "Short URL copied to clipboard!")
        else:
            messagebox.showerror("Error", "No URL to copy.")


if __name__ == "__main__":
    URLShortener()
