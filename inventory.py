import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import datafunc

class Inventory:
    def __init__(self, master):
        self.distribution_data = None
        self.file_path = None
        self.prev = None
        self.size = None
        self.distribution_table = None
        self.inventory_data = None
        self.inventory_table = None
        self.show_inventory = False
        self.top = tk.Toplevel(master)
        self.top.title('Monitoring')
        self.center_window(900, 650)

        self.master = master
        self.master.withdraw()

        self.style = ttk.Style(self.top)
        self.style.configure('top.TButton', font=('Segoe UI', 12))
        self.style.configure('mid.TButton', font=('Segoe UI', 10))
        self.style.configure('bot.TButton', font=('Segoe UI', 8))
        self.style.configure('Treeview', rowheight=25, font=('Segoe UI', 8))
        self.style.map('Treeview', background=[('selected', '#D2D2D2')], foreground=[('selected', '#000000')])

        self.main_frame = tk.Frame(self.top, padx=5, bg='#F6F6F6')

        self.menu_frame = tk.Frame(self.main_frame, width=150, padx=10, pady=10, bg='#D2D2D2')
        self.dash_label = ttk.Label(self.menu_frame, text='MONITORING', padding=(11, 9),
                                    font=('Segoe UI', 14, 'bold'), background='#C4C4C4')
        self.menus_frame = tk.Frame(self.menu_frame, bg='#D2D2D2')
        self.inventory = ttk.Button(self.menus_frame, style='top.TButton', text='INVENTORY',
                                    takefocus=0, command=self.inventory)
        self.distribution = ttk.Button(self.menus_frame, style='top.TButton', text='DISTRIBUTION',
                                       takefocus=0, command=self.distribution)

        self.dash_frame = tk.Frame(self.main_frame, bg='#F6F6F6')

        self.nav_frame = tk.Frame(self.dash_frame, height=50, padx=10, pady=10, bg='#D2D2D2')
        self.nav_label = ttk.Label(self.nav_frame, text='Monitoring >> Inventory', font=('Segoe UI', 14),
                                   foreground='#515151', background='#D2D2D2')
        self.inventory_to_excel = ttk.Button(self.nav_frame, text='MODULE INVENTORY TO EXCEL', style='mid.TButton',
                                             takefocus=0, command=self.inventory_to_excel)
        self.student_to_excel = ttk.Button(self.nav_frame, text='DISTRIBUTION DATA TO EXCEL', style='mid.TButton',
                                           takefocus=0, command=self.student_to_excel)

        # INVENTORY
        self.inventory_manager_frame = tk.Frame(self.menus_frame, bg='#D2D2D2')
        self.add_new_inventory = ttk.Button(self.inventory_manager_frame, text='ADD NEW', style='mid.TButton',
                                            takefocus=0, command=self.add_new_inventory)
        self.modify_inventory = ttk.Button(self.inventory_manager_frame, text='MODIFY', takefocus=0,
                                           style='mid.TButton', command=self.modify_inventory)
        self.add_inventory = ttk.Button(self.inventory_manager_frame, text='ADD QUANTITY', takefocus=0,
                                        style='mid.TButton', command=self.add_inventory)
        self.delete_inventory = ttk.Button(self.inventory_manager_frame, text='DELETE', takefocus=0,
                                           style='mid.TButton', command=self.delete_inventory)
        self.clear_inventory = ttk.Button(self.inventory_manager_frame, text='CLEAR DATA', takefocus=0,
                                          style='mid.TButton', command=self.clear_inventory_data)
        self.restore_inventory = ttk.Button(self.inventory_manager_frame, text='RESTORE', takefocus=0,
                                            style='mid.TButton', command=self.restore_inventory_data)

        # ADD NEW INVENTORY
        self.add_new_inventory_frame = tk.Frame(self.inventory_manager_frame, bg='#D2D2D2')
        self.add_new_pen_code = tk.StringVar()
        self.add_new_pen_code_text = ttk.Label(self.add_new_inventory_frame, text='NEW PEN CODE',
                                               font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.add_new_pen_code_box = ttk.Entry(self.add_new_inventory_frame, textvariable=self.add_new_pen_code,
                                              font=('Segoe UI', 11), justify='center')
        self.add_new_pen_code_box.bind('<KeyPress>', self.shortcut)
        self.add_new_title = tk.StringVar()
        self.add_new_title_text = ttk.Label(self.add_new_inventory_frame, text='NEW SUBJECT TITLE',
                                            font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.add_new_title_box = ttk.Entry(self.add_new_inventory_frame, textvariable=self.add_new_title,
                                           font=('Segoe UI', 11), justify='center')
        self.add_new_title_box.bind('<KeyPress>', self.shortcut)
        self.add_new_quantity = tk.StringVar()
        self.add_new_quantity_text = ttk.Label(self.add_new_inventory_frame, text='QUANTITY',
                                               font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.add_new_quantity_box = ttk.Entry(self.add_new_inventory_frame, textvariable=self.add_new_quantity,
                                              font=('Segoe UI', 11), justify='center')
        self.add_new_quantity_box.bind('<KeyPress>', self.shortcut)
        self.add_new_inventory_data = ttk.Button(self.add_new_inventory_frame, text='ADD NEW', takefocus=0,
                                                 style='bot.TButton', command=self.add_new_inventory_data)

        # MODIFY INVENTORY
        self.modify_inventory_frame = tk.Frame(self.inventory_manager_frame, bg='#D2D2D2')
        self.modify_pen_code = tk.StringVar()
        self.modify_pen_code_text = ttk.Label(self.modify_inventory_frame, text='OLD / NEW PEN CODE',
                                              font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.modify_pen_code_box = ttk.Entry(self.modify_inventory_frame, textvariable=self.modify_pen_code,
                                             font=('Segoe UI', 11), justify='center')
        self.modify_pen_code_box.bind('<KeyPress>', self.shortcut)
        self.modify_title = tk.StringVar()
        self.modify_title_text = ttk.Label(self.modify_inventory_frame, text='OLD / NEW SUBJECT TITLE',
                                           font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.modify_title_box = ttk.Entry(self.modify_inventory_frame, textvariable=self.modify_title,
                                          font=('Segoe UI', 11), justify='center')
        self.modify_title_box.bind('<KeyPress>', self.shortcut)
        self.modify_quantity = tk.StringVar()
        self.modify_quantity_text = ttk.Label(self.modify_inventory_frame, text='OLD / NEW QUANTITY',
                                              font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.modify_quantity_box = ttk.Entry(self.modify_inventory_frame, textvariable=self.modify_quantity,
                                             font=('Segoe UI', 11), justify='center')
        self.modify_quantity_box.bind('<KeyPress>', self.shortcut)
        self.modify_inventory_data = ttk.Button(self.modify_inventory_frame, text='MODIFY', takefocus=0,
                                                style='bot.TButton', command=self.modify_inventory_data)

        # ADD INVENTORY
        self.add_inventory_frame = tk.Frame(self.inventory_manager_frame, bg='#D2D2D2')
        self.add_pen_code = tk.StringVar()
        self.add_pen_code_text = ttk.Label(self.add_inventory_frame, text='PEN CODE',
                                           font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.add_pen_code_box = ttk.Entry(self.add_inventory_frame, textvariable=self.add_pen_code,
                                          font=('Segoe UI', 11), justify='center')
        self.add_pen_code_box.bind('<KeyPress>', self.shortcut)
        self.add_quantity = tk.StringVar()
        self.add_quantity_text = ttk.Label(self.add_inventory_frame, text='QUANTITY TO ADD',
                                           font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.add_quantity_box = ttk.Entry(self.add_inventory_frame, textvariable=self.add_quantity,
                                          font=('Segoe UI', 11), justify='center')
        self.add_quantity_box.bind('<KeyPress>', self.shortcut)
        self.add_inventory_data = ttk.Button(self.add_inventory_frame, text='ADD', takefocus=0, style='bot.TButton',
                                             command=self.add_inventory_data)

        # DELETE INVENTORY
        self.delete_inventory_frame = tk.Frame(self.inventory_manager_frame, bg='#D2D2D2')
        self.delete_pen_code = tk.StringVar()
        self.delete_pen_code_text = ttk.Label(self.delete_inventory_frame, text='PEN CODE',
                                              font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.delete_pen_code_box = ttk.Entry(self.delete_inventory_frame, textvariable=self.delete_pen_code,
                                             font=('Segoe UI', 11), justify='center')
        self.delete_pen_code_box.bind('<KeyPress>', self.shortcut)
        self.delete_inventory_data = ttk.Button(self.delete_inventory_frame, text='DELETE', takefocus=0,
                                                style='bot.TButton', command=self.delete_inventory_data)

        # DISTRIBUTION
        self.distribution_manager_frame = tk.Frame(self.menus_frame, bg='#D2D2D2')
        self.filter_distribution = ttk.Button(self.distribution_manager_frame, text='FILTER', style='mid.TButton',
                                              takefocus=0, command=self.filter_distribution)
        self.modify_distribution = ttk.Button(self.distribution_manager_frame, text='MODIFY', style='mid.TButton',
                                              takefocus=0, command=self.modify_distribution)
        self.delete_data = ttk.Button(self.distribution_manager_frame, text='DELETE',
                                      style='mid.TButton', takefocus=0, command=self.delete_distribution)
        self.clear_distribution = ttk.Button(self.distribution_manager_frame, text='CLEAR DATA',
                                             style='mid.TButton', takefocus=0, command=self.clear_distribution_data)
        self.restore_distribution = ttk.Button(self.distribution_manager_frame, text='RESTORE',
                                               style='mid.TButton', takefocus=0, command=self.restore_distribution_data)

        # FILTER DISTRIBUTION
        self.filter_distribution_frame = tk.Frame(self.distribution_manager_frame, height=300, bg='#D2D2D2')
        self.filter_keyword = tk.StringVar()
        self.filter_keyword_text = ttk.Label(self.filter_distribution_frame, text='KEYWORD',
                                             font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.filter_keyword_box = ttk.Entry(self.filter_distribution_frame, textvariable=self.filter_keyword,
                                            font=('Segoe UI', 11), justify='center')
        self.filter_keyword_box.bind('<KeyPress>', self.shortcut)
        self.filter_distribution_data = ttk.Button(self.filter_distribution_frame, text='FILTER', takefocus=0,
                                                   style='bot.TButton', command=self.filter_distribution_data)
        self.remove_distribution_data_filter = ttk.Button(self.filter_distribution_frame, text='REMOVE FILTER',
                                                          takefocus=0, style='bot.TButton',
                                                          command=self.remove_distribution_data_filter)

        # MODIFY DISTRIBUTION
        self.modify_distribution_frame = tk.Frame(self.distribution_manager_frame, height=300, bg='#D2D2D2')
        self.modify_course = tk.StringVar()
        self.modify_course_text = ttk.Label(self.modify_distribution_frame, text='OLD / NEW COURSE',
                                            font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.modify_course_box = ttk.Entry(self.modify_distribution_frame, textvariable=self.modify_course,
                                           font=('Segoe UI', 11), justify='center')
        self.modify_course_box.bind('<KeyPress>', self.shortcut)
        self.modify_id = tk.StringVar()
        self.modify_id_text = ttk.Label(self.modify_distribution_frame, text='OLD / NEW STUDENT ID',
                                        font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.modify_id_box = ttk.Entry(self.modify_distribution_frame, textvariable=self.modify_id,
                                       font=('Segoe UI', 11), justify='center')
        self.modify_id_box.bind('<KeyPress>', self.shortcut)
        self.modify_name = tk.StringVar()
        self.modify_name_text = ttk.Label(self.modify_distribution_frame, text='OLD / NEW STUDENT NAME',
                                          font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.modify_name_box = ttk.Entry(self.modify_distribution_frame, textvariable=self.modify_name,
                                         font=('Segoe UI', 11), justify='center')
        self.modify_name_box.bind('<KeyPress>', self.shortcut)
        self.modify_distribution_data = ttk.Button(self.modify_distribution_frame, text='MODIFY', takefocus=0,
                                                   style='bot.TButton', command=self.modify_distribution_data)

        # DELETE DISTRIBUTION
        self.delete_distribution_frame = tk.Frame(self.distribution_manager_frame, height=300, bg='#D2D2D2')
        self.delete_keyword = tk.StringVar()
        self.delete_keyword_text = ttk.Label(self.delete_distribution_frame, text='COURSE / ID',
                                             font=('Segoe UI', 7, 'bold'), background='#D2D2D2')
        self.delete_keyword_box = ttk.Entry(self.delete_distribution_frame, textvariable=self.delete_keyword,
                                            font=('Segoe UI', 11), justify='center')
        self.delete_keyword_box.bind('<KeyPress>', self.shortcut)
        self.delete_distribution_data = ttk.Button(self.delete_distribution_frame, text='DELETE', takefocus=0,
                                                   style='bot.TButton', command=self.delete_distribution_data)

        self.inventory_frame = tk.Frame(self.dash_frame, bg='#DADADA')
        self.distribution_frame = tk.Frame(self.dash_frame, bg='#DADADA')

        # INVENTORY TABLE
        inventory_columns = ('PEN CODE', 'SUBJECT TITLE', 'QUANTITY')
        self.inventory_table = ttk.Treeview(self.inventory_frame, columns=inventory_columns, show='headings')
        self.inventory_table.tag_configure('hover', background='#EEEEEE')
        self.inventory_table.bind("<Motion>", self.hover)
        self.inventory_table.configure(selectmode='none')
        for col in inventory_columns:
            self.inventory_table.heading(col, text=col, anchor='center')
            if col == 'SUBJECT TITLE':
                self.inventory_table.column(col, anchor='center', width=400, minwidth=400)
            else:
                self.inventory_table.column(col, anchor='center', width=100, minwidth=100)
        self.update_inventory_table()

        # DISTRIBUTION TABLE
        distribution_columns = ('ITEM', 'COURSE', 'STUDENT ID', 'STUDENT NAME', 'STATUS', 'DATE')
        self.distribution_table = ttk.Treeview(self.distribution_frame, columns=distribution_columns, show='headings')
        self.distribution_table.tag_configure('hover', background='#EEEEEE')
        self.distribution_table.bind("<Motion>", self.hover)
        self.distribution_table.bind('<<TreeviewSelect>>', self.toggle_row)
        self.size = 40
        for col in distribution_columns:
            self.distribution_table.heading(col, text=col, anchor='center')
            if any(col == val for val in ('ITEM', 'DATE')):
                self.distribution_table.column(col, anchor='center', width=90, minwidth=90)
            elif any(col == val for val in ('COURSE', 'STUDENT ID')):
                self.distribution_table.column(col, anchor='center', width=40 + self.size, minwidth=40 + self.size)
                self.size += 20
            elif col == 'STATUS':
                self.distribution_table.column(col, anchor='w', width=120, minwidth=120)
            else:
                self.distribution_table.column(col, anchor='center', width=200, minwidth=200)
        self.update_distribution_table(False)

        self.dash_label.place(x=-10, y=-10)
        self.inventory.pack(fill='x', pady=5)
        self.distribution.pack(fill='x', pady=5)

        # INVENTORY
        self.add_new_inventory.pack(fill='x', pady=5)
        self.modify_inventory.pack(fill='x', pady=5)
        self.add_inventory.pack(fill='x', pady=5)
        self.delete_inventory.pack(fill='x', pady=5)
        self.clear_inventory.pack(fill='x', pady=5)
        self.restore_inventory.pack(fill='x', pady=5)
        self.inventory_manager_frame.pack(expand=True, fill='both', pady=20)

        # ADD NEW INVENTORY
        self.add_new_pen_code_text.pack(anchor='nw', pady=5)
        self.add_new_pen_code_box.pack(fill='x')
        self.add_new_title_text.pack(anchor='nw', pady=5)
        self.add_new_title_box.pack(fill='x')
        self.add_new_quantity_text.pack(anchor='nw', pady=5)
        self.add_new_quantity_box.pack(fill='x')
        self.add_new_inventory_data.pack(fill='x', pady=20)

        # MODIFY INVENTORY
        self.modify_pen_code_text.pack(anchor='nw', pady=5)
        self.modify_pen_code_box.pack(fill='x')
        self.modify_title_text.pack(anchor='nw', pady=5)
        self.modify_title_box.pack(fill='x')
        self.modify_quantity_text.pack(anchor='nw', pady=5)
        self.modify_quantity_box.pack(fill='x')
        self.modify_inventory_data.pack(fill='x', pady=20)

        # ADD INVENTORY
        self.add_pen_code_text.pack(anchor='nw', pady=5)
        self.add_pen_code_box.pack(fill='x')
        self.add_quantity_text.pack(anchor='nw', pady=5)
        self.add_quantity_box.pack(fill='x')
        self.add_inventory_data.pack(fill='x', pady=20)

        # DELETE INVENTORY
        self.delete_pen_code_text.pack(anchor='nw', pady=5)
        self.delete_pen_code_box.pack(fill='x')
        self.delete_inventory_data.pack(fill='x', pady=20)

        # DISTRIBUTION
        self.filter_distribution.pack(fill='x', pady=5)
        self.modify_distribution.pack(fill='x', pady=5)
        self.delete_data.pack(fill='x', pady=5)
        self.clear_distribution.pack(fill='x', pady=5)
        self.restore_distribution.pack(fill='x', pady=5)

        # FILTER DISTRIBUTION
        self.filter_keyword_text.pack(anchor='nw', pady=5)
        self.filter_keyword_box.pack(fill='x')
        self.filter_distribution_data.pack(fill='x', pady=20)

        # MODIFY DISTRIBUTION
        self.modify_course_text.pack(anchor='nw', pady=5)
        self.modify_course_box.pack(fill='x')
        self.modify_id_text.pack(anchor='nw', pady=5)
        self.modify_id_box.pack(fill='x')
        self.modify_name_text.pack(anchor='nw', pady=5)
        self.modify_name_box.pack(fill='x')
        self.modify_distribution_data.pack(fill='x', pady=20)

        # DELETE DISTRIBUTION
        self.delete_keyword_text.pack(anchor='nw', pady=5)
        self.delete_keyword_box.pack(fill='x')
        self.delete_distribution_data.pack(fill='x', pady=20)

        # MENU
        self.menus_frame.place(x=0, y=50, width=130, relheight=0.92)
        self.menu_frame.pack(side="left", fill='y', padx=5, pady=10)

        # NAVIGATION
        self.nav_label.pack(side="left", fill='both', expand=True)
        self.inventory_to_excel.pack(side="left")
        self.nav_frame.pack(side="top", fill='x', pady=5)

        # INVENTORY TABLE
        self.inventory_table.pack(fill='both', padx=10, pady=10, expand=True)
        self.inventory_frame.pack(side="bottom", fill='both', pady=5, expand=True)

        # DISTRIBUTION TABLE
        self.distribution_table.pack(fill='both', padx=10, pady=10, expand=True)

        self.dash_frame.pack(side="left", fill='both', padx=5, pady=5, expand=True)
        self.main_frame.pack(expand=True, fill='both')

        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        self.top.mainloop()

    def inventory_to_excel(self):
        if datafunc.inventory_data:
            self.file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                          filetypes=[('Excel files', '*.xlsx')],
                                                          initialfile='module_inventory.xlsx')
            if datafunc.inventory_to_excel(self.file_path):
                messagebox.showinfo(title='Successful',
                                    message=f'Module inventory excel file has been successfully '
                                            f'saved in {self.file_path}',
                                    parent=self.top)
        else:
            messagebox.showinfo(title='No data', message='Inventory has no data.', parent=self.top)

    def student_to_excel(self):
        if datafunc.student_data:
            self.file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                          filetypes=[('Excel files', '*.xlsx')],
                                                          initialfile='distribution_data.xlsx')
            if datafunc.student_to_excel(self.file_path):
                messagebox.showinfo(title='Successful', message=f'Module inventory excel file has been successfully '
                                                                f'saved in {self.file_path}',
                                    parent=self.top)
        else:
            messagebox.showinfo(title='No data', message='Distribution has no data.', parent=self.top)

    def shortcut(self, event):
        if event.keysym == 'Return':
            if event.widget == self.add_new_quantity_box:
                self.add_new_inventory_data.invoke()
            elif event.widget == self.modify_quantity_box:
                self.modify_inventory_data.invoke()
            elif event.widget == self.add_quantity_box:
                self.add_inventory_data.invoke()
            elif event.widget == self.delete_pen_code_box:
                self.delete_inventory_data.invoke()
            elif event.widget == self.filter_keyword_box:
                self.filter_distribution_data.invoke()
            elif event.widget == self.modify_name_box:
                self.modify_distribution_data.invoke()
            elif event.widget == self.delete_keyword_box:
                self.delete_distribution_data.invoke()
            else:
                self.top.event_generate('<Tab>')

    def inventory(self):
        self.update_inventory_table()
        if self.show_inventory:
            self.student_to_excel.pack_forget()
            self.distribution_frame.pack_forget()
            self.distribution_manager_frame.pack_forget()
            self.nav_label.configure(text='Monitoring >> Inventory')
            self.inventory_frame.pack(side="bottom", fill='both', pady=5, expand=True)
            self.inventory_manager_frame.pack(expand=True, fill='both', pady=20)
            self.inventory_to_excel.pack(side="left")
            self.delete_distribution_box()
            self.show_inventory = False

    def add_new_inventory(self):
        self.delete_inventory_box()
        self.nav_label.configure(text='Monitoring >> Inventory >> Add New')
        self.add_new_inventory_frame.pack(side="left", expand=True, fill='x')

    def add_inventory(self):
        self.delete_inventory_box()
        self.nav_label.configure(text='Monitoring >> Inventory >> Add')
        self.add_inventory_frame.pack(side="left", expand=True, fill='x')

    def modify_inventory(self):
        self.delete_inventory_box()
        self.nav_label.configure(text='Monitoring >> Inventory >> Modify')
        self.modify_inventory_frame.pack(side="left", expand=True, fill='x')

    def delete_inventory(self):
        self.delete_inventory_box()
        self.nav_label.configure(text='Monitoring >> Inventory >> Delete')
        self.delete_inventory_frame.pack(side="left", expand=True, fill='x')

    def add_new_inventory_data(self):
        if self.add_new_pen_code.get() and self.add_new_title.get() and self.add_new_quantity.get():
            if not datafunc.add_inventory(self.add_new_pen_code.get().upper().strip(),
                                          self.add_new_title.get().title().strip(),
                                          int(self.add_new_quantity.get().strip())):
                self.update_inventory_table()
                self.add_new_pen_code_box.focus()
                self.add_new_pen_code_box.delete(0, 'end')
                self.add_new_title_box.delete(0, 'end')
                self.add_new_quantity_box.delete(0, 'end')
                datafunc.write_data()
            else:
                messagebox.showinfo(title='Error',
                                    message=f'{self.add_new_pen_code.get().upper()} already exist.',
                                    parent=self.top)
                self.add_new_pen_code_box.focus()
                self.add_new_pen_code_box.delete(0, 'end')
                self.add_new_title_box.delete(0, 'end')
                self.add_new_quantity_box.delete(0, 'end')

    def modify_inventory_data(self):
        if self.modify_pen_code.get() and self.modify_title.get() and self.modify_quantity.get():
            if not datafunc.modify_inventory(self.modify_pen_code.get().upper().strip(),
                                             self.modify_title.get().title().strip(),
                                             int(self.modify_quantity.get().strip())):
                self.update_inventory_table()
                self.modify_pen_code_box.focus()
                self.modify_pen_code_box.delete(0, 'end')
                self.modify_title_box.delete(0, 'end')
                self.modify_quantity_box.delete(0, 'end')
                datafunc.write_data()
            else:
                messagebox.showinfo(title='Error',
                                    message=f'{self.modify_pen_code.get().upper().strip()} or '
                                            f'{self.modify_title.get().title().strip()} does not exist.',
                                    parent=self.top)
                self.modify_pen_code_box.focus()
                self.modify_pen_code_box.delete(0, 'end')
                self.modify_title_box.delete(0, 'end')
                self.modify_quantity_box.delete(0, 'end')

    def add_inventory_data(self):
        if self.add_pen_code.get() and self.add_quantity.get():
            if not datafunc.add_inventory_data(self.add_pen_code.get().upper().strip(),
                                               int(self.add_quantity.get().strip())):
                self.update_inventory_table()
                self.add_pen_code_box.focus()
                self.add_pen_code_box.delete(0, 'end')
                self.add_quantity_box.delete(0, 'end')
                datafunc.write_data()
            else:
                messagebox.showinfo(title='Error', message=f'{self.add_pen_code.get().upper().strip()} does not exist.',
                                    parent=self.top)
                self.add_pen_code_box.focus()
                self.add_pen_code_box.delete(0, 'end')
                self.add_quantity_box.delete(0, 'end')

    def delete_inventory_data(self):
        if self.delete_pen_code.get():
            if datafunc.inDict(datafunc.inventory_data, self.delete_pen_code.get().upper().strip()):
                if messagebox.askyesno(title='Delete?',
                                       message=f"Do you want to delete {self.delete_pen_code.get().upper().strip()}?\n"
                                               f"\nThis action will BACKUP the deleted data which can be added back to "
                                               f"the CURRENT data using the 'RESTORE' action.", parent=self.top,
                                       icon=messagebox.WARNING):
                    datafunc.delete_inventory(self.delete_pen_code.get().upper().strip())
                    self.update_inventory_table()
                    self.delete_pen_code_box.delete(0, 'end')
                    datafunc.write_data()
                    datafunc.write_data_backup()
            else:
                messagebox.showinfo(title='Error',
                                    message=f'{self.delete_pen_code.get().upper().strip()} does not exist.',
                                    parent=self.top)
                self.delete_pen_code_box.delete(0, 'end')

    def clear_inventory_data(self):
        self.delete_inventory_box()
        self.nav_label.configure(text='Monitoring >> Inventory')
        if datafunc.inventory_data:
            if messagebox.askyesno(title='Clear data?', message=f"Do you want to delete ALL inventory data?\n\nThis "
                                                                f"action will BACKUP the deleted data which can be "
                                                                f"added back to the data using the 'RESTORE' action.",
                                   parent=self.top, icon=messagebox.WARNING):
                datafunc.clear_inventory()
                self.update_inventory_table()
                self.prev = None
                datafunc.write_data()
                datafunc.write_data_backup()
        else:
            messagebox.showinfo(title='No data', message='Inventory has no data.', parent=self.top)

    def restore_inventory_data(self):
        self.delete_inventory_box()
        self.nav_label.configure(text='Monitoring >> Inventory')
        if datafunc.inventory_data_backup:
            if messagebox.askyesno(title='Restore?', message='Do you want to restore ALL deleted INVENTORY data?\n'
                                                             '\nThis action will NOT OVERWRITE duplicates in the '
                                                             'CURRENT data and will EMPTY the INVENTORY backup '
                                                             'data.', parent=self.top, icon=messagebox.WARNING):
                datafunc.restore_inventory_data()
                self.update_inventory_table()
                datafunc.write_data()
                datafunc.write_data_backup()
        else:
            messagebox.showinfo(title='No data', message='Inventory backup has no data.', parent=self.top)

    def distribution(self):
        self.distribution_table.selection_remove(*self.distribution_table.selection())
        self.update_distribution_table(False)
        if not self.show_inventory:
            self.inventory_to_excel.pack_forget()
            self.inventory_frame.pack_forget()
            self.inventory_manager_frame.pack_forget()
            self.nav_label.configure(text='Monitoring >> Distribution')
            self.distribution_frame.pack(side="bottom", fill='both', pady=5, expand=True)
            self.distribution_manager_frame.pack(expand=True, fill='both', pady=20)
            self.student_to_excel.pack(side="left")
            self.delete_inventory_box()
            self.show_inventory = True

    def filter_distribution(self):
        self.delete_distribution_box()
        self.nav_label.configure(text='Monitoring >> Distribution >> Filter')
        self.filter_distribution_frame.pack(side="left", expand=True, fill='x')
        self.distribution_table.selection_remove(*self.distribution_table.selection())

    def modify_distribution(self):
        self.delete_distribution_box()
        self.remove_distribution_data_filter.invoke()
        self.nav_label.configure(text='Monitoring >> Distribution >> Modify')
        self.modify_distribution_frame.pack(side="left", expand=True, fill='x')
        self.distribution_table.selection_remove(*self.distribution_table.selection())

    def delete_distribution(self):
        self.delete_distribution_box()
        self.remove_distribution_data_filter.invoke()
        self.nav_label.configure(text='Monitoring >> Distribution >> Delete')
        self.delete_distribution_frame.pack(side="left", expand=True, fill='x')
        self.distribution_table.selection_remove(*self.distribution_table.selection())

    def filter_distribution_data(self):
        self.distribution_table.selection_remove(*self.distribution_table.selection())
        if self.filter_keyword.get():
            if (datafunc.inDict(datafunc.student_data, self.filter_keyword.get().upper().strip()) or
                    datafunc.inDict(datafunc.student_data, self.filter_keyword.get().title().strip())):
                if isinstance(datafunc.filter_student_data(self.filter_keyword.get().upper().strip()), list):
                    self.distribution_data = datafunc.filter_student_data(self.filter_keyword.get().upper().strip())
                else:
                    self.distribution_data = datafunc.filter_student_data(self.filter_keyword.get().title().strip())
                self.update_distribution_table(True)
                self.filter_keyword_box.delete(0, 'end')
                self.remove_distribution_data_filter.pack(fill='x')
            else:
                messagebox.showinfo(title='No data', message=f'Data has no record on '
                                                             f'{self.filter_keyword.get().strip().upper()}.',
                                    parent=self.top)

    def remove_distribution_data_filter(self):
        self.update_distribution_table(False)
        self.filter_keyword_box.delete(0, 'end')
        self.remove_distribution_data_filter.pack_forget()
        self.distribution_table.selection_remove(*self.distribution_table.selection())

    def modify_distribution_data(self):
        self.remove_distribution_data_filter.invoke()
        self.distribution_table.selection_remove(*self.distribution_table.selection())
        if self.modify_course.get() and self.modify_id.get() and self.modify_name.get():
            if not datafunc.modify_student_data(self.modify_course.get().upper().strip(), self.modify_id.get().strip(),
                                                self.modify_name.get().title().strip()):
                self.update_distribution_table(False)
                self.modify_course_box.focus()
                self.modify_course_box.delete(0, 'end')
                self.modify_id_box.delete(0, 'end')
                self.modify_name_box.delete(0, 'end')
                datafunc.write_data()
            else:
                messagebox.showinfo(title='Error', message=f'{self.modify_course.get().upper().strip()} or '
                                                           f'{self.modify_id.get().strip()} or '
                                                           f'{self.modify_name.get().title().strip()} does not exist.',
                                    parent=self.top)
                self.modify_course_box.focus()
                self.modify_course_box.delete(0, 'end')
                self.modify_id_box.delete(0, 'end')
                self.modify_name_box.delete(0, 'end')

    def delete_distribution_data(self):
        self.remove_distribution_data_filter.invoke()
        self.distribution_table.selection_remove(*self.distribution_table.selection())
        if self.delete_keyword.get():
            if datafunc.inDict(datafunc.student_data, self.delete_keyword.get().upper().strip()):
                if messagebox.askyesno(title='Delete?',
                                       message=f"Do you want to delete {self.delete_keyword.get().upper().strip()}?\n"
                                               f"\nThis action will BACKUP the deleted data which can be added back to "
                                               f"the CURRENT data using the 'RESTORE' action.", parent=self.top,
                                       icon=messagebox.WARNING):
                    datafunc.delete_distribution(self.delete_keyword.get().upper().strip())
                    self.update_distribution_table(False)
                    self.delete_keyword_box.delete(0, 'end')
                    datafunc.write_data()
                    datafunc.write_data_backup()
            else:
                messagebox.showinfo(title='Error', message=f'{self.delete_keyword.get().upper().strip()} does not '
                                                           f'exist.', parent=self.top)
                self.delete_keyword_box.delete(0, 'end')

    def clear_distribution_data(self):
        self.delete_distribution_box()
        if datafunc.student_data:
            if messagebox.askyesno(title='Clear data?', message=f"Do you want to delete ALL distribution data?\n\nThis "
                                                                f"action will BACKUP the deleted data which can be "
                                                                f"added back to the data using the 'RESTORE' action.",
                                   parent=self.top, icon=messagebox.WARNING):
                datafunc.clear_distribution()
                self.update_distribution_table(False)
                datafunc.write_data()
                datafunc.write_data_backup()
        else:
            messagebox.showinfo(title='No data', message='Distribution has no data.', parent=self.top)

    def restore_distribution_data(self):
        self.delete_distribution_box()
        self.remove_distribution_data_filter.invoke()
        self.nav_label.configure(text='Monitoring >> Distribution')
        self.distribution_table.selection_remove(*self.distribution_table.selection())
        if datafunc.student_data_backup:
            if messagebox.askyesno(title='Restore?', message='Do you want to restore ALL deleted DISTRIBUTION data?\n'
                                                             '\nThis action will NOT OVERWRITE duplicates in the '
                                                             'CURRENT data and will EMPTY the DISTRIBUTION backup '
                                                             'data.', parent=self.top, icon=messagebox.WARNING):
                datafunc.restore_distribution_data()
                self.update_distribution_table(False)
                datafunc.write_data()
                datafunc.write_data_backup()
        else:
            messagebox.showinfo(title='No data', message='Distribution backup has no data.', parent=self.top)

    def delete_inventory_box(self):
        self.top.focus()
        self.add_new_pen_code_box.delete(0, 'end')
        self.add_new_title_box.delete(0, 'end')
        self.add_new_quantity_box.delete(0, 'end')
        self.modify_pen_code_box.delete(0, 'end')
        self.modify_title_box.delete(0, 'end')
        self.modify_quantity_box.delete(0, 'end')
        self.add_pen_code_box.delete(0, 'end')
        self.add_quantity_box.delete(0, 'end')
        self.delete_pen_code_box.delete(0, 'end')
        self.add_new_inventory_frame.pack_forget()
        self.modify_inventory_frame.pack_forget()
        self.add_inventory_frame.pack_forget()
        self.delete_inventory_frame.pack_forget()

    def delete_distribution_box(self):
        self.top.focus()
        self.filter_keyword_box.delete(0, 'end')
        self.modify_id_box.delete(0, 'end')
        self.modify_name_box.delete(0, 'end')
        self.delete_keyword_box.delete(0, 'end')
        self.filter_distribution_frame.pack_forget()
        self.modify_distribution_frame.pack_forget()
        self.delete_distribution_frame.pack_forget()

    def update_inventory_table(self):
        self.inventory_table.delete(*self.inventory_table.get_children())
        self.inventory_data = datafunc.get_inventory_data()
        for row in self.inventory_data:
            self.inventory_table.insert('', 'end', values=row)

    def update_distribution_table(self, is_filtering):
        self.distribution_table.delete(*self.distribution_table.get_children())
        if not is_filtering:
            self.distribution_data = datafunc.get_student_data()
        self.prev = None
        for row in self.distribution_data:
            if isinstance(row[4], tuple):
                parent = self.distribution_table.insert('', 'end', values=(row[0], row[1], row[2], row[3],
                                                                           f'  {row[4][0]}', row[5][0]), open=False)
                for i in range(1, len(row[4])):
                    self.distribution_table.insert(parent, 'end', values=('', '', '', '', f'  {row[4][i]}', row[5][i]))
            else:
                self.distribution_table.insert('', 'end', values=(row[0], row[1], row[2], row[3],
                                                                  f'  {row[4]}', row[5]), open=False)

    def hover(self, event):
        row = event.widget.identify_row(event.y)
        if row != self.prev:
            if self.prev:
                event.widget.item(self.prev, tags=[])
            event.widget.item(row, tags=['hover'])
            self.prev = row

    def toggle_row(self, event):
        _row = event
        row = self.distribution_table.focus()
        for _row in self.distribution_table.get_children():
            if not _row == row:
                self.distribution_table.item(_row, open=False)
        self.distribution_table.item(row, open=not self.distribution_table.item(row, 'open'))

    def center_window(self, width, height):
        x_coordinate = (self.top.winfo_screenwidth() - width) // 2
        y_coordinate = (self.top.winfo_screenheight() - height) // 3
        self.top.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def on_close(self):
        if messagebox.askyesno(title='Exit?', message='Do you want to exit?', parent=self.top):
            self.master.deiconify()
            self.top.destroy()
