#Author: Andrzej Serwotka

from tkinter import *
from tkinter import ttk
from pathlib import Path
import shlex
import subprocess
import _thread
import os

root = Tk()
root.minsize(width=640, height=480)
root.maxsize(width=640, height=480)

filedropboxuploader = open('dropbox_uploader_path.txt', 'r')
dropboks_app_path = filedropboxuploader.read().strip()

#Ustawiania dotyczące okna
root.title("PyBoxer")
mainframe = ttk.Frame(root, padding="0 0 0 0", width=640, height=480)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.grid_columnconfigure(0, weight=1)
mainframe.grid_rowconfigure(0, weight=2)
mainframe.grid_rowconfigure(1, weight=1)
mainframe.grid_rowconfigure(2, weight=1)
mainframe.grid_propagate(0)

framewithlists = ttk.Frame(mainframe, relief=SUNKEN)
framewithlists.grid_rowconfigure(0, weight=1)
framewithlists.grid_rowconfigure(1, weight=10)
framewithlists.grid_rowconfigure(2, weight=1)
framewithlists.grid_columnconfigure(0, weight=14)
framewithlists.grid_columnconfigure(1, weight=1)
framewithlists.grid_columnconfigure(2, weight=14)
framewithlists.grid_columnconfigure(3, weight=1)
framewithlists.grid(column=0, row=0, sticky=(N, W, E, S))
framewithlists.grid_propagate(0)


labellocal = ttk.Label(framewithlists, text='Pliki lokalne')
labellocal.grid(row=0, column=0)

labelremote = ttk.Label(framewithlists, text='Pliki zdalne')
labelremote.grid(row=0, column=2)

#Pole na pliki lokalne
xscrollbarlocal = Scrollbar(framewithlists, orient=HORIZONTAL)
xscrollbarlocal.grid(row=2, column=0, sticky=E+W+N)

yscrollbarlocal = Scrollbar(framewithlists)
yscrollbarlocal.grid(row=1, column=1, sticky=N+S+W)

locallist = Listbox(framewithlists, yscrollcommand = yscrollbarlocal.set, xscrollcommand = xscrollbarlocal.set )
locallist.grid(row=1, column=0, sticky=N+S+E+W)

xscrollbarlocal.config(command=locallist.xview)
yscrollbarlocal.config(command=locallist.yview)

#Pole na pliki na dysku
xscrollbarremote = Scrollbar(framewithlists, orient=HORIZONTAL)
xscrollbarremote.grid(row=2, column=2, sticky=E+W+N )

yscrollbarremote = Scrollbar(framewithlists)
yscrollbarremote.grid(row=1, column=3, sticky=N+S+W)

remotelist = Listbox(framewithlists, yscrollcommand = yscrollbarremote.set, xscrollcommand = xscrollbarremote.set)
remotelist.grid(row=1, column=2, sticky=N+S+E+W)

xscrollbarremote.config(command=remotelist.xview)
yscrollbarremote.config(command=remotelist.yview)

###################################################################

def callback():
    print ("click!")
    #Dodaje element na koniec listy
    remotelist.insert(END, "DODANO")
	#Usuwa aktualnie zaznaczony element z listy
    print(remotelist.get(ANCHOR))

framewithbuttons = ttk.Frame(mainframe, relief=SUNKEN)
framewithbuttons.grid_rowconfigure(0, weight=1)
framewithbuttons.grid_rowconfigure(1, weight=1)
framewithbuttons.grid_columnconfigure(0, weight=1)
framewithbuttons.grid_columnconfigure(1, weight=1)
framewithbuttons.grid_columnconfigure(2, weight=1)
framewithbuttons.grid(column=0, row=1, sticky=(N, W, E, S))
framewithbuttons.grid_propagate(0)

#Pole na konsolę
framewithconsole = ttk.Frame(mainframe, relief=SUNKEN)
framewithconsole.grid(column=0, row=2, sticky=(N, W, E, S))
framewithconsole.grid_columnconfigure(0, weight=18)
framewithconsole.grid_columnconfigure(1, weight=1)
framewithconsole.grid_rowconfigure(0, weight=6)
framewithconsole.grid_rowconfigure(1, weight=1)
framewithconsole.grid_propagate(0)

xscrollbarconsole = Scrollbar(framewithconsole, orient=HORIZONTAL)
xscrollbarconsole.grid(row=1, column=0, sticky=E+W+N)

yscrollbarconsole = Scrollbar(framewithconsole)
yscrollbarconsole.grid(row=0, column=1, sticky=N+S+W)

consolelist = Listbox(framewithconsole, yscrollcommand = yscrollbarconsole.set, xscrollcommand = xscrollbarconsole.set )
consolelist.grid(row=0, column=0, sticky=N+S+E+W)

xscrollbarconsole.config(command=consolelist.xview)
yscrollbarconsole.config(command=consolelist.yview)
##################################################################################

#Funkcja sprawdza, czy jest zapisana jakaś ostatnia lokalna ścieżka
#Jeżeli jest, to zwraca ją jako string
#Jeżel nie, to zapisuje do pliku ścieżkę lokalną użytkownika i zwraca ją jako string
def lastlocalpathdir():
	localdirpath = Path('LocalDirPath.txt')
	file = None
	path = None
	global consolelist
	if not localdirpath.is_file():
		file = open('LocalDirPath.txt', 'w')
		file.write(str(Path.home()))
		path = str(Path.home())
		return path
	else:
		file = open('LocalDirPath.txt', 'r')
		path = file.read()
		return path

#Funkcja zwracająca listę plików z podanej ścieżki
def listlocalfilestoleftpanel(pathstr):
	global locallist
	files = os.listdir(pathstr)
	for e in files:
		locallist.insert(END, e)

#Funkcja wyłączająca możliwość użycia przycisków
def disablebuttons():
	buttonopendir.config(state="disabled")
	buttongoback.config(state="disabled")
	buttondelete.config(state="disabled")
	buttondownload.config(state="disabled")
	buttonupload.config(state="disabled")
	buttonrefresh.config(state="disabled")	

#Funkcja włączająca możliwość użycia przycisków
def enablebuttons():
	buttonopendir.config(state="normal")
	buttongoback.config(state="normal")
	buttondelete.config(state="normal")
	buttondownload.config(state="normal")
	buttonupload.config(state="normal")
	buttonrefresh.config(state="normal")

#Funkcja listująca pliki zdalne do prawego panelu
def listremotefilestorightpanel():

	disablebuttons()

	global remotelist
	global consolelist
	global dropboks_app_path
	current_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(dropboks_app_path)

	with open(current_path + "/" + "listing_output.txt", "w+") as output:
		subprocess.call(["./dropbox_uploader.sh", "list"], stdout=output)

	os.chdir(current_path)
	with open('listing_output.txt') as f:
		next(f)
		for line in f:
			line = line.strip()
			line = line.split(' ', 1)[1]
			line = line.split(' ', 1)[1].strip()
			remotelist.insert(END, line)

	consolelist.yview(END)

	enablebuttons()

#Funkcja odświeżająca oba panele
def refresh():
	global locallist
	global remotelist
	global consolelist

	consolelist.yview(END)

	locallist.delete(0, END)
	remotelist.delete(0, END)

	_thread.start_new_thread(listremotefilestorightpanel, ())
	listlocalfilestoleftpanel(lastlocalpathdir())

	file = open('LocalDirPath.txt', 'r')
	currentpath = file.read().strip()
	file.close()
	consolelist.insert(END, 'Obecna lokalna ścieżka: ' + currentpath)
	consolelist.yview(END)
	appjuststarted = False

#Funkcja otwierająca katalog i wypisująca jego zzawartość do
#lewego panelu
def opendir():
	global locallist
	global consolelist
	currentlocalpath = lastlocalpathdir()
	current_path = os.path.dirname(os.path.abspath(__file__))

	os.chdir(currentlocalpath)
	nextlocaldirstr = Path(locallist.get(ANCHOR))

	if not nextlocaldirstr.is_dir():
		os.chdir(current_path)
		consolelist.insert(END, 'Nie wybrano folderu!')
		consolelist.yview(END)
	else:
		if not currentlocalpath == '/':
			nextlocaldirpath = Path(currentlocalpath + '/' + str(nextlocaldirstr))
		else:
			nextlocaldirpath = Path(currentlocalpath + str(nextlocaldirstr))
		os.chdir(current_path)
		file = open('LocalDirPath.txt', 'w')
		file.write(str(nextlocaldirpath))
		file.close()
	refresh()

#Funkcja otwierająca wyższy katalog w drzewie katalogów - o ile jest to możliwe
def previousdir():
	global consolelist
	currentlocalpath = lastlocalpathdir()
	current_path = os.path.dirname(os.path.abspath(__file__))
	if str(currentlocalpath) == '/':
		consolelist.insert(END, 'Folder "/" - nie można bardziej cofnąć!')
		consolelist.yview(END)
	else:
		path = Path(currentlocalpath).parent
		file = open('LocalDirPath.txt', 'w')
		file.write(str(path))
		file.close()
		refresh()

#Funkcja uruchamiająca wątek wysyłanie plików na dropboksa
def upload():
	_thread.start_new_thread(startupload, ())

#Funkcja wysyłająca pliki na dropboksa
def startupload():
	global dropboks_app_path
	global locallist

	disablebuttons()

	currentlocalpath = lastlocalpathdir()
	current_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(dropboks_app_path)

	with open(current_path + "/" + "uploading_output.txt", "w+") as output:
		subprocess.call(["./dropbox_uploader.sh", "upload", currentlocalpath + '/' + locallist.get(ANCHOR), remotelist.get(ANCHOR)], stdout=output)

	os.chdir(current_path)

	with open('uploading_output.txt', 'r') as f:
		putoutputtoconsole(f)

	enablebuttons()
	refresh()

#Funkcja uruchamiająca wątek pobierania plików z dropboksa
def download():
	_thread.start_new_thread(startdownload, ())

#Funkcja pobierająca pliki z dropboksa
def startdownload():
	global dropboks_app_path
	global remotelist

	disablebuttons()

	currentlocalpath = lastlocalpathdir()
	current_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(dropboks_app_path)

	with open(current_path + "/" + "downloading_output.txt", "w+") as output:
		subprocess.call(["./dropbox_uploader.sh", "download", remotelist.get(ANCHOR), currentlocalpath + '/' + remotelist.get(ANCHOR)], stdout=output)

	os.chdir(current_path)

	with open('downloading_output.txt', 'r') as f:
		putoutputtoconsole(f)

	enablebuttons()
	refresh()

#Funkcja uruchamiająca wątek usuwania plików z dropboksa
def delete():
	_thread.start_new_thread(startdelete, ())

#Funkcja usuwająca pliki z dropboksa
def startdelete():
	global dropboks_app_path
	global remotelist

	disablebuttons()

	currentlocalpath = lastlocalpathdir()
	current_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(dropboks_app_path)

	with open(current_path + "/" + "deleting_output.txt", "w+") as output:
		subprocess.call(["./dropbox_uploader.sh", "delete", remotelist.get(ANCHOR)], stdout=output)

	os.chdir(current_path)

	with open('deleting_output.txt', 'r') as f:
		putoutputtoconsole(f)

	enablebuttons()
	refresh()

#Funkcja wypisująca output na konsolę (dolną listę)
def putoutputtoconsole(file):
	global consolelist
	first_line = file.readline().strip()
	consolelist.insert(END, '[OUTPUT] ' + first_line)
	consolelist.yview(END)

##################################################################################

#Przyciski

#Przycisk otwierania folderu
buttonopendir = Button(framewithbuttons,text="Otwórz katalog", command=opendir)
buttonopendir.grid(row=0,column=0, sticky=N+S+E+W)

#Przysisk przechodzenia do poprzedniego folderu
buttongoback = Button(framewithbuttons,text="Poprzedni katalog", command=previousdir)
buttongoback.grid(row=0,column=1, sticky=N+S+E+W)

#Przycisk usuwania zaznaczonego pliku lub folderu
buttondelete = Button(framewithbuttons,text="Usuń zdalny plik", command=delete)
buttondelete.grid(row=0,column=2, sticky=N+S+E+W)

#Przycisk pobierania zaznaczonego pliku lub folderu
buttondownload = Button(framewithbuttons,text="Pobierz", command=download)
buttondownload.grid(row=1,column=0, sticky=N+S+E+W)

#Przycisk wysyłania zaznaczonego pliku lub folderu
buttonupload = Button(framewithbuttons,text="Wyślij", command=upload)
buttonupload.grid(row=1,column=1, sticky=N+S+E+W)

#Przycisk odświeżania
buttonrefresh = Button(framewithbuttons,text="Odśwież", command=refresh)
buttonrefresh.grid(row=1,column=2, sticky=N+S+E+W)

refresh()

root.focus_set() # <-- move focus to this widget
root.mainloop()
