from tkinter import *
from timeit import default_timer
import datetime
from RPi import GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

temp1 = 0
temp2 = 0

pins = [2, 3, 4, 5]

for i in range(0, len(pins)):
    GPIO.setup(pins[i], GPIO.IN)
    print(pins[i])

historique = []
debut_partie = False
tour_joueur = 1
liste_init = [
        ["wR", "wN", "wB", "wK", "wQ", "wP", "wN", "wR"],
        ["wP", "wP", "wP", "wP", "wP", 0, "wP", "wP"],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"]
        ]

liste_pins = [
        [0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
        ]

liste_init_interpin = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
] # Liste des positions intersection pins disponibles

liste_pins_init = [
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]    
] # Liste des valeurs lues pas les pins disponibles

liste1 = []

for i in range(0, len(liste_pins)):
    for j in range(0, len(liste_pins[i])):
        if liste_pins[i][j] != 0:
            liste_init_interpin[i][j] = liste_init[i][j]
        else:
            liste_init_interpin[i][j] = 0

def init_partie():

    global debut_partie

    if (debut_partie==False):
        debut_partie = True

def tour():

    global tour_joueur

    if(tour_joueur==1):
        tour_joueur=2
    else:
        tour_joueur=1

def updateTime():
    global temp1
    global temp2

    if(tour_joueur==1):
        now1 = default_timer() - start - temp2
        minutes1, seconds1 = divmod(now1, 60)
        hours1, minutes1 = divmod(minutes1, 60)
        str_time1 = "%d:%02d:%02d" % (hours1, minutes1, seconds1)
        canvas1.itemconfigure(text_clock1, text=str_time1)
        temp1 = now1


    else:
        now2 = default_timer() - start - temp1
        minutes2, seconds2 = divmod(now2, 60)
        hours2, minutes2 = divmod(minutes2, 60)
        str_time2 = "%d:%02d:%02d" % (hours2, minutes2, seconds2)
        canvas2.itemconfigure(text_clock2, text=str_time2)
        temp2 = now2

    fenetre.after(1000, updateTime)

def positionInitiale(liste1, liste2):
    for i in range(0, len(liste1)):
        for j in range(0, len(liste1[i])):
            if (liste1[i][j] == 1):
                if (liste2[i][j] == 0):
                    returnArray = [i,j]
                    return returnArray
            
def positionFinale(liste1, liste2):
    for i in range(0, len(liste1)):
        for j in range(0, len(liste1[i])):
            if (liste1[i][j] == 0):
                if (liste2[i][j] == 1):
                    returnArray = [i,j]
                    return returnArray
    return None

def typePiece(liste):
    global liste_init
    return liste_init[liste[0]][liste[1]]

def updateHisto():
    global liste_pins_init
    global tour_joueur
    global historique
    liste_coordonnees_finale = [-1, -1]
    liste1 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]    
]
    
    for i in range(0, len(liste_pins)):
        for j in range(0, len(liste_pins[i])):
            if liste_pins[i][j] != 0:
                liste1[i][j] = GPIO.input(liste_pins[i][j])
            else:
                liste1[i][j] = 0
    
    for i in liste1:
        print(i)
    if liste_pins_init == liste1:
        print(historique)
    else:
        print(historique)
        liste_coordonnees = positionInitiale(liste_pins_init, liste1)
        liste_coordonnees_finale = positionFinale(liste_pins_init, liste1)
        while liste_coordonnees_finale == None:
            for i in range(0, len(liste_pins)):
                for j in range(0, len(liste_pins[i])):
                    if liste_pins[i][j] != 0:
                        liste1[i][j] = GPIO.input(liste_pins[i][j])
                    else:
                        liste1[i][j] = 0
            liste_coordonnees_finale = positionFinale(liste_pins_init, liste1)
        print(liste_coordonnees_finale)
        piece = typePiece(liste_coordonnees)
        if "P" in piece:
            liste_init[liste_coordonnees_finale[0]][liste_coordonnees_finale[1]] = liste_init[liste_coordonnees[0]][liste_coordonnees[1]]
            liste_init[liste_coordonnees[0]][liste_coordonnees[1]] = 0
            historique.append(chr(liste_coordonnees_finale[1] + 97) + str(liste_coordonnees_finale[0] + 1))
        liste_pins_init = liste1[:]

    canvas3.itemconfigure(cantext, text = liste_pins_init[0])
    canvas4.itemconfigure(cantext1, text = liste_pins_init[1])
    canvas5.itemconfigure(cantext2, text = liste_pins_init[2])
    canvas6.itemconfigure(cantext3, text = liste_pins_init[3])
    canvas7.itemconfigure(cantext4, text = liste_pins_init[4])
    canvas8.itemconfigure(cantext5, text = liste_pins_init[5])
    canvas9.itemconfigure(cantext6, text = liste_pins_init[6])
    canvas10.itemconfigure(cantext7, text = liste_pins_init[7])
    
    fenetre.after(2000, updateHisto)
    
var = 0
name1 = ""
name2 = ""

def save_name():

    global var
    global name1
    global name2
    if var == 0:
        var = 1
    else:
        var = 0
        
    if var == 1:
        name1 = ent1.get()
        name2 = ent2.get()
        var = 0
        
    print(name1)
    print(name2)
        
    fenetre1.destroy()
    

fenetre1 = Tk()
fenetre1.title("Bienvenue")

var1 = StringVar()
var1.set("Joueur 1")
var2 = StringVar()
var2.set("Joueur 2")
ent1 = Entry(fenetre1, textvariable = var1)
ent1.pack(side = BOTTOM)
ent2 = Entry(fenetre1, textvariable = var2)
ent2.pack(side = BOTTOM)
butt0 = Button(fenetre1, text = "Save", command = save_name).pack(side = RIGHT)
lab = Label(fenetre1, text = "Entrez les noms des joueurs").pack(side = TOP)


    
fenetre1.mainloop()

def save_pgn(moves, winner, filename, name1, name2):
    print(moves)
    now = datetime.datetime.now()
    if now.month < 10:
        month_str = "0" + str(now.month)
    else:
        month_str = str(now.month)
    if now.day < 10:
        day_str = "0" + str(now.day)
    else:
        day_str = str(now.day)

    date_header = "Date" + " \"" + str(now.year) + "." + month_str + "." + day_str + "\""
    headers = ["Event \"?\"", "Site \"?\"", "Round \"?\"", "White \""+ name1 +"\"", "Black \"" + name2 + "\""]
    headers.append(date_header)

    if winner is None:
        headers.append("Result \"*\"")
    elif winner == 0:
        headers.append("Result \"1-0\"")
    elif winner == 1/2:
        headers.append("Result \"1/2-1/2\"")
    else:
        headers.append("Result \"0-1\"")

    file_saved = open(filename, "w+")
    for i in headers:
        file_saved.write(i)
        file_saved.write("\n")

    file_saved.write("\n")

    compteur = 1
    for i in range(0, len(moves)):
        if i % 2 == 0:
            file_saved.write(str(compteur) + ". ")
            compteur += 1
            if i + 1 < len(moves):
                file_saved.write(moves[i] + " " + moves[i + 1])
            else:
                file_saved.write(moves[i])
            file_saved.write("\n")


fenetre = Tk()
fenetre.title('Chess_Saver')

frame1 = Frame(fenetre, borderwidth = 2) ##POUR LES BOUTONS/HISTORIQUE/TEMPS
frame1.pack(side = RIGHT)
frame2 = Frame(fenetre, borderwidth = 2) ##POUR LES PIECES D ECHEC
frame2.pack(side = LEFT)
frame3 = LabelFrame(frame1, text = 'Historique', padx = 60)
frame3.pack(side = BOTTOM)
frame4 = Frame(frame1, padx = 60)
frame4.pack(side = LEFT)
frame5 = Frame(frame1, padx = 60)
frame5.pack(side = RIGHT)

canvas3 = Canvas(frame2,height = 30, width = 200)
canvas3.pack()
canvas4 = Canvas(frame2,height = 30, width = 200)
canvas4.pack()
canvas5 = Canvas(frame2,height = 30, width = 200)
canvas5.pack()
canvas6 = Canvas(frame2,height = 30, width = 200)
canvas6.pack()
canvas7 = Canvas(frame2,height = 30, width = 200)
canvas7.pack()
canvas8 = Canvas(frame2,height = 30, width = 200)
canvas8.pack()
canvas9 = Canvas(frame2,height = 30, width = 200)
canvas9.pack()
canvas10 = Canvas(frame2,height = 30, width = 200)
canvas10.pack()


bouton1 = Button(frame1, text = 'Tour Joueur', command = tour, width = 30)
bouton1.pack(side = BOTTOM)
but01 = Button(frame1, text = "Save", command = lambda: save_pgn(historique, None,"save.pgn", name1, name2))
but01.pack()
but02 = Button(frame1, text = "Quitter", command = fenetre.destroy)
but02.pack()


Label(frame4, text = name1).pack(side = TOP)
Label(frame5, text = name2).pack(side = TOP)
canvas1 = Canvas(frame4)
canvas1.pack(side = LEFT)
canvas2 = Canvas(frame5)
canvas2.pack(side = RIGHT)

text_clock1 = canvas1.create_text(40, 20)
text_clock2 = canvas2.create_text(40, 20)
start = default_timer()

updateTime()

cantext = canvas3.create_text(60, 10)
cantext1 = canvas4.create_text(60, 10)
cantext2 = canvas5.create_text(60, 10)
cantext3 = canvas6.create_text(60, 10)
cantext4 = canvas7.create_text(60, 10)
cantext5 = canvas8.create_text(60, 10)
cantext6 = canvas9.create_text(60, 10)
cantext7 = canvas10.create_text(60, 10)


updateHisto()

Label(frame3, text = 'Mouvement').pack()

fenetre.mainloop()
