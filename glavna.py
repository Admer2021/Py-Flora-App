from tkinter import *
from baza_pod import *
from tkinter import messagebox
from klase import *
import io
from PIL import Image,ImageTk

baza = sqlite3.connect('Korisnici.db')
baza.execute(''' CREATE TABLE IF NOT EXISTS Tablica_korisnici (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password INTEGER,
                email TEXT NOT NULL
                )''')
cursor = baza.cursor()

loginroot = None

def login_window():
    inicijalizacija()

    global name_var
    global pass_var
    global ime_var
    global sifra_var
    global sifra2_var
    global email_var
    global loginroot

    loginroot = Tk()
    loginroot.geometry('600x400')
    loginroot.title("Login")

    name_var=StringVar()
    pass_var=StringVar()
    ime_var = StringVar()
    sifra_var = IntVar()
    sifra2_var = IntVar()
    email_var = StringVar()

    name_label = Label(loginroot, text='Korisnik: ', font=('Times', 12))
    pass_label = Label(loginroot, text='Šifra: ', font=('Times', 12))

    tekst1_label = Label(loginroot, text='Dobrodošli u aplikaciju PyFlora', font=('Times', 14, 'bold italic underline'))
    tekst2_label = Label(loginroot,text='Ukoliko niste registirani možete se registrirati klikom na gumb "Registracija"\nPoslije registracije potrebno je ponovno pokrenuti aplikaciju!\n\nPočetni korisnik:\nadmin\n2023', font=('Times', 10, 'bold italic underline'))
    tekst2_label.place(x=80,y=70)
    tekst1_label.place(x=160,y=15)

    name_entry = Entry(loginroot, width=30, textvariable=name_var)
    pass_entry = Entry(loginroot, width=30, textvariable=pass_var)

    login_button = Button(loginroot, text='Logiranje', width=15, command=logiranje)        
    reg_button = Button(loginroot, text='Registracija', width=15, command=registracija)   

    name_label.place(x=130, y=200)
    pass_label.place(x=130, y=230)
    name_entry.place(x=230, y=200)
    pass_entry.place(x=230, y=230)
    login_button.place(x=170, y=270)
    reg_button.place(x=300, y=270)

    mainloop()

def registracija():
    global regroot
    loginroot.destroy()
    regroot = Tk()
    regroot.geometry('400x300')

    ime_label = Label(regroot, text='Korisnik: ', font=('Calibri', 12))
    sifra_label = Label(regroot, text='Šifra: ', font=('Calibri', 12))
    sifra2_label = Label(regroot, text='Šifra: ', font=('Calibri', 12))
    email_label = Label(regroot, text='E-mail: ', font=('Calibri', 12))

    ime_entry = Entry(regroot, textvariable=ime_var, width=30)
    sifra_entry = Entry(regroot, textvariable=sifra_var, width=30)
    sifra2_entry = Entry(regroot, textvariable=sifra2_var, width=30)
    email_entry = Entry(regroot, textvariable=email_var, width=30)

    reg2_button = Button(regroot, text='Register', command= lambda:unos_u_bazu(ime_entry,sifra_entry,sifra2_entry,email_entry) , font=('Calibri', 12))   

    ime_label.place(x=30, y=50)
    sifra_label.place(x=30, y=80)
    sifra2_label.place(x=30, y=110)
    email_label.place(x=30,y=140)
    reg2_button.place(x=130, y=180)
    ime_entry.place(x=120, y=50)
    sifra_entry.place(x=120, y=80)
    sifra2_entry.place(x=120, y=110)
    email_entry.place(x=120, y=140)

    mainloop()
    login_window()
    inicijalizacija()

def unos_u_bazu(ime_var, sifra_var, sifra2_var, email_var):
    ime = ime_var.get()
    sifra = sifra_var.get()
    sifra2 = sifra2_var.get()
    email = email_var.get()

    if sifra == sifra2:
        baza.execute(f"INSERT INTO Tablica_korisnici (username, password, email) VALUES ('{ime}', '{sifra}', '{email}')")
        baza.commit()
        regroot.withdraw()
        login_window()
        name_var.set('')
        pass_var.set('')
        inicijalizacija()
        messagebox.showinfo("Uspješna registracija", "Registracija uspješna!")
    else:
        messagebox.showerror("Neuspješna registracija", "Lozinke se ne podudaraju! Molimo unesite istu lozinku u oba polja.")

    regroot.destroy()

mainroot= None
slika_tk_jedan = None


def otvori_glavni_prozor():
    global mainroot, slika_tk_jedan
    
    mainroot = Tk()
    mainroot.geometry('800x600')
    mainroot.title('Py Flora')

    inicijalizacija()
    
    naziv_app = Label(mainroot, text='PyFlora Aplikacija', font=('Times', 36, 'bold italic underline'))
    naziv_app.place(x=200, y=10)

    welcome_label = Label(mainroot, text=f'Dobrodošli {ime_log}', font=('Times', 12, 'bold italic underline'))
    welcome_label.place(x=15, y=100)

    biljka_label = Label(mainroot, text='Prikaz jedne biljke iz baze podataka:', font=('Times', 12, 'bold italic'))
    biljka_label.place(x=15,y=170)

    gumb_otvori_biljke = Button(mainroot, text='Prikaži Biljke', font=('Times', 12, 'italic'), command=prozor_biljke)
    gumb_otvori_biljke.place(x=40, y=400)

    gumb_otvori_posude = Button(mainroot, text='Prikaži Posude', font=('Times', 12, 'italic'), command=prozor_posude)
    gumb_otvori_posude.place(x=180, y=400)



    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        query_select = "SELECT * FROM Tablica_biljke ORDER BY id LIMIT 1"
        cursor.execute(query_select, )
        
        biljka = cursor.fetchone()

        vlaznost_biljka = random.randint(50,100)
        vlaznost_zraka = random.randint(50,100)
        toplina_biljka = random.randint(15,40)

        if biljka:

            jedna_biljka_frame = Frame(mainroot, width=400, height=300, bd=1, relief='solid')
            jedna_biljka_frame.place(x=15, y=230)

            naziv_label = Label(jedna_biljka_frame, text=f"Naziv: {biljka[1]}", font=('Times', 12, 'italic'))
            naziv_label.grid(row=0, column=0, sticky="nw")

            njega_label = Label(jedna_biljka_frame, text=f'Njega: {biljka[3]}', font=('Times', 12, 'italic'), width=33, wraplength=320)
            njega_label.grid(row=1, column=0, sticky="nw")

            tlo_label = Label(jedna_biljka_frame, text=f'Vlažnost tla u posudi: {vlaznost_biljka}%', font=('Times', 12, 'italic'))
            tlo_label.grid(row=2, column=0, sticky='nw')

            zrak_label = Label(jedna_biljka_frame, text=f'Vlažnost zraka u prostoriji: {vlaznost_zraka}%', font=('Times', 12, 'italic'))
            zrak_label.grid(row=3, column=0, sticky='nw')

            toplina_label = Label(jedna_biljka_frame, text=f'Trenutna temperatura u prostoriji: {toplina_biljka}C', font=('Times', 12, 'italic'))
            toplina_label.grid(row=4, column=0, sticky='nw')

        else:
            print(f"Biljka nije pronađena.")

    except sqlite3.Error as e:
        print(f"Dogodila se pogreška pri dohvatu biljke iz baze: {e}")

    finally:
        if connection:
            connection.close()
    
    prognoza_sutra()
    loginroot.destroy()

def logiranje():
    inicijalizacija()
    global ime_log
    ime_log = name_var.get()
    sifra_log = pass_var.get()

    cursor.execute("SELECT * FROM Tablica_korisnici WHERE username = ? AND password = ?", (ime_log, sifra_log))
    user_data = cursor.fetchone()
    if user_data:
        otvori_glavni_prozor()
        mainroot.mainloop()
        return True
        
    else:
        messagebox.showerror("Neuspješno logiranje", "Pogrešno korisničko ime ili lozinka!")
        return False

def prognoza_sutra():
    vlaznost = random.randint(0,100)
    temperatura = random.randint(20,35)
    tlak = random.randint(900,1100)
    #slika_kisa = Image.open('kisa1.jpg')
    #s_kisa = ImageTk.PhotoImage(slika_kisa)
    #slika_sunce = Image.open('vrijeme_sunce.jpg')
    #s_sunce = ImageTk.PhotoImage(slika_sunce)

    prognoza = Frame(mainroot, width=390, height=450, bd=1, relief=SOLID)
    naslov_label = Label(prognoza, text='Trenutna prognoza', font=('Times', 14, 'bold italic underline'))
    temp_label = Label(prognoza,text=f'Trenutna temperatura: {temperatura} C', font=('Times', 12, 'italic'))
    vlaznost_label = Label(prognoza, text=f'Vlažnost zraka: {vlaznost}%', font=('Times', 12, 'italic'))
    tlak_label = Label(prognoza,text=f'Tlak: {tlak}', font=('Times', 12, 'italic'))
    min_temp = Label(prognoza, text='Minimalna temperatura: 20 C', font=('Times', 12, 'italic'))
    maks_temp= Label(prognoza, text='Maksimalna temperatura: 35 C', font=('Times', 12, 'italic'))
    vlaznost75 = Label(prognoza,text='Trenutno je velika mogućnost za kišu, ponesite kišobran!', font=('Times', 12, 'italic'))
    vlaznost0 = Label(prognoza,text='Trenutno je sunčano, pazite na veliku izloženost sunca', font=('Times', 12, 'italic'))
    #kisa_label = Label(prognoza, image=s_kisa)
    #sunce_label = Label(prognoza, image=s_sunce)
    if vlaznost>=75:
        vlaznost75.place(x=15,y=230)
        #kisa_label.place(x=15, y=260)
    else:
        vlaznost0.place(x=15,y=230)
        #sunce_label.place(x=15, y=260)

    naslov_label.place(x=120,y=15)
    prognoza.place(x=400, y=100)
    temp_label.place(x=15,y=80)
    vlaznost_label.place(x=15,y=110)
    tlak_label.place(x=15,y=140)
    min_temp.place(x=15,y=170)
    maks_temp.place(x=15,y=200)

login_window()