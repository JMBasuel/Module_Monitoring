import tkinter as tk
from tkinter import ttk
from distribution import Distribution
from inventory import Inventory
import datafunc

class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Module Monitoring')
        self.root.resizable(False, False)
        self.center_window(300, 150)

        datafunc.read_data()
        datafunc.read_data_backup()

        self.frame = tk.Frame(self.root, pady=15, padx=20, bg='#F6F6F6')
        self.mod_inv = ttk.Button(self.frame, text='Module Monitoring', command=self.open_inventory)
        self.mod_dist = ttk.Button(self.frame, text='Module Distribution', command=self.open_distribution)

        self.mod_inv.pack(pady=5, expand=True, fill='both')
        self.mod_dist.pack(pady=5, expand=True, fill='both')
        self.frame.pack(expand=True, fill='both')

        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.mainloop()

    def open_inventory(self):
        Inventory(self.root)

    def open_distribution(self):
        Distribution(self.root)

    def center_window(self, width, height):
        x_coordinate = (self.root.winfo_screenwidth() - width) // 2
        y_coordinate = (self.root.winfo_screenheight() - height) // 3
        self.root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def on_close(self):
        datafunc.write_data()
        datafunc.write_data_backup()
        self.root.destroy()


if __name__ == '__main__':
    Main()
