import os
import re
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from scrollframe import ScrollFrame
from PIL import Image, ImageTk
import datafunc

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base_path, relative_path)


class Distribution:
    def __init__(self, master):
        self.subjects = None
        self.id = None
        self.name = None
        self.course = None
        self.distribution_data = None
        self.state = None
        self.label = None
        self.p1 = re.compile(r'\d{2}-\d{4}-\d{5,}')
        self.p2 = re.compile(r'^[A-Za-z ]+, [A-Za-z ]+ [A-Za-z]\.$')
        self.top = tk.Toplevel(master)
        self.top.title('Module Distribution')
        self.center_window(680, 600)

        self.master = master
        self.master.withdraw()

        self.style = ttk.Style(self.top)
        self.style.configure('submit.TButton', font=('Segoe UI', 12))
        self.style.configure('refresh.TButton', font=('Segoe UI', 8))
        self.style.configure('TCheckbutton', font=('Segoe UI', 9), background='#D2D2D2')

        self.main_frame = tk.Frame(self.top, bg='#F6F6F6')

        self.info_frame = tk.Frame(self.main_frame, padx=5, pady=5, bg='#DCDCDC')
        self.info_label = ttk.Label(self.info_frame, padding=(0, 3), text='INFORMATION', font=('Segoe UI', 12),
                                    anchor='center', background='#DCDCDC')
        self.info_box_frame = tk.Frame(self.info_frame, bg='#DCDCDC')
        self.info_course_frame = tk.Frame(self.info_box_frame, bg='#DCDCDC')
        self.info_course = tk.StringVar()
        self.info_course_text = ttk.Label(self.info_course_frame, text='\nCOURSE', font=('Segoe UI', 10),
                                          background='#DCDCDC')
        self.options = ['ABEL', 'BSA', 'BSAIS', 'BSAR', 'BSCE', 'BSCRIM', 'BSCS', 'BSENT', 'BSTM', 'MedTech',
                        'Other']
        self.info_course_box = ttk.Combobox(self.info_course_frame, textvariable=self.info_course, values=self.options,
                                            font=('Segoe UI', 11), justify='center', state='readonly', takefocus=0)
        self.info_course_box.bind('<<ComboboxSelected>>', self.combobox)
        self.info_course_box.bind('<KeyPress>', self.shortcut)
        self.info_course_box.bind('<FocusOut>', self.focus_out)
        self.info_id_frame = tk.Frame(self.info_box_frame, bg='#DCDCDC')
        self.info_id = tk.StringVar()
        self.info_id_text = ttk.Label(self.info_id_frame, text='STUDENT ID\nEx. ##-####-######', font=('Segoe UI', 10),
                                      background='#DCDCDC')
        self.info_id_box = ttk.Entry(self.info_id_frame, textvariable=self.info_id, font=('Segoe UI', 11),
                                     justify='center')
        self.info_id_box.bind('<KeyPress>', self.shortcut)
        self.info_id_box.bind('<FocusOut>', self.focus_out)
        self.info_name_frame = tk.Frame(self.info_box_frame, bg='#DCDCDC')
        self.info_name = tk.StringVar()
        self.info_name_text = ttk.Label(self.info_name_frame, text='STUDENT NAME\nEx. Doe, John A.',
                                        font=('Segoe UI', 10), background='#DCDCDC')
        self.info_name_box = ttk.Entry(self.info_name_frame, textvariable=self.info_name, font=('Segoe UI', 11),
                                       justify='center')
        self.info_name_box.bind('<KeyPress>', self.shortcut)
        self.info_name_box.bind('<FocusOut>', self.focus_out)

        self.claim_frame = tk.Frame(self.main_frame, padx=5, pady=5, bg='#DCDCDC')
        self.claim_label = ttk.Label(self.claim_frame, padding=(0, 3), text='CLAIM', font=('Segoe UI', 12),
                                     anchor='center', background='#DCDCDC')
        self.claim_label.pack(fill='x', anchor='n')
        self.path = resource_path('refresh.png')
        self.image = ImageTk.PhotoImage(Image.open(self.path).resize((15, 15), Image.LANCZOS))
        self.refresh = ttk.Button(self.claim_frame, command=self.refresh, state='disabled',
                                  takefocus=0, style='refresh.TButton', padding=(-5, -5))

        self.keyword = tk.StringVar()
        self.search = ttk.Entry(self.claim_frame, textvariable=self.keyword, font=('Segoe UI', 11))
        self.search.bind('<KeyRelease>', self.filter)
        self.setup_search()

        self.checks_frame = ScrollFrame(self.claim_frame)
        self.data = datafunc.get_pen()
        self.checks = {}
        for pen in self.data:
            self.checks[pen] = tk.BooleanVar()
            self.check = ttk.Checkbutton(self.checks_frame.frame, text=f'  {pen}', variable=self.checks[pen],
                                         name=pen.lower(), takefocus=0, command=self.update_button_state)
            self.check.lower()
            self.check.pack(fill='x', ipady=5, pady=5, padx=5)

        self.result_frame = tk.Frame(self.main_frame, pady=5, padx=10, bg='#DCDCDC')
        self.result_label = ttk.Label(self.result_frame, padding=(0, 5), text='RESULT', font=('Segoe UI', 12),
                                      anchor='center', background='#DCDCDC')

        self.submit = ttk.Button(self.main_frame, text='Claim', command=self.submit, state='disabled',
                                 takefocus=0, style='submit.TButton')

        self.info_label.pack(fill='x', anchor='n')
        self.info_course_text.pack(anchor='nw', pady=5)
        self.info_course_box.pack(fill='x')
        self.info_course_frame.pack(fill='x', pady=20)
        self.info_id_text.pack(anchor='nw', pady=5)
        self.info_id_box.pack(fill='x')
        self.info_id_frame.pack(fill='x', pady=10)
        self.info_name_text.pack(anchor='nw', pady=5)
        self.info_name_box.pack(fill='x')
        self.info_name_frame.pack(fill='x', pady=20)
        self.info_box_frame.pack(fill='x', padx=10, pady=20)
        self.info_frame.place(relx=0.165, rely=0.019, anchor='n', relwidth=0.30, relheight=0.83)

        self.refresh.place(relx=1, rely=0, anchor='ne', width=25, height=25)
        self.search.pack(fill='x', pady=5)
        self.checks_frame.pack(fill='both', expand=True)
        self.claim_frame.place(relx=0.5, rely=0.019, anchor='n', relwidth=0.34, relheight=0.83)

        self.result_label.pack(fill='x', anchor='n')
        self.result_frame.place(relx=0.835, rely=0.019, anchor='n', relwidth=0.30, relheight=0.83)

        self.submit.place(relx=0.5, rely=0.93, anchor='center', relwidth=0.25, relheight=0.06)

        self.main_frame.pack(fill='both', expand=True)

        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        self.top.mainloop()

    def clear(self, _):
        self.top.focus()

    def setup_search(self):
        placeholder = "Search for item ..."
        def focus_in(_):
            if self.search.get() == placeholder:
                self.search.delete(0, tk.END)
                self.search.configure(foreground='black')
        def focus_out(_):
            if not self.search.get():
                self.search.insert(0, placeholder)
                self.search.configure(foreground='gray')
        self.search.insert(0, placeholder)
        self.search.configure(foreground='gray')
        self.search.bind("<FocusIn>", focus_in)
        self.search.bind("<FocusOut>", focus_out)

    def filter(self, _):
        for pen, var in self.checks.items():
            keyword = self.keyword.get().lower()
            if keyword in pen.lower():
                self.checks_frame.frame.nametowidget(pen.lower()).pack(fill='x', ipady=5, pady=5, padx=5)
            else:
                self.checks_frame.frame.nametowidget(pen.lower()).pack_forget()

    def combobox(self, event):
        if self.info_course.get() == 'Other':
            self.info_course_text.configure(text='ENTER YOUR COURSE\nEx. BSENTREP')
            self.info_course_box.state(['!readonly'])
            self.info_course_box.delete(0, 'end')
        elif event:
            self.info_course_text.configure(text='\nCOURSE')
            self.info_course_box.state(['readonly'])
            self.info_id_box.focus()
            for child in self.result_frame.winfo_children():
                if child is not self.result_label:
                    child.destroy()

    def shortcut(self, event):
        if event.keysym == 'Return':
            if event.widget == self.info_id_box:
                self.check_id()
            elif event.widget == self.info_name_box:
                self.check_name()
            else:
                self.info_id_box.focus()
        else:
            event.widget.configure(foreground='black')
            self.update_button_state()

    def check_id(self):
        if self.p1.match(self.info_id.get().strip()):
            self.info_id_box.configure(foreground='black')
            self.top.event_generate('<Tab>')
            return True
        else:
            self.info_id_box.configure(foreground='red')
            return False

    def check_name(self):
        if self.p2.match(self.info_name.get()):
            self.info_name_box.configure(foreground='black')
            self.top.focus()
            return True
        else:
            self.info_name_box.configure(foreground='red')
            return False

    def focus_out(self, event):
        if event.widget == self.info_course_box:
            self.info_course_text.configure(text='\nCOURSE')
            self.info_course_box.state(['readonly'])
        elif event.widget == self.info_id_box:
            if self.p1.match(self.info_id.get().strip()):
                self.info_id_box.configure(foreground='black')
                if datafunc.inDict(datafunc.student_data, self.info_id.get().strip()):
                    self.distribution_data = datafunc.get_student_name_id(self.info_id.get().strip())
                    self.course = list(self.distribution_data.keys())[0]
                    self.name = list(self.distribution_data[self.course][self.info_id.get().strip()].keys())[0]
                    self.info_course_box.set(self.course)
                    self.info_name_box.delete(0, 'end')
                    self.info_name_box.insert(0, self.name)
                    self.top.focus()
            else:
                self.info_id_box.configure(foreground='red')
        else:
            if self.p2.match(self.info_name.get()):
                self.info_name_box.configure(foreground='black')
                if datafunc.inDict(datafunc.student_data, self.info_name.get().title().strip()):
                    self.distribution_data = datafunc.get_student_name_id(self.info_name.get().title().strip())
                    self.course = list(self.distribution_data.keys())[0]
                    self.id = list(self.distribution_data[self.course].keys())[0]
                    self.name = list(self.distribution_data[self.course][self.id].keys())[0]
                    self.subjects = self.distribution_data[self.course][self.id][self.name]
                    self.info_course_box.set(self.course)
                    self.info_id_box.delete(0, 'end')
                    self.info_id_box.insert(0, self.id)
                    for subject, claims in self.subjects.items():
                        for _, claimed in claims.items():
                            if not claimed:
                                self.checks[subject].set(True)
                            else:
                                for frame in self.checks_frame.winfo_children():
                                    for canvas in frame.winfo_children():
                                        for checkbutton in canvas.winfo_children():
                                            if checkbutton.cget('text') == f'  {subject}':
                                                self.checks[subject].set(False)
                                                checkbutton['state'] = 'disabled'
            else:
                self.info_name_box.configure(foreground='red')
        self.update_button_state()

    def refresh(self):
        for var in self.checks.values():
            var.set(False)
        self.update_button_state()
        self.top.focus()

    def update_button_state(self):
        for child in self.result_frame.winfo_children():
            if child is not self.result_label:
                child.destroy()
        if any(var.get() for var in self.checks.values()):
            self.refresh['state'] = 'normal'
            self.refresh.configure(image=self.image)
            if self.p1.match(self.info_id.get().strip()) and self.p2.match(self.info_name.get()):
                if sum(val.get() is True for val in self.checks.values()) < 11:
                    self.submit['state'] = 'normal'
                else:
                    self.submit['state'] = 'disabled'
        else:
            self.submit['state'] = 'disabled'
            self.refresh['state'] = 'disabled'
            self.refresh.configure(image='')

    def submit(self):
        if self.info_course.get() and self.check_id() and self.info_id.get() and self.check_name() and self.info_name.get():
            checked = [pen for pen, var in self.checks.items() if var.get()]
            if messagebox.askyesno(title='Submit?', message=f'Are you sure you want to claim these '
                                                            f'modules?\n{", ".join(checked)}', parent=self.top):
                claimed = {}
                for pen in checked:
                    if datafunc.subtract_inventory_data(pen):
                        claimed[pen] = False
                    else:
                        claimed[pen] = True
                for pen, claim in claimed.items():
                    self.label = ttk.Label(self.result_frame,
                                           text=f"{pen}  -  {'Claimed' if claim else 'Unclaimed'}",
                                           font=('Segoe UI', 9), anchor='center', background='#D2D2D2')
                    self.label.pack(fill='x', ipady=6, pady=5)
                datafunc.add_student(self.info_course.get().upper().strip(), self.info_id.get().strip(),
                                     self.info_name.get().title().strip(), claimed)
                for var in self.checks.values():
                    var.set(False)
                for frame in self.checks_frame.winfo_children():
                    for canvas in frame.winfo_children():
                        for checkbutton in canvas.winfo_children():
                            checkbutton['state'] = 'normal'
                self.submit['state'] = 'disabled'
                self.refresh['state'] = 'disabled'
                self.refresh.configure(image='')
                claimed.clear()
                self.top.focus()
                self.info_course_box.set('')
                self.info_id_box.delete(0, 'end')
                self.info_name_box.delete(0, 'end')
                datafunc.write_data()
        else:
            messagebox.showinfo(title='Missing', message='Missing information.', parent=self.top)

    def center_window(self, width, height):
        x_coordinate = (self.top.winfo_screenwidth() - width) // 2
        y_coordinate = (self.top.winfo_screenheight() - height) // 3
        self.top.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def on_close(self):
        if messagebox.askyesno(title='Exit?', message='Do you want to exit?', parent=self.top):
            self.master.deiconify()
            self.top.destroy()
