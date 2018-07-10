
# -*- coding: utf-8 -*-
import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from processor.ontology.Ontology import Ontology
from processor.ontology.AutocompleteEntry import AutocompleteEntry as AutoEntry


class Example(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # variable
        self.variable = {}
        self.word = tk.StringVar()
        self.wclass = tk.StringVar()
        self.test = tk.StringVar()
        self.ont = Ontology()
        self.ontoname = tk.StringVar()

        # frame -1
        frame = tk.Frame(self)
        tk.Label(frame, text='Tên Ontology').pack(side='left', padx=5, pady=5)
        tk.Entry(frame, textvariable=self.ontoname).pack(side='left', padx=5, pady=5)
        frame.pack(side='top', fill='x')

        # frame 0
        frame0 = tk.Frame(self)
        self.listword = tk.Listbox(frame0, width='40')
        tk.Button(frame0, text='RELOAD', command=self.loadlistword).pack(side='bottom', padx=5, pady=5)
        frame0.pack(side='right', fill='y', padx=5, pady=5)
        self.listword.pack(side='top', expand=1, fill='y', padx=5, pady=5)

        # frame 1: word
        frame1 = tk.Frame(self)
            # word name
        tk.Label(frame1, text="Word").pack(side='left', padx=5, pady=5)
        entry_name = ttk.Entry(frame1, textvariable=self.word)
        entry_name.pack(side='left', padx=5, pady=5)
        tk.Label(frame1, text="Class").pack(side='left', padx=5, pady=5)
            # class name
        cbb_class = ttk.Combobox(frame1, textvariable=self.wclass)
        cbb_class['value'] = Ontology.Class
        cbb_class.pack(side='left', padx=5, pady=5)
        frame1.pack(side='top', fill='x')

        # frame 1: data entry
        entry_relation = self.relationUI('Relation', Ontology.Relation)
        entry_data = self.relationUI('Data Properties', Ontology.DataProperty)
        self.relationUI('Person Data', Ontology.PersonData)
        self.relationUI('Book Data', Ontology.BookData)

        # frame 4: button
        frame4 = tk.Frame(self)
        btn_add = tk.Button(frame4, text='ADD', command=self.addword)
        btn_save = tk.Button(frame4, text='SAVE', command=self.saveonto)
        btn_show = tk.Button(frame4, text='SHOW', command=self.showonto)
        btn_load = tk.Button(frame4, text='LOAD', command=self.loadonto)
        btn_reasoner = tk.Button(frame4, text='REASONER', command=self.onto_reasoner)
        btn_delete = tk.Button(frame4, text='DELETE', command=self.deleteWord)
        btn_save.pack(side='right', padx=5, pady=5)
        btn_add.pack(side='right', padx=5, pady=5)
        btn_show.pack(side='right', padx=5, pady=5)
        btn_load.pack(side='right', padx=5, pady=5)
        btn_reasoner.pack(side='right', padx=5, pady=5)
        btn_delete.pack(side='right', padx=5, pady=5)
        frame4.pack(side='top', fill='x', padx=5, pady=5)

    # Khởi tạo GUI cho các property
    def relationUI(self, name, list):
        widget = {}
        lbf = tk.LabelFrame(self, text=name)
        for i in list:
            frame = tk.Frame(lbf)
            label_text = tk.StringVar()
            label = tk.Label(frame, text=i+': ')
            entry = tk.Entry(frame, textvariable=label_text, width='80')

            label.pack(side='left', padx=5, pady=5)
            entry.pack(side='right', padx=5, pady=5)
            frame.pack(side='top', fill='x', padx=5, pady=5)
            widget[i] = entry
            self.variable[i] = label_text
        lbf.pack(side='top', fill='x', padx=5, pady=5)
        return widget

    def addword(self):
        word = self.word.get()
        self.ont.initword(word, self.wclass.get())
        if word == '':
            messagebox.showerror("Lỗi", "Chưa điền thông tin")
            return
        for i in Ontology.Relation:
            x = self.variable[i].get().split(',')
            for w in x:
                self.ont.addRelation(word, i, w)
        for i in Ontology.DataProperty:
            self.ont.addData(word, i, self.variable[i].get())
        for i in Ontology.PersonData:
            self.ont.addData(word, i, self.variable[i].get())
        for i in Ontology.BookData:
            self.ont.addData(word, i, self.variable[i].get())
        self.loadlistword()
        pass

    def saveonto(self):
        name = self.ontoname.get()
        if name == '':
            messagebox.showerror('Trang Uyên', 'Chưa nhập tên Onto (tên file)')
            return
        if os.path.isfile(name) or os.path.isfile(name + ".npy"):
            result = messagebox.askyesno('Trang Uyên', 'File ' + name + ' đã tồn tại. Bạn có muốn ghi đè lên không?')
            if result is False:
                return
        extension = name[-4:].lower()
        if extension == '.csv':
            Ontology.save_to_csv(name, self.ont)
        elif extension == '.npy':
            Ontology.save(name, self.ont)
        else:
            Ontology.save(name + ".npy", self.ont)
        messagebox.showinfo('Trang Uyên', 'Lưu file '+name+' thành công!')
        pass

    def showonto(self):
        word = self.listword.get('active')
        self.word.set(word)
        self.wclass.set(self.ont.onto[word]['Class'])
        for i in Ontology.Relation:
            if i in self.ont.onto[word]['Relation']:
                self.variable[i].set(','.join(self.ont.onto[word]['Relation'][i]))
            else:
                self.variable[i].set('')
        for i in Ontology.AllDataProperty:
            if i in self.ont.onto[word]['Data']:
                self.variable[i].set(self.ont.onto[word]['Data'][i])
            else:
                self.variable[i].set('')
        # messagebox.showinfo("", word)
        pass

    def loadonto(self):
        tempdir = filedialog.askopenfilename(parent=self, title="Select file",
                                             filetypes=[("npy files", "*.npy"), ("csv files", "*.csv")],
                                             multiple=False)
        if len(tempdir) > 0:
            extension = tempdir[-3:].lower()
            if extension == 'npy':
                self.ont = Ontology.load(tempdir)
            elif extension == 'csv':
                self.ont = Ontology.load_from_csv(tempdir)
                #messagebox.showinfo("Trang Uyên", self.ont.onto)
            self.loadlistword()
        messagebox.showinfo("Trang Uyên", "ONTOLOGY LOADED")

    def loadlistword(self):
        self.listword.delete(0, 'end')
        for w in self.ont.words:
            self.listword.insert('end', w)
        pass

    def onto_reasoner(self):
        self.ont.reasoner()
        self.loadlistword()
        pass

    def deleteWord(self):
        word = self.listword.get('active')
        result = messagebox.askyesno('Trang Uyên', 'Bạn có muốn xóa từ "' + word + '" không?')
        if result:
            self.ont.deleteWord(word)
            self.loadlistword()
        pass


class ManageOntology:
    def start(self):
        root = tk.Tk()
        root.title('Ontology')
        root.tk.call('encoding', 'system', 'utf-8')
        Example(root).pack(fill="both", expand=True)
        root.mainloop()
