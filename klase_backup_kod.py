from baza_pod import *
from tkinter import *
from tkinter import filedialog, messagebox
import sqlite3
import io
from PIL import Image, ImageTk
from PIL import *
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# KLASA BILJKE, UNUTAR KLASE JE REGISTRACIJA NOVE BILJKE JER SVAKA NOVA BILJKA IMA ISTE PARAMTERE POPUT NAZIVA NJEGE SLIKE I SLIČNO!!!

class Biljke():
    biljke_instanca = None

    def __init__(self, biljke_root, height, width):
        super().__init__()
        self.biljke_root = biljke_root
        self.biljke_root['height'] = height
        self.biljke_root['width'] = width
        self.putanja_do_slike = None
        self.naziv_var = StringVar()
        self.njega_var = StringVar()
        self.slika_info_label = None  

    def start_klasa_biljke(self): 
        print('pokrenuta nova biljka klasa')
        self.biljke_instanca = self

        nova_biljka = Toplevel(self.biljke_root)
        nova_biljka.geometry('400x300')
        nova_biljka.title("Nova biljka")
        nova_biljka.biljke_instanca = self
        nova_biljka.slika_info_label = self.slika_info_label  

        naziv_label = Label(nova_biljka, text='Naziv biljke: ')
        slika_label = Label(nova_biljka, text='Slika biljke: ')
        njega_label = Label(nova_biljka, text='Njega biljke: ')
        self.slika_info_label = Label(nova_biljka, text='Odabrana slika: ')

        naziv_entry = Entry(nova_biljka, textvariable=self.naziv_var)
        njega_entry = Entry(nova_biljka, textvariable=self.njega_var)
        upload_button = Button(nova_biljka, text='Upload slike', command=lambda: Biljke.ucitaj_sliku(self))

        naziv_label.place(x=20, y=50)
        njega_label.place(x=20, y=80)
        slika_label.place(x=15, y=120)
        naziv_entry.place(x=100, y=50)
        njega_entry.place(x=100, y=80)
        upload_button.place(x=80, y=120)
        self.slika_info_label.place(x=15, y=160)
        reg_biljke = Button(nova_biljka, text='Registracija biljke', command=lambda: self.registriraj_biljku(nova_biljka))
        reg_biljke.place(x=80, y=200)

        nova_biljka.mainloop()

        return self.biljke_instanca
    
    def ucitaj_sliku(self):
        if self.putanja_do_slike is None:
            self.putanja_do_slike = filedialog.askopenfilename(filetypes=[("Slike", "*.jpg *.png *.jpeg")])
            if self.slika_info_label: 
                self.slika_info_label.config(text=f'Odabrana slika: {self.putanja_do_slike}')

    def registriraj_biljku(self, nova_biljka):
        global naziv
        naziv = self.naziv_var.get()
        njega = self.njega_var.get()
        slika_bin = None

        if not naziv or not njega or not self.putanja_do_slike:
            return 

        with open(self.putanja_do_slike, "rb") as f:
            slika_bin = f.read()

        try:
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()

            query_insert = "INSERT INTO Tablica_biljke (naziv, njega, slika) VALUES (?, ?, ?)"
            cursor.execute(query_insert, (naziv, njega, slika_bin))
            connection.commit()
            
            nova_posuda(naziv, nova_biljka)

        except sqlite3.Error as e:
            print(f"Dogodila se pogreška pri spremanju podataka u bazu podataka: {e}")

        finally:
            if connection:
                connection.close()
                b_root.destroy()
        prozor_biljke()
        return True


#PROZOR ZA PRIKAZ POSUDA, FUNKCIONALNOSTI ZA PROZOR POSUDE I MANIPULISANJE TABLICA_POSUDE UNUTAR BAZA PODATAKA!!!!


def prozor_posude():
    global posuda_x, posuda_y, brojac, p_root, scrollbar, canvas, frame_posude

    p_root = Tk()
    p_root.title("Glavni prozor")
    p_root.geometry('600x400')

    scrollbar = Scrollbar(p_root, orient='vertical')
    scrollbar.pack(side='right', fill='y')

    canvas = Canvas(p_root, yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)

    frame_posude = Frame(canvas)
    canvas.create_window((0, 0), window=frame_posude, anchor='nw')

    scrollbar.config(command=canvas.yview)

    brisanje_button = Button(p_root, text='Obriši posudu!', command=brisanje_posude)
    brisanje_button.pack(side='top')

    prikazi_posude()

    p_root.mainloop()

def nova_posuda(naziv_biljke, nova_biljka):
    global posuda_x, posuda_y, p_root

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        query_insert_posuda = "INSERT INTO Tablica_posude (biljka_id) VALUES (?)"
        cursor.execute(query_insert_posuda, (naziv_biljke,))
        connection.commit()

    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri spremanju podataka u bazu podataka: {e}")

    finally:
        if connection:
            connection.close()

def prikazi_posude():
    global posuda_x, posuda_y, naziv_posude, frame_posude

    posuda_x = 15
    posuda_y = 50
    brojac = 0
    slike_tk_rj = {}

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        query_select_biljke = "SELECT * FROM Tablica_biljke"

        cursor.execute(query_select_biljke)

        biljke = cursor.fetchall()

        for biljka in biljke:
            if biljka[2]:
                slika_bin = biljka[2]
                slika_stream = io.BytesIO(slika_bin)

                try:
                    slika = Image.open(slika_stream)
                    slika.thumbnail((150, 150))

                    slika_tk = ImageTk.PhotoImage(slika)
                    slike_tk_rj[biljka[0]] = slika_tk

                except Exception as e:
                    print("Greška pri otvaranju slike:", e)
    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri dohvaćanju podataka iz baze podataka: {e}")

    finally:
        if connection:
            connection.close()

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        query_select_posude = "SELECT * FROM Tablica_posude"

        cursor.execute(query_select_posude)

        posude = cursor.fetchall()

        for posuda in posude:
            posuda_frame = Frame(frame_posude, width=300, height=200, bd=1, relief='solid')
            naziv_posude = Label(posuda_frame, text=f'Posuda za {posuda[1]}', font=('Times', 12, 'italic'))
            vise_button = Button(posuda_frame, text='Više o posudi', command=prosiri_posude, font=('Times', 12, 'italic'))
            posuda_frame.grid(row=brojac // 5, column=brojac % 5, padx=10, pady=10)
            brojac += 1

            slika_label = Label(posuda_frame, image=slike_tk_rj.get(posuda[0]))
            slika_label.image = slike_tk_rj.get(posuda[0])
            slika_label.place(x=15, y=15)
            naziv_posude.place(x=125, y=15)
            vise_button.place(x=200, y=165)

    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri dohvaćanju podataka iz baze podataka: {e}")

    finally:
        if connection:
            connection.close()

    canvas.update_idletasks()  # Osigurava da se canvas pravilno postavi
    canvas.config(scrollregion=canvas.bbox('all'))  # Omogućava pomicanje kroz cijeli sadržaj

def prosiri_posude():
    global vise_root
    vise_root = Tk()
    vise_root.geometry('950x500')

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        query_select_posude = "SELECT * FROM Tablica_posude"

        cursor.execute(query_select_posude)

        posude = cursor.fetchall()

        for posuda in posude:
            vlaznost_label = Label(vise_root, text=f'Vlaznost tla: {random.uniform(0, 100):.2f}%')
            svjetlost_label = Label(vise_root, text=f'Svjetlost: {random.uniform(0, 100):.2f}%')
            vlaga_zraka_label = Label(vise_root, text=f'Vlaga zraka: {random.uniform(0, 100):.2f}%')

            vlaznost_label.place(x=15, y=170)
            svjetlost_label.place(x=15, y=190)
            vlaga_zraka_label.place(x=15, y=210)

            prikazi_graf_button = Button(vise_root, text='Prikazi Grafove', command=lambda id=posuda[0]: prikazi_grafove(id))
            prikazi_graf_button.place(x=15, y=280)

    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri dohvaćanju podataka iz baze podataka: {e}")

    finally:
        if connection:
            connection.close()
            p_root.destroy()

    vise_root.mainloop()
    prozor_posude()

def prikazi_grafove(posuda_id):
    vlaznost_tla = [random.uniform(50, 100) for _ in range(10)]
    svjetlost = [random.uniform(50, 100) for _ in range(10)]
    vlaga_zraka = [random.uniform(50, 100) for _ in range(10)]

    draw_line_chart(vlaznost_tla, 'Vlaznost Tla')
    draw_pie_chart([svjetlost[-1], 100 - svjetlost[-1]], 'svjetlost')
    draw_histogram(vlaga_zraka, 'Vlaga zraka ')

def draw_line_chart(data, title):
    global vise_root
    figure, ax = plt.subplots()
    ax.plot(data)
    ax.set_title(title)
    ax.set_xlabel('Vrijeme')
    ax.set_ylabel('Vrijednost')

    figure.set_size_inches(3.5, 2)

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(8)

    canvas = FigureCanvasTkAgg(figure, master=vise_root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=200, y=65)
    plt.close()

def draw_pie_chart(data, title):
    global vise_root
    figure, ax = plt.subplots()
    ax.pie(data, labels=['Vrijednost', 'Preostalo'])
    ax.set_title(title)

    figure.set_size_inches(3.5, 2)

    for item in ([ax.title] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(8)

    canvas = FigureCanvasTkAgg(figure, master=vise_root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=580, y=65)
    plt.close()

def draw_histogram(data, title):
    global vise_root
    figure, ax = plt.subplots()
    ax.hist(data, bins=10, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Vrijednost')
    ax.set_ylabel('Broj uzoraka')

    figure.set_size_inches(3.5, 2)

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(8)

    canvas = FigureCanvasTkAgg(figure, master=vise_root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=390, y=280)
    plt.close()

def brisanje_posude():
    global posuda_listbox, frame_posude
    selected_index = posuda_listbox.curselection()
    if not selected_index:
        messagebox.showerror('Greška', 'Molimo odaberite posudu za brisanje!')
        return

    selected_posuda = posuda_listbox.get(selected_index)

    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        cursor.execute("SELECT posuda_id FROM Tablica_posude WHERE biljka_id=?", (selected_posuda,))
        result = cursor.fetchone()

        if result is not None:
            query_delete = '''DELETE FROM Tablica_posude WHERE biljka_id=?'''
            cursor.execute(query_delete, (selected_posuda,))
            connection.commit()
            messagebox.showinfo('Uspješno brisanje', f'Posuda za {selected_posuda} uspješno obrisana.')
        else:
            messagebox.showerror('Greška', 'Unijeli ste pogrešan naziv biljke za brisanje!')

    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri spajanju na SQLite bazu {e}")

    finally:
        if connection:
            connection.close()
            posuda_listbox.delete(0, 'end')  # Očisti listbox
            prikazi_posude()


#PROZOR ZA PRIKAZ BILJKA, FUNKCIONALNOSTI ZA PROZOR BILJKE I MANIPULISANJE TABLICA_BILJKE UNUTAR BAZA PODATAKA!!!!


def prozor_biljke():
    global b_root
    b_root = Tk()
    b_root.title("Glavni prozor")
    b_root.geometry('1700x900')
    
    biljke_instance = Biljke(b_root, height=250, width=500)
    Biljke.biljke_instanca = biljke_instance

    gumb_brisanje_biljke = Button(b_root, text='Brisanje biljke', command=brisanje_biljke)
    gumb_brisanje_biljke.place(x=120, y=15)
    
    start_button = Button(b_root, text="Nova biljka", command=Biljke.biljke_instanca.start_klasa_biljke)
    start_button.place(x=15,y=15)

    uredivanje_biljke_button = Button(b_root, text='Uređivanje biljke', command= uredi_biljku)
    uredivanje_biljke_button.place(x=220, y=15)
    prikazi_biljke()
    b_root.mainloop()
    return b_root

def brisanje_biljke():
    def izbrisi():
        entry_naziv_biljke = entry_naziv_biljke_var.get()

        try:
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()

            cursor.execute("SELECT naziv FROM Tablica_biljke WHERE naziv=?", (entry_naziv_biljke,))
            result = cursor.fetchone()
            if result:
                query_delete = '''DELETE FROM Tablica_biljke WHERE naziv=?'''
                cursor.execute(query_delete, (entry_naziv_biljke,))
                connection.commit()
                messagebox.showinfo('Uspješno brisanje', f'Biljka {entry_naziv_biljke} uspješno obrisana.')
            else:
                messagebox.showerror('Greška', 'Unijeli ste pogrešan naziv biljke za brisanje!')

        except sqlite3.Error as e:
            print(f"Dogodila se pogreška pri spajanju na SQLite bazu {e}")

        finally:
            if connection:
                connection.close()
                b_root.destroy()
        prozor_biljke()
        
    brisanje_biljke_window = Toplevel()
    brisanje_biljke_window.geometry('300x150')
    brisanje_biljke_window.title("Brisanje biljke")

    label_naziv_biljke = Label(brisanje_biljke_window, text="Naziv biljke za brisanje: ")
    label_naziv_biljke.place(x=15,y=50)

    entry_naziv_biljke_var = StringVar()
    entry_naziv_biljke = Entry(brisanje_biljke_window, textvariable=entry_naziv_biljke_var)
    entry_naziv_biljke.place(x=160, y=50)

    button_brisanje = Button(brisanje_biljke_window, text="Obriši biljku", command=izbrisi)
    button_brisanje.place(x=100, y=100)

    brisanje_biljke_window.mainloop()

nova_putanja_do_slike = None     
nova_slika_info_label = None

def ucitaj_novu_sliku():
    global nova_putanja_do_slike, nova_slika_info_label
    if nova_putanja_do_slike is None:
        nova_putanja_do_slike = filedialog.askopenfilename(filetypes=[("Slike", "*.jpg *.png *.jpeg")])
        if nova_slika_info_label: 
            nova_slika_info_label.config(text=f'Odabrana slika: {nova_putanja_do_slike}')

def novi_podaci():
        novi_naziv = novi_naziv_var.get()
        nova_njega = nova_njega_var.get()
        entry_biljke_uredivanje = stara_biljka_var.get()
        slika_bin = None

        if not novi_naziv or not nova_njega or not nova_putanja_do_slike:
            return 

        with open(nova_putanja_do_slike, "rb") as f:
            slika_bin = f.read()

        try:
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()

            cursor.execute("SELECT naziv FROM Tablica_biljke WHERE naziv=?", (entry_biljke_uredivanje,))
            result = cursor.fetchone()

            if result:
                connection = sqlite3.connect(database_name)
                cursor = connection.cursor()

                query_update = "UPDATE Tablica_biljke SET naziv=?, slika=?, njega=? WHERE naziv=?"
                cursor.execute(query_update, (novi_naziv, slika_bin, nova_njega, entry_biljke_uredivanje))
                connection.commit()
                messagebox.showinfo('Uspješno ažuriranje', f'Biljka {novi_naziv} uspješno ažurirana.')
            else:
                messagebox.showerror('Greška', 'Unijeli ste pogrešan naziv biljke za ažuriranje!')


        except sqlite3.Error as e:
            print(f"Dogodila se pogreška pri spremanju podataka u bazu podataka: {e}")

        finally:
            if connection:
                connection.close()
                b_root.destroy()
        prozor_biljke()
        return True

def uredi_biljku():
    global novi_naziv_var,nova_njega_var, stara_biljka_var,nova_slika_info_label

    uredivanje_biljke = Toplevel()
    uredivanje_biljke.geometry('400x300')
    uredivanje_biljke.title('Ažuriranje biljke')

    novi_naziv_var = StringVar()
    nova_njega_var = StringVar()
    stara_biljka_var = StringVar()

    label_stara_biljka = Label(uredivanje_biljke, text='Naziv biljke za ažuriratnje: ')
    entry_stara_biljka = Entry(uredivanje_biljke, textvariable= stara_biljka_var, width=35)
    novi_naziv_label = Label(uredivanje_biljke, text='Novi naziv biljke: ')
    nova_njega_label = Label(uredivanje_biljke, text='Nova njega biljke: ')
    nova_slika_info_label = Label(uredivanje_biljke, text='Odabrana slika: ')
    novi_naziv_entry = Entry(uredivanje_biljke, textvariable=novi_naziv_var, width=35)
    nova_njega_entry = Entry(uredivanje_biljke, textvariable=nova_njega_var, width=35)
    novi_upload_button = Button(uredivanje_biljke, text='Upload slike', command=ucitaj_novu_sliku)

    label_stara_biljka.place(x=20, y=50)
    novi_naziv_label.place(x=20, y=80)
    nova_njega_label.place(x=20, y=110)
    entry_stara_biljka.place(x=170,y=50)
    novi_naziv_entry.place(x=170, y=80)
    nova_njega_entry.place(x=170, y=110)
    novi_upload_button.place(x=20, y=150)
    nova_slika_info_label.place(x=20, y=190)

    novi_reg_biljke = Button(uredivanje_biljke, text='Uredi biljke', command=novi_podaci)
    novi_reg_biljke.place(x=150, y=230)

def prikazi_biljke():
    global b_root
            
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        query_select = "SELECT * FROM Tablica_biljke"
        cursor.execute(query_select)
        biljke = cursor.fetchall()

        for i, biljka in enumerate(biljke):
            redak = i // 5
            stupac = i % 5
                                
            vlaznost = random.randint(50,100)

            pady_top = 50 if redak == 0 else 15

            biljka_frame = Frame(b_root, width=300, height=200, bd=1, relief=SOLID)
            biljka_frame.grid(row=redak, column=stupac, padx=10, pady=(pady_top, 15))  

            naziv_label = Label(biljka_frame, text=f"Naziv: {biljka[1]}")
            naziv_label.grid(row=0, column=0, sticky="nw")  

            vlaznost_label = Label(biljka_frame, text=f'Vlaznost tla: {vlaznost}%')
            vlaznost_label.grid(row=2,column=1)

            njega_text = Text(biljka_frame, wrap=WORD, width=18, height=9)
            njega_text.grid(row=1, column=0, sticky="sw")  
            if biljka[3]:
                njega_text.insert(END, biljka[3])  
                njega_text.config(state=DISABLED)

            if biljka[2]:
                slika_bin = biljka[2]
                slika_stream = io.BytesIO(slika_bin)

                try:
                    slika = Image.open(slika_stream)
                    slika.thumbnail((150, 150))

                    slika_tk = ImageTk.PhotoImage(slika)

                    slika_label = Label(biljka_frame, image=slika_tk)
                    slika_label.image = slika_tk
                    slika_label.grid(row=0, column=1, rowspan=2, padx=5, pady=10,) 
                except Exception as e:
                    print("Greška pri otvaranju slike:", e)
    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri dohvatu biljaka iz baze: {e}")

    finally:
        if connection:
            connection.close()   
    
#prozor_biljke()