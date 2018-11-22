# coding: latin1
import string
import time
import urllib
import math
import copy
from sets import Set
from itertools import permutations
from itertools import combinations_with_replacement
import sys


# Worum geht es hier? Ein Quick_and_Dirty Schachprogramm.py

# Ideen: 
# Erst alle Vorwärtszüge, dann alle Rechtszüge ... so wird das Abbrechen nach einer Figur im Weg oder einem Schlagfall einfacher. Problem: Dame?
# Alpha-Beta-Pruning durch ein dictionary - da muss ich mir überlegen, welche Zugfolgen nicht vertauschbar sind. 
# Am einfachsten: Alle Zugfolgen mit Schlagzügen bleiben unvertauscht und ungeprunt. 
# Wie speichere ich das Brett? Geschachtelte Listen? Dictionary[a1]=T, Dictionary[(a,1)]=4.5 ? Listen.
# Am besten ist sicherlich ich definiere eine Brett-Klasse, die von list erbt. Dann lerne ich vielleicht noch was.
# Brettaufbauen ist dann eine Methode, Zugausführen, etc
# Und es gibt eine Variable Schlagzug = War der letzte Zug ein Schlagzug? Die Stellungsbewertung macht bei Schlagzug==True eine Bewertung 
# aller Gegenzüge statt der direkten Stellungsbewertung --> Schlagzugfolgen werden immer bis zum Ende gerechnet.
# Bei einer neuen Stellung ist das nicht relevant, nur am Ende von Varianten.

# Partie-Klasse mit Brett(-Klasse) und Brettdaten: Schlagzug, Rochaderechte, 50-Move-Regel, ...
# Übersichtlichere Brettausgabe mittels ANSII-Art - eingeben mit """ """ und dann schauen welche Indices welche Felder sind.
# Geht auch noch mehr ANSII-Art: Anfangs-Logo, Trophy am Ende, non-verbale Kommunikation, etc
# Vielleicht auch Partievorführung? Und Partiespeicherung. Am besten beides in externen Dateien. Eines Tages in Pgn.

# Umwandlung separat vor der restlichen Berechnung prüfen: Kann irgendein Bauer umgewandelt werden --> Vorrausberechnung dieses Zuges
# Spätere Berechnung um zu schauen ob Nicht-Umwandlungszüge den Wert noch übertreffen.

# Alles in ein Modul und nur das was gerade geschrieben wird in ein Test.py
# Alg mit Alpha-Beta erstmal mit Mühle testen.
# Schon das Durchgehen aller Zugfolgen vermeiden oder nur das Bewerten der Endstellung? Erstmal Laufzeit testen.
# In C statt dictionary ein PrefixTrie durch alle Felder und Stellungsdaten?

# Suchtiefe abhängig von Zuganzahl.
# Besten Zug noch mal weiter rechnen?

# Stellungsbewertung: Nicht vergessen Rochaderecht miteinzubeziehen.

# Zug-Rücknahme-Methode wichtig. Und am einfachsten durch Speicherung des Partie-Verlaufs.

# Figurenwert zu Figurenchar Konvertierungen
Wert_Char={}
Wert_Char[4.5]='T'
Wert_Char[3]='S'
Wert_Char[3.5]='L'
Wert_Char[8]='D'
Wert_Char[300]='K'
Wert_Char[1]='B'
Wert_Char[-4.5]='t'
Wert_Char[-3]='s'
Wert_Char[-3.5]='l'
Wert_Char[-1]='b'
Wert_Char[-8]='d'
Wert_Char[-300]='k'
Wert_Char[0]='0'

Char_Wert={}
Char_Wert['B']=1
Char_Wert['S']=3
Char_Wert['L']=3.5
Char_Wert['T']=4.5
Char_Wert['D']=8
Char_Wert['K']=300
Char_Wert['b']=-1
Char_Wert['s']=-3
Char_Wert['l']=-3.5
Char_Wert['t']=-4.5
Char_Wert['d']=-8
Char_Wert['k']=-300

# Alg-Not zu Koordinaten:
Alg_Koord={}
Alg_Koord['a1']=(0,0)
Alg_Koord['a2']=(0,1)
Alg_Koord['a3']=(0,2)
Alg_Koord['a4']=(0,3)
Alg_Koord['a5']=(0,4)
Alg_Koord['a6']=(0,5)
Alg_Koord['a7']=(0,6)
Alg_Koord['a8']=(0,7)

Alg_Koord['b1']=(1,0)
Alg_Koord['b2']=(1,1)
Alg_Koord['b3']=(1,2)
Alg_Koord['b4']=(1,3)
Alg_Koord['b5']=(1,4)
Alg_Koord['b6']=(1,5)
Alg_Koord['b7']=(1,6)
Alg_Koord['b8']=(1,7)

Alg_Koord['c1']=(2,0)
Alg_Koord['c2']=(2,1)
Alg_Koord['c3']=(2,2)
Alg_Koord['c4']=(2,3)
Alg_Koord['c5']=(2,4)
Alg_Koord['c6']=(2,5)
Alg_Koord['c7']=(2,6)
Alg_Koord['c8']=(2,7)

Alg_Koord['d1']=(3,0)
Alg_Koord['d2']=(3,1)
Alg_Koord['d3']=(3,2)
Alg_Koord['d4']=(3,3)
Alg_Koord['d5']=(3,4)
Alg_Koord['d6']=(3,5)
Alg_Koord['d7']=(3,6)
Alg_Koord['d8']=(3,7)

Alg_Koord['e1']=(4,0)
Alg_Koord['e2']=(4,1)
Alg_Koord['e3']=(4,2)
Alg_Koord['e4']=(4,3)
Alg_Koord['e5']=(4,4)
Alg_Koord['e6']=(4,5)
Alg_Koord['e7']=(4,6)
Alg_Koord['e8']=(4,7)

Alg_Koord['f1']=(5,0)
Alg_Koord['f2']=(5,1)
Alg_Koord['f3']=(5,2)
Alg_Koord['f4']=(5,3)
Alg_Koord['f5']=(5,4)
Alg_Koord['f6']=(5,5)
Alg_Koord['f7']=(5,6)
Alg_Koord['f8']=(5,7)

Alg_Koord['g1']=(6,0)
Alg_Koord['g2']=(6,1)
Alg_Koord['g3']=(6,2)
Alg_Koord['g4']=(6,3)
Alg_Koord['g5']=(6,4)
Alg_Koord['g6']=(6,5)
Alg_Koord['g7']=(6,6)
Alg_Koord['g8']=(6,7)

Alg_Koord['h1']=(7,0)
Alg_Koord['h2']=(7,1)
Alg_Koord['h3']=(7,2)
Alg_Koord['h4']=(7,3)
Alg_Koord['h5']=(7,4)
Alg_Koord['h6']=(7,5)
Alg_Koord['h7']=(7,6)
Alg_Koord['h8']=(7,7)

Koord_Alg=[]
Koord_Alg.append(['a','b','c','d','e','f','g','h'])
Koord_Alg.append(range(1,9))

# Leere Felder:
W_Feld=["       ","       ","       ","       "]
S_Feld=[".......",".......",".......","......."]
Feld=[S_Feld,W_Feld]
# Die Figuren als Liste von  vier Strings:
W_Bauer_WF=["   _   ","  ( )  ","  / \  "," (___) "]
W_Bauer_SF=["..._...","..( )..","../ \..",".(___)."]
W_Bauer=[W_Bauer_SF,W_Bauer_WF]
	
S_Bauer_WF=["   _   ","  (#)  ","  /#\  "," (###) "]
S_Bauer_SF=["..._...","..(#)..","../#\..",".(###)."]
S_Bauer=[S_Bauer_SF,S_Bauer_WF]

W_Turm_WF=[" [_|_] ","  [ ]  ","  [ ]  "," (___) "]
W_Turm_SF=[".[_|_].","..[ ]..","..[ ]..",".(___)."]
W_Turm=[W_Turm_SF,W_Turm_WF]

S_Turm_WF=[" [_|_] ","  [#]  ","  [#]  "," (###) "]
S_Turm_SF=[".[_|_].","..[#]..","..[#]..",".(###)."]
S_Turm=[S_Turm_SF,S_Turm_WF]

W_Springer_WF=["  ,-/| "," /_ )\ ","  / /\ "," (___) "]
W_Springer_SF=["..,-/|.","./_ )\.","../ /\.",".(___)."]
W_Springer=[W_Springer_SF,W_Springer_WF]

S_Springer_WF=["  ,-/| "," /_#)\ ","  /#/\ "," (###) "]
S_Springer_SF=["..,-/|.","./_#)\.","../#/\.",".(###)."]
S_Springer=[S_Springer_SF,S_Springer_WF]

W_Laeufer_WF=["  /|\  ","  \ /  ","  | |  "," (___) "]
W_Laeufer_SF=["../|\..","..\ /..","..| |..",".(___)."]
W_Laeufer=[W_Laeufer_SF,W_Laeufer_WF]

S_Laeufer_WF=["  /|\  ","  \#/  ","  |#|  "," (###) "]
S_Laeufer_SF=["../|\..","..\#/..","..|#|..",".(###)."]
S_Laeufer=[S_Laeufer_SF,S_Laeufer_WF]

W_Dame_WF=["  \*/  ","  ( )  ","  ) (  "," (___) "]
W_Dame_SF=["..\*/..","..( )..","..) (..",".(___)."]
W_Dame=[W_Dame_SF,W_Dame_WF]

S_Dame_WF=["  \*/  ","  (#)  ","  )#(  "," (###) "]
S_Dame_SF=["..\*/..","..(#)..","..)#(..",".(###)."]
S_Dame=[S_Dame_SF,S_Dame_WF]

W_Koenig_WF=["  \+/  ","  [ ]  ","  [ ]  "," (___) "]
W_Koenig_SF=["..\+/..","..[ ]..","..[ ]..",".(___)."]
W_Koenig=[W_Koenig_SF,W_Koenig_WF]

S_Koenig_WF=["  \+/  ","  [#]  ","  [#]  "," (###) "]
S_Koenig_SF=["..\+/..","..[#]..","..[#]..",".(###)."]
S_Koenig=[S_Koenig_SF,S_Koenig_WF]

Figuren={}
Figuren[0]=Feld
Figuren[1]=W_Bauer
Figuren[3]=W_Springer
Figuren[3.5]=W_Laeufer
Figuren[4.5]=W_Turm
Figuren[8]=W_Dame
Figuren[300]=W_Koenig

Figuren[-1]=S_Bauer
Figuren[-3]=S_Springer
Figuren[-3.5]=S_Laeufer
Figuren[-4.5]=S_Turm
Figuren[-8]=S_Dame
Figuren[-300]=S_Koenig

Begrenzung="+-------+-------+-------+-------+-------+-------+-------+-------+"

WinningPooh=[
"Play against Winning Pooh: ",
"                    .--,",
"     .-.    __,,,__/    |",
"    /   \-'`        `-./_",
"    |    |               `)",
"     \   `             `\ ;",
"    /       ,        ,    |",
"    |      /         : O /_",
"    |          O  .--;__   '.",
"    |                (  )`.  |",
"    \                 `-` /  |",
"     \          ,_  _.-./`  /",
"      \          \``-.(    /",
"      |           `---'   /--.",
"    ,--\___..__        _.'   /--.",
"jgs \          `-._  _`/    '    '.",
"    .' ` ' .       ``    '        ."]

def WinningPoohPrint():
	for string in WinningPooh:
		print string

#######################################################################################################
# Brett-Klasse ########################################################################################
#######################################################################################################
class Brett(list):
	"ebenholz und elfenbein und fein geschnitze Figuren"
	def __init__(self,Brettname=None):
		list(self)					# Oder list.__init__(self) ?
		for x in range(8):
			self.append([])
		for x in range(8):
			for y in range(8):			
				self[x].append(0)

	def Aufbauen(self):
		self[0][0]=4.5
		self[1][0]=3
		self[2][0]=3.5
		self[3][0]=8
		self[4][0]=300
		self[5][0]=3.5
		self[6][0]=3
		self[7][0]=4.5
		self[0][7]=-4.5
		self[1][7]=-3
		self[2][7]=-3.5
		self[3][7]=-8
		self[4][7]=-300
		self[5][7]=-3.5
		self[6][7]=-3
		self[7][7]=-4.5
		for x in range(8):
			self[x][1]=1
			self[x][6]=-1

	def Ausgabe(self):
		for y in range(8):
			for x in range(8):
				print Wert_Char[self[x][7-y]],
			print
		print

	def Zug(self,(x,y),(a,b)):	#Tupel für Koordinaten um die Umwandlung in Alg. Not. zu erleichtern.
		self[a][b]=self[x][y]
		self[x][y]=0

# Ende der Brett-Klasse
#######################################################################################################
# Stellungs-Klasse ########################################################################################
#######################################################################################################
class Stellung():
	def __init__(self):
		self.Brett=Brett()
		self.Analysebrett=Brett() 		# Für den imSchach-Zuggenerator
		self.W_Koenigsfeld=(4,0)
		self.S_Koenigsfeld=(4,7)
		self.W_am_Zug=True
		self.Schlagzug=False
		self.wKurzeRochade=True
		self.wLangeRochade=True
		self.sKurzeRochade=True
		self.sLangeRochade=True
		self.fifty_moves=0
		self.Over=False
		self.enpassant= -1
		# self.dreimalige={} Das kommt in die Partie-Klasse nicht hierhin.

	def Zug(self,zugtuple):			# Im Gegensatz zum Brettzug müssen hier auch noch die anderen Daten upgedatet werden.
		# Hier kann man sicher einiges optimieren, so dass z.b. erstmal geschaut wird, ob das Rochaderecht noch existiert etc...
		# Vielleicht wird später beim Algorithmus durch die Reihenfolge der Zugüberprüfung einiges optimiert - Wenn man erst beim
		# Koenig und den Türmen nachschaut, muss man später nicht immer Überprüfen ob das Rochaderecht negiert werden muss etc

		# a_feld=Alg_Koord[str1]			# Wird hier ersetzt und später vielleicht auch direkt bei den Parametern
		# z_feld=Alg_Koord[str2]			# Schließlich macht es keinen Sinn im Alg dann mit a1-e5 zu arbeiten
		a_feld=zugtuple[0]
		z_feld=zugtuple[1]

		zr=-1
		if(self.W_am_Zug):
			zr=1

		self.enpassant=-1 		# Der Default.

		if(self.Brett[z_feld[0]][z_feld[1]]!=0):
			self.fifty_moves=-1
			self.Schlagzug=True
			if(abs(self.Brett[z_feld[0]][z_feld[1]])==300):			# König schlagen beendet die Partie (vorerst)
				self.Over=True
		else:
			self.Schlagzug=False
		# Rochaden:
		if(abs(self.Brett[a_feld[0]][a_feld[1]])==300): 	# Wenn wir es überhaupt mit einem Königszug zu tun haben ...
			if(zr==1):
				self.W_Koenigsfeld=z_feld
			else:
				self.S_Koenigsfeld=z_feld
			#weiße Rochaden
			if(a_feld==(4,0) and z_feld==(6,0)):		#wKRochade durch Königszug.
				self.Brett.Zug((7,0),(5,0))				#Turmzug
				self.wKurzeRochade=False
				self.wLangeRochade=False

			elif(a_feld==(4,0) and z_feld==(2,0)):		#wLRochade durch Königszug.
				self.Brett.Zug((0,0),(3,0))				#Turmzug
				self.wKurzeRochade=False
				self.wLangeRochade=False
			#schwarze Rochaden
			elif(a_feld==(4,7) and z_feld==(6,7)):		#sKRochade durch Königszug.
				self.Brett.Zug((7,7),(5,7))				#Turmzug
				self.sKurzeRochade=False
				self.sLangeRochade=False

			elif(a_feld==(4,7) and z_feld==(2,7)):		#sLRochade durch Königszug.
				self.Brett.Zug((0,7),(3,7))				#Turmzug
				self.sKurzeRochade=False
				self.sLangeRochade=False

		# en passant
		if(self.Brett[a_feld[0]][a_feld[1]]==1 or self.Brett[a_feld[0]][a_feld[1]]==-1):	#wBauer oder sBauer
			self.fifty_moves=-1
			if(( (not (a_feld[0] - z_feld[0])==0)) and self.Brett[z_feld[0]][z_feld[1]]== 0):			#Linie gewechselt aber nichts geschlagen
				self.Brett[z_feld[0]][z_feld[1] - self.Brett[a_feld[0]][a_feld[1]] ]=0		#En Passant: clever S-W unterschieden: wB=1 sB=-1

		# doppelschritt als Linie wird unter self.enpassant gespeichert.
		
			elif(abs(z_feld[1]-a_feld[1])==2):	# Elif weil entweder Doppelschritt oder EnPassant schlagen.
				self.enpassant=z_feld[0] 		# Sonst gilt der Default s.o.
	

		# Umwandlung - und dann diese drei Bauernzüge zusammenfassen.


		# Turmzüge --> Rochadeverfall:
		if(a_feld==(0,0)):
			wLangeRochade=False
		elif(a_feld==(7,0)):
			wKurzeRochade=False
		elif(a_feld==(0,7)):
			sLangeRochade=False
		elif(a_feld==(7,7)):
			sKurzeRochade=False

		# Auch wenn das Brett erst später mit Königen gefüllt wird.
		# Wir müssen VOR dem Zug überprüfen ob wir einen König schlagen:
		Koenigschlaegerei=False
		if(abs(self.Brett[z_feld[0]][z_feld[1]])==300):
			Koenigschlaegerei=True
			gegkoenig=self.Brett[z_feld[0]][z_feld[1]]*-1

		self.Brett.Zug(a_feld,z_feld)
		self.fifty_moves=self.fifty_moves+1
		self.W_am_Zug = not self.W_am_Zug
		# Umwandlung (muss nach dem Zugausführen kommen):
		if(len(zugtuple)==3):
			self.Brett[z_feld[0]][z_feld[1]]=zugtuple[2]*zr

		# König geschlagen:
		# Dieser Abschnitt muss eventuell abgeändert werden, wenn das Programm vorschreitet.
		# Zurueck_Zug muss davon informiert werden.
		if(Koenigschlaegerei):
			for x in range(8):
				for y in range(8):
					self.Brett[x][y]=gegkoenig


	# Muss noch getestet werden:	
	def Umwandlung(self):
		#print "Umwandlungstalk:"
		reihe=7
		bauer=1
		if(self.W_am_Zug):	# Weiß am Zug heißt gerade konnte Schwarz einen Bauern auf die Grundreihe schieben.
			#print "Weiß ist am Zug, das heißt für Schwarz könnte was umgewandelt werden."
			reihe=0 		# Und zwar auf der weißen! Grundreihe
			bauer=-1
		#else:
			#print "Schwarz ist am Zug, das heißt für Weiß könnte was umgewandelt werden."

		for x in range(8):
			#print "Suche auf Brett {}{}".format(x,reihe)
			if(self.Brett[x][reihe]==bauer):
				#print "Bauer gefunden:Brett{}{}".format(x,reihe)
				z=""
				while(z==""):
					z = raw_input('Umwandlung in: ')

				if(z=='D' or z=='d' or z=='q' or z=='Q'):
					self.Brett[x][reihe]= 8*bauer
				elif(z=='T' or z=='t' or z=='r' or z=='R'):
					self.Brett[x][reihe]=4.5*bauer
				elif(z=='S' or z=='s' or z=='N' or z=='n'):
					self.Brett[x][reihe]=3*bauer
				elif(z=='L' or z=='l' or z=='B' or z=='b'):
					self.Brett[x][reihe]=3.5*bauer
				else:
					self.Umwandlung()



	# Ausgabe von Stellungsinformationen
	def Info(self):
		if(self.W_am_Zug):
			print "Weiß ist am Zug."
		else:
			print "Schwarz ist am Zug."

		if(self.Schlagzug):
			print "Der letzte Zug war ein Schlagzug."
		else:
			print "Der letzte Zug war kein Schlagzug."
		
		# Rochaderechte:
		if(self.wKurzeRochade):
			print "Weiß darf noch kurz rochieren."
		else:
			print "Weiß darf nicht mehr kurz rochieren."

		if(self.wLangeRochade):
			print "Weiß darf noch lang rochieren."
		else:
			print "Weiß darf nicht mehr lang rochieren."

		if(self.sKurzeRochade):
			print "Schwarz darf noch kurz rochieren."
		else:
			print "Schwarz darf nicht mehr kurz rochieren."

		if(self.sLangeRochade):
			print "Schwarz darf noch lang rochieren."
		else:
			print "Schwarz darf nicht mehr lang rochieren."

		print "Es wurden {} Züge seit dem letzten Bauern- oder Schlagzug gemacht.".format(self.fifty_moves)
		if(not self.Over):
			print "Die Partie läuft noch."
		else:
			print "Die Partie ist vorbei."

		if(self.enpassant!= -1):
			print "Auf der {}-Linie wurde gerade ein Doppelschritt durchgeführt.".format("abcdefgh"[self.enpassant])
		else:
			print "Kein Doppelschritt im letzten Zug."
		
		# self.dreimalige={}

	# Hier kommt die Edel_Ausgabe


	def Edel_Ausgabe(self):		# x y z.b. a3 oder d5, oder so. z ist die Zeile der Darstellung.
		Ausgabeliste=[]
		Ausgabeliste.append(Begrenzung)
		Ausgabeliste.append("\n")
		for y in range(8):				# Reihe 7-y 
			for z in range(4):			# Zeile z
				for x in range(8):		# Feld x
					Ausgabeliste.append("|")
					Ausgabeliste.append(Figuren[self.Brett[x][7-y]][(y+x+1)%2][z])
				Ausgabeliste.append("|\n")
			Ausgabeliste.append(Begrenzung)
			Ausgabeliste.append("\n")
		print "".join(Ausgabeliste)

	# HIER KOMMT EIN VERWANDTER DES ZUGGENERATORS: NOTWENDIG FÜR ROCHADE UND VIELLEICHT MATT/PATT/SCHACH
	def Feld_bedroht(self,x,y,durch_schwarz):
		f=1
		if(durch_schwarz):
			f=-1
		#Durch Bauern.
		if(self.Auf_Brett(x+1,y-f)):
			if(self.Brett[x+1][y-f]==f):
				return True
		if(self.Auf_Brett(x-1,y-f)):
			if(self.Brett[x-1][y-f]==f):
				return True
		#Durch Springer:
		if(self.Auf_Brett(x+2,y+1)):
			if(self.Brett[x+2][y+1]==f*3):	# 1.
				return True

		if(self.Auf_Brett(x+2,y-1)):
			if(self.Brett[x+2][y-1]==f*3):	# 2.
				return True

		if(self.Auf_Brett(x+1,y+2)):
			if(self.Brett[x+1][y+2]==f*3): # 3.
				return True

		if(self.Auf_Brett(x+1,y-2)):
			if(self.Brett[x+1][y-2]==f*3): # 4.
				return True

		if(self.Auf_Brett(x-2,y+1)):
			if(self.Brett[x-2][y+1]==f*3): #5.
				return True

		if(self.Auf_Brett(x-2,y-1)):
			if(self.Brett[x-2][y-1]==f*3): #6.
				return True

		if(self.Auf_Brett(x-1,y+2)):
			if(self.Brett[x-1][y+2]==f*3): # 7.
				return True

		if(self.Auf_Brett(x-1,y-2)):
			if(self.Brett[x-1][y-2]==f*3): # 8.
				return True	

		#Durch Diagonalzüge:
		for z in range(1,8):
			if(self.Auf_Brett(x+z,y+z)):
				if(self.Brett[x+z][y+z]==f*3.5 or self.Brett[x+z][y+z]==f*8):
					return True
				if(self.Brett[x+z][y+z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x-z,y+z)):
				if(self.Brett[x-z][y+z]==f*3.5 or self.Brett[x-z][y+z]==f*8):
					return True
				if(self.Brett[x-z][y+z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x+z,y-z)):
				if(self.Brett[x+z][y-z]==f*3.5 or self.Brett[x+z][y-z]==f*8):
					return True
				if(self.Brett[x+z][y-z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x-z,y-z)):
				if(self.Brett[x-z][y-z]==f*3.5 or self.Brett[x-z][y-z]==f*8):
					return True
				if(self.Brett[x-z][y-z]!=0):
					break			
		#Durch gerade Züge:
		for z in range(1,8):
			if(self.Auf_Brett(x,y+z)):
				if(self.Brett[x][y+z]==f*4.5 or self.Brett[x][y+z]==f*8):
					return True
				if(self.Brett[x][y+z]!=0):
					break		

		for z in range(1,8):
			if(self.Auf_Brett(x,y-z)):
				if(self.Brett[x][y-z]==f*4.5 or self.Brett[x][y-z]==f*8):
					return True
				if(self.Brett[x][y-z]!=0):
					break	

		for z in range(1,8):
			if(self.Auf_Brett(x+z,y)):
				if(self.Brett[x+z][y]==f*4.5 or self.Brett[x+z][y]==f*8):
					return True
				if(self.Brett[x+z][y]!=0):
					break	

		for z in range(1,8):
			if(self.Auf_Brett(x-1,y)):
				if(self.Brett[x-1][y]==f*4.5 or self.Brett[x-1][y]==f*8):
					return True
				if(self.Brett[x-1][y]!=0):
					break		
		#Durch den König:
		if(self.Auf_Brett(x-1,y)):
			if(self.Brett[x-1][y]==f*300):
				return True

		if(self.Auf_Brett(x-1,y+1)):
			if(self.Brett[x-1][y+1]==f*300):
				return True

		if(self.Auf_Brett(x-1,y-1)):
			if(self.Brett[x-1][y-1]==f*300):
				return True

		if(self.Auf_Brett(x,y+1)):
			if(self.Brett[x][y+1]==f*300):
				return True

		if(self.Auf_Brett(x,y-1)):
			if(self.Brett[x][y-1]==f*300):
				return True

		if(self.Auf_Brett(x+1,y)):
			if(self.Brett[x+1][y]==f*300):
				return True

		if(self.Auf_Brett(x+1,y+1)):
			if(self.Brett[x+1][y+1]==f*300):
				return True

		if(self.Auf_Brett(x+1,y-1)):
			if(self.Brett[x+1][y-1]==f*300):
				return True

		return False

	def Analyse_Feld_bedroht(self,x,y,durch_schwarz):
		f=1
		if(durch_schwarz):
			f=-1
		#Durch Bauern.
		if(self.Auf_Brett(x+1,y-f)):
			if(self.Analysebrett[x+1][y-f]==f):
				return True
		if(self.Auf_Brett(x-1,y-f)):
			if(self.Analysebrett[x-1][y-f]==f):
				return True
		#Durch Springer:
		if(self.Auf_Brett(x+2,y+1)):
			if(self.Analysebrett[x+2][y+1]==f*3):	# 1.
				return True

		if(self.Auf_Brett(x+2,y-1)):
			if(self.Analysebrett[x+2][y-1]==f*3):	# 2.
				return True

		if(self.Auf_Brett(x+1,y+2)):
			if(self.Analysebrett[x+1][y+2]==f*3): # 3.
				return True

		if(self.Auf_Brett(x+1,y-2)):
			if(self.Analysebrett[x+1][y-2]==f*3): # 4.
				return True

		if(self.Auf_Brett(x-2,y+1)):
			if(self.Analysebrett[x-2][y+1]==f*3): #5.
				return True

		if(self.Auf_Brett(x-2,y-1)):
			if(self.Analysebrett[x-2][y-1]==f*3): #6.
				return True

		if(self.Auf_Brett(x-1,y+2)):
			if(self.Analysebrett[x-1][y+2]==f*3): # 7.
				return True

		if(self.Auf_Brett(x-1,y-2)):
			if(self.Analysebrett[x-1][y-2]==f*3): # 8.
				return True	

		#Durch Diagonalzüge:
		for z in range(1,8):
			if(self.Auf_Brett(x+z,y+z)):
				if(self.Analysebrett[x+z][y+z]==f*3.5 or self.Analysebrett[x+z][y+z]==f*8):
					return True
				if(self.Analysebrett[x+z][y+z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x-z,y+z)):
				if(self.Analysebrett[x-z][y+z]==f*3.5 or self.Analysebrett[x-z][y+z]==f*8):
					return True
				if(self.Analysebrett[x-z][y+z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x+z,y-z)):
				if(self.Analysebrett[x+z][y-z]==f*3.5 or self.Analysebrett[x+z][y-z]==f*8):
					return True
				if(self.Analysebrett[x+z][y-z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x-z,y-z)):
				if(self.Analysebrett[x-z][y-z]==f*3.5 or self.Analysebrett[x-z][y-z]==f*8):
					return True
				if(self.Analysebrett[x-z][y-z]!=0):
					break			
		#Durch gerade Züge:
		for z in range(1,8):
			if(self.Auf_Brett(x,y+z)):
				if(self.Analysebrett[x][y+z]==f*4.5 or self.Analysebrett[x][y+z]==f*8):
					return True
				if(self.Analysebrett[x][y+z]!=0):
					break		

		for z in range(1,8):
			if(self.Auf_Brett(x,y-z)):
				if(self.Analysebrett[x][y-z]==f*4.5 or self.Analysebrett[x][y-z]==f*8):
					return True
				if(self.Analysebrett[x][y-z]!=0):
					break	

		for z in range(1,8):
			if(self.Auf_Brett(x+z,y)):
				if(self.Analysebrett[x+z][y]==f*4.5 or self.Analysebrett[x+z][y]==f*8):
					return True
				if(self.Analysebrett[x+z][y]!=0):
					break	

		for z in range(1,8):
			if(self.Auf_Brett(x-1,y)):
				if(self.Analysebrett[x-1][y]==f*4.5 or self.Analysebrett[x-1][y]==f*8):
					return True
				if(self.Analysebrett[x-1][y]!=0):
					break		
		#Durch den König:
		if(self.Auf_Brett(x-1,y)):
			if(self.Analysebrett[x-1][y]==f*300):
				return True

		if(self.Auf_Brett(x-1,y+1)):
			if(self.Analysebrett[x-1][y+1]==f*300):
				return True

		if(self.Auf_Brett(x-1,y-1)):
			if(self.Analysebrett[x-1][y-1]==f*300):
				return True

		if(self.Auf_Brett(x,y+1)):
			if(self.Analysebrett[x][y+1]==f*300):
				return True

		if(self.Auf_Brett(x,y-1)):
			if(self.Analysebrett[x][y-1]==f*300):
				return True

		if(self.Auf_Brett(x+1,y)):
			if(self.Analysebrett[x+1][y]==f*300):
				return True

		if(self.Auf_Brett(x+1,y+1)):
			if(self.Analysebrett[x+1][y+1]==f*300):
				return True

		if(self.Auf_Brett(x+1,y-1)):
			if(self.Analysebrett[x+1][y-1]==f*300):
				return True

		return False

	def Zug_Feld_bedroht(self,x,y,durch_schwarz):
		f=1
		if(durch_schwarz):
			f=-1
		#Durch Bauern.
		if(self.Auf_Brett(x+1,y-f)):
			if(self.Brett[x+1][y-f]==f):
				return ((x+1,y-f),(x,y))
		if(self.Auf_Brett(x-1,y-f)):
			if(self.Brett[x-1][y-f]==f):
				return ((x-1,y-f),(x,y))
		#Durch Springer:
		if(self.Auf_Brett(x+2,y+1)):
			if(self.Brett[x+2][y+1]==f*3):	# 1.
				return ((x+2,y+1),(x,y))

		if(self.Auf_Brett(x+2,y-1)):
			if(self.Brett[x+2][y-1]==f*3):	# 2.
				return ((x+2,y-1),(x,y))

		if(self.Auf_Brett(x+1,y+2)):
			if(self.Brett[x+1][y+2]==f*3): # 3.
				return ((x+1,y+2),(x,y))

		if(self.Auf_Brett(x+1,y-2)):
			if(self.Brett[x+1][y-2]==f*3): # 4.
				return ((x+1,y-2),(x,y))

		if(self.Auf_Brett(x-2,y+1)):
			if(self.Brett[x-2][y+1]==f*3): #5.
				return ((x-2,y+1),(x,y))

		if(self.Auf_Brett(x-2,y-1)):
			if(self.Brett[x-2][y-1]==f*3): #6.
				return ((x-2,y-1),(x,y))

		if(self.Auf_Brett(x-1,y+2)):
			if(self.Brett[x-1][y+2]==f*3): # 7.
				return ((x-1,y+2),(x,y))

		if(self.Auf_Brett(x-1,y-2)):
			if(self.Brett[x-1][y-2]==f*3): # 8.
				return ((x-1,y-2),(x,y))

		#Durch Diagonalzüge:
		for z in range(1,8):
			if(self.Auf_Brett(x+z,y+z)):
				if(self.Brett[x+z][y+z]==f*3.5 or self.Brett[x+z][y+z]==f*8):
					return ((x+z,y+z),(x,y))
				if(self.Brett[x+z][y+z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x-z,y+z)):
				if(self.Brett[x-z][y+z]==f*3.5 or self.Brett[x-z][y+z]==f*8):
					return ((x-z,y+z),(x,y))
				if(self.Brett[x-z][y+z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x+z,y-z)):
				if(self.Brett[x+z][y-z]==f*3.5 or self.Brett[x+z][y-z]==f*8):
					return ((x+z,y-z),(x,y))
				if(self.Brett[x+z][y-z]!=0):
					break

		for z in range(1,8):
			if(self.Auf_Brett(x-z,y-z)):
				if(self.Brett[x-z][y-z]==f*3.5 or self.Brett[x-z][y-z]==f*8):
					return ((x-z,y-z),(x,y))
				if(self.Brett[x-z][y-z]!=0):
					break			
		#Durch gerade Züge:
		for z in range(1,8):
			if(self.Auf_Brett(x,y+z)):
				if(self.Brett[x][y+z]==f*4.5 or self.Brett[x][y+z]==f*8):
					return ((x,y+z),(x,y))
				if(self.Brett[x][y+z]!=0):
					break		

		for z in range(1,8):
			if(self.Auf_Brett(x,y-z)):
				if(self.Brett[x][y-z]==f*4.5 or self.Brett[x][y-z]==f*8):
					return ((x,y-z),(x,y))
				if(self.Brett[x][y-z]!=0):
					break	

		for z in range(1,8):
			if(self.Auf_Brett(x+z,y)):
				if(self.Brett[x+z][y]==f*4.5 or self.Brett[x+z][y]==f*8):
					return ((x+z,y),(x,y))
				if(self.Brett[x+z][y]!=0):
					break	

		for z in range(1,8):
			if(self.Auf_Brett(x-1,y)):
				if(self.Brett[x-1][y]==f*4.5 or self.Brett[x-1][y]==f*8):
					return ((x-1,y),(x,y))
				if(self.Brett[x-1][y]!=0):
					break		
		#Durch den König:
		if(self.Auf_Brett(x-1,y)):
			if(self.Brett[x-1][y]==f*300):
				return ((x-1,y),(x,y))

		if(self.Auf_Brett(x-1,y+1)):
			if(self.Brett[x-1][y+1]==f*300):
				return ((x-1,y+1),(x,y))

		if(self.Auf_Brett(x-1,y-1)):
			if(self.Brett[x-1][y-1]==f*300):
				return ((x-1,y-1),(x,y))

		if(self.Auf_Brett(x,y+1)):
			if(self.Brett[x][y+1]==f*300):
				return ((x,y+1),(x,y))

		if(self.Auf_Brett(x,y-1)):
			if(self.Brett[x][y-1]==f*300):
				return ((x,y-1),(x,y))

		if(self.Auf_Brett(x+1,y)):
			if(self.Brett[x+1][y]==f*300):
				return ((x+1,y),(x,y))

		if(self.Auf_Brett(x+1,y+1)):
			if(self.Brett[x+1][y+1]==f*300):
				return ((x+1,y+1),(x,y))

		if(self.Auf_Brett(x+1,y-1)):
			if(self.Brett[x+1][y-1]==f*300):
				return ((x+1,y-1),(x,y))

		return -1
	
	##################################################################################################
		# Hier kommt der Zuggenerator:
	##################################################################################################

	def Auf_Brett(self,x,y):
		if(x in range(8) and y in range(8)):
			return True
		else:
			return False


	def Zuggenerator(self):

		# Das ist der Abschnitt, der dafür sorgen soll, dass es keine Gegenschachs mehr gibt.
		if(not self.W_am_Zug):
			zr=-1
			imSchach=self.Zug_Feld_bedroht(self.W_Koenigsfeld[0],self.W_Koenigsfeld[1],True)

		if(self.W_am_Zug):
			zr=1
			imSchach=self.Zug_Feld_bedroht(self.S_Koenigsfeld[0],self.S_Koenigsfeld[1],False)

		# if(imSchach!=-1):
		# 	#print imSchach
		# 	yield imSchach		


		if(False): # Das muss ich wieder entfernen, wenn ich das oben wieder entkommentiere.
			pass
		# Hier kommt der Rest.
		else:
			for x in range(8):

				for y in range(8):

					#####################################################################
					if(self.Brett[x][y]*zr<=0):	# Häufigster Fall --> Schnelles Continue
						continue
					#####################################################################
					elif(self.Brett[x][y]==zr):		# Zweithäufigster Fall: Bauern.

						if(self.Brett[x][y+zr]==0):
							if(not(y+zr)%7):					# Auf der Achten Reihe 0 oder 7
								yield ((x,y),(x,y+zr),8) 		# Umwandlung in die Dame etc
								yield ((x,y),(x,y+zr),4.5)
								yield ((x,y),(x,y+zr),3.5)
								yield ((x,y),(x,y+zr),3)
							else:
								yield ((x,y),(x,y+zr))

						if(x<7):
							if(self.Brett[x+1][y+zr]*zr*(-1)>0):
								if(not(y+zr)%7):					# Auf der Achten Reihe 0 oder 7
									yield ((x,y),(x+1,y+zr),8) 		# Umwandlung in die Dame etc
									yield ((x,y),(x+1,y+zr),4.5)
									yield ((x,y),(x+1,y+zr),3.5)
									yield ((x,y),(x+1,y+zr),3)
								else:
									yield ((x,y),(x+1,y+zr))
						
						if(x>0):
							if(self.Brett[x-1][y+zr]*zr*(-1)>0):
								if(not(y+zr)%7):
									yield ((x,y),(x-1,y+zr),8)
									yield ((x,y),(x-1,y+zr),4.5)
									yield ((x,y),(x-1,y+zr),3.5)
									yield ((x,y),(x-1,y+zr),3)
								else:
									yield ((x,y),(x-1,y+zr))
						# Doppelzuege:
						if(y==int(3.5-zr*2.5)):
							if(self.Brett[x][y+2*zr]==0 and self.Brett[x][y+zr]==0):
								yield ((x,y),(x,y+2*zr))
						# Hier muss ich noch EnPassant einbauen.
						if(y==int(3.5+zr*0.5) and self.enpassant==x+1 and x<7):
							yield ((x,y),(x+1,y+zr))

						if(y==int(3.5+zr*0.5) and self.enpassant==x-1 and x>0):
							yield ((x,y),(x-1,y+zr))

						continue
					#####################################################################
					elif(self.Brett[x][y]==3*zr):	# Springerzuege

						if(self.Auf_Brett(x+2,y+1)):
							if(self.Brett[x+2][y+1]*zr*(-1)>=0):	# 1.
								yield ((x,y),(x+2,y+1))

						if(self.Auf_Brett(x+2,y-1)):
							if(self.Brett[x+2][y-1]*zr*(-1)>=0):	# 2.
								yield ((x,y),(x+2,y-1))

						if(self.Auf_Brett(x+1,y+2)):
							if(self.Brett[x+1][y+2]*zr*(-1)>=0): # 3.
								yield ((x,y),(x+1,y+2))

						if(self.Auf_Brett(x+1,y-2)):
							if(self.Brett[x+1][y-2]*zr*(-1)>=0): # 4.
								yield ((x,y),(x+1,y-2))

						if(self.Auf_Brett(x-2,y+1)):
							if(self.Brett[x-2][y+1]*zr*(-1)>=0): #5.
								yield ((x,y),(x-2,y+1))

						if(self.Auf_Brett(x-2,y-1)):
							if(self.Brett[x-2][y-1]*zr*(-1)>=0): #6.
								yield ((x,y),(x-2,y-1))

						if(self.Auf_Brett(x-1,y+2)):
							if(self.Brett[x-1][y+2]*zr*(-1)>=0): # 7.
								yield ((x,y),(x-1,y+2))

						if(self.Auf_Brett(x-1,y-2)):
							if(self.Brett[x-1][y-2]*zr*(-1)>=0): # 8.
								yield ((x,y),(x-1,y-2))

						continue
					#####################################################################

					elif(self.Brett[x][y]==3.5*zr):	# Laeuferzuege
						for z in range(1,8):
							if(self.Auf_Brett(x+z,y+z)):
								if(self.Brett[x+z][y+z]*zr>0):
									break
								if(self.Brett[x+z][y+z]==0):
									yield ((x,y),(x+z,y+z))
								elif(self.Brett[x+z][y+z]*zr<0): # 8.
									yield ((x,y),(x+z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y-z)):
								if(self.Brett[x+z][y-z]*zr>0):
									break
								if(self.Brett[x+z][y-z]==0):
									yield ((x,y),(x+z,y-z))
								elif(self.Brett[x+z][y-z]*zr<0): # 8.
									yield ((x,y),(x+z,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y+z)):
								if(self.Brett[x-z][y+z]*zr>0):
									break
								if(self.Brett[x-z][y+z]==0):
									yield ((x,y),(x-z,y+z))
								elif(self.Brett[x-z][y+z]*zr<0): # 8.
									yield ((x,y),(x-z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y-z)):
								if(self.Brett[x-z][y-z]*zr>0):
									break
								if(self.Brett[x-z][y-z]==0):
									yield ((x,y),(x-z,y-z))
								elif(self.Brett[x-z][y-z]*zr<0): # 8.
									yield ((x,y),(x-z,y-z))
									break
							else:
								break
						continue
					#####################################################################

					elif(self.Brett[x][y]==4.5*zr):	# Turmzuege

						for z in range(1,8):
							if(self.Auf_Brett(x,y+z)):
								if(self.Brett[x][y+z]*zr>0):
									break
								if(self.Brett[x][y+z]==0):
									yield ((x,y),(x,y+z))
								elif(self.Brett[x][y+z]*zr<0): # 8.
									yield ((x,y),(x,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y)):
								if(self.Brett[x+z][y]*zr>0):
									break
								if(self.Brett[x+z][y]==0):
									yield ((x,y),(x+z,y))
								elif(self.Brett[x+z][y]*zr<0): # 8.
									yield ((x,y),(x+z,y))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x,y-z)):
								if(self.Brett[x][y-z]*zr>0):
									break
								if(self.Brett[x][y-z]==0):
									yield ((x,y),(x,y-z))
								elif(self.Brett[x][y-z]*zr<0): # 8.
									yield ((x,y),(x,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y)):
								if(self.Brett[x-z][y]*zr>0):
									break
								if(self.Brett[x-z][y]==0):
									yield ((x,y),(x-z,y))
								elif(self.Brett[x-z][y]*zr<0): # 8.
									yield ((x,y),(x-z,y))
									break
							else:
								break

						continue

					#####################################################################

					elif(self.Brett[x][y]==8*zr):	# Damenzuege
						# Die Turmzuege unter den Damenzuegen.
						for z in range(1,8):
							if(self.Auf_Brett(x,y+z)):
								if(self.Brett[x][y+z]*zr>0):
									break
								if(self.Brett[x][y+z]==0):
									yield ((x,y),(x,y+z))
								elif(self.Brett[x][y+z]*zr<0): # 8.
									yield ((x,y),(x,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y)):
								if(self.Brett[x+z][y]*zr>0):
									break
								if(self.Brett[x+z][y]==0):
									yield ((x,y),(x+z,y))
								elif(self.Brett[x+z][y]*zr<0): # 8.
									yield ((x,y),(x+z,y))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x,y-z)):
								if(self.Brett[x][y-z]*zr>0):
									break
								if(self.Brett[x][y-z]==0):
									yield ((x,y),(x,y-z))
								elif(self.Brett[x][y-z]*zr<0): # 8.
									yield ((x,y),(x,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y)):
								if(self.Brett[x-z][y]*zr>0):
									break
								if(self.Brett[x-z][y]==0):
									yield ((x,y),(x-z,y))
								elif(self.Brett[x-z][y]*zr<0): # 8.
									yield ((x,y),(x-z,y))
									break
							else:
								break
						#Die Laeuferzuege unter den Damenzuegen.

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y+z)):
								if(self.Brett[x+z][y+z]*zr>0):
									break
								if(self.Brett[x+z][y+z]==0):
									yield ((x,y),(x+z,y+z))
								elif(self.Brett[x+z][y+z]*zr<0): # 8.
									yield ((x,y),(x+z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y-z)):
								if(self.Brett[x+z][y-z]*zr>0):
									break
								if(self.Brett[x+z][y-z]==0):
									yield ((x,y),(x+z,y-z))
								elif(self.Brett[x+z][y-z]*zr<0): # 8.
									yield ((x,y),(x+z,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y+z)):
								if(self.Brett[x-z][y+z]*zr>0):
									break
								if(self.Brett[x-z][y+z]==0):
									yield ((x,y),(x-z,y+z))
								elif(self.Brett[x-z][y+z]*zr<0): # 8.
									yield ((x,y),(x-z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y-z)):
								if(self.Brett[x-z][y-z]*zr>0):
									break
								if(self.Brett[x-z][y-z]==0):
									yield ((x,y),(x-z,y-z))
								elif(self.Brett[x-z][y-z]*zr<0): # 8.
									yield ((x,y),(x-z,y-z))
									break
							else:
								break

						continue
					#####################################################################

					elif(self.Brett[x][y]==300*zr):	# Koenigszuege

					#Die Zuege nach Vorne
						if(x<7 and y<7):
							if(self.Brett[x+1][y+1]*zr<=0):
								yield ((x,y),(x+1,y+1))
						if(y<7):
							if(self.Brett[x][y+1]*zr<=0):
								yield ((x,y),(x,y+1))
						if(x>0 and y<7):
							if(self.Brett[x-1][y+1]*zr<=0):
								yield ((x,y),(x-1,y+1))	
					#Die Zuege zur Seite
						if(x<7):
							if(self.Brett[x+1][y]*zr<=0):
								yield ((x,y),(x+1,y))

						if(x>0):
							if(self.Brett[x-1][y]*zr<=0):
								yield ((x,y),(x-1,y))	
					#Die Zuege nach hinten	
						if(x<7 and y>0):
							if(self.Brett[x+1][y-1]*zr<=0):
								yield ((x,y),(x+1,y-1))
						if(y>0):
							if(self.Brett[x][y-1]*zr<=0):
								yield ((x,y),(x,y-1))
						if(x*y>0):
							if(self.Brett[x-1][y-1]*zr<=0):
								yield ((x,y),(x-1,y-1))	
					#Rochadezuege:
					#Problem: Rochieren über bedrohtes Feld --> Viele Abfragen.
					#Lösung: def Feld_bedroht(self,x,y):
						if(self.wKurzeRochade and self.W_am_Zug):
							if(self.Brett[5][0]==0 and self.Brett[6][0]==0):
								if(not self.Feld_bedroht(5,0,True)):
									if(not self.Feld_bedroht(4,0,True)):
										yield ((4,0),(6,0))	

						if(self.wLangeRochade and self.W_am_Zug):
							if(self.Brett[3][0]==0 and self.Brett[1][0]==0 and self.Brett[2][0]==0):
								if(not self.Feld_bedroht(3,0,True)):
									if(not self.Feld_bedroht(4,0,True)):
										yield ((4,0),(2,0))

						if(self.sKurzeRochade and not self.W_am_Zug):
							if(self.Brett[5][7]==0 and self.Brett[6][7]==0):
								if(not self.Feld_bedroht(5,7,False)):
									if(not self.Feld_bedroht(4,7,False)):
										yield ((4,7),(6,7))

						if(self.sLangeRochade and not self.W_am_Zug):
							if(self.Brett[3][7]==0 and self.Brett[2][7]==0 and self.Brett[1][7]==0):
								if(not self.Feld_bedroht(3,7,False)):
									if(not self.Feld_bedroht(4,7,False)):
										yield ((4,7),(2,7))

	##################################################################################################
	# Hier kommt der Schlag_Zuggenerator .... mit Umwandlung. Und Koenigszuegen.
	def Schlag_Zuggenerator(self):

		# Das ist der Abschnitt, der dafür sorgen soll, dass es keine Gegenschachs mehr gibt.
		if(not self.W_am_Zug):
			zr=-1
			imSchach=self.Zug_Feld_bedroht(self.W_Koenigsfeld[0],self.W_Koenigsfeld[1],True)

		if(self.W_am_Zug):
			zr=1
			imSchach=self.Zug_Feld_bedroht(self.S_Koenigsfeld[0],self.S_Koenigsfeld[1],False)

		# if(imSchach!=-1):    #Hmm, was war denn hier das Problem?
		# 	#print imSchach
		# 	yield imSchach		


		if(False): # Das muss ich wieder entfernen, wenn ich das oben wieder entkommentiere.
			pass
		# Hier kommt der Rest.
		else:
			for x in range(8):

				for y in range(8):

					#####################################################################
					if(self.Brett[x][y]*zr<=0):	# Häufigster Fall --> Schnelles Continue
						continue
					#####################################################################
					elif(self.Brett[x][y]==zr):		# Zweithäufigster Fall: Bauern.

						if(self.Brett[x][y+zr]==0):
							if(not(y+zr)%7):					# Auf der Achten Reihe 0 oder 7
								yield ((x,y),(x,y+zr),8) 		# Umwandlung in die Dame etc
								yield ((x,y),(x,y+zr),4.5)
								yield ((x,y),(x,y+zr),3.5)
								yield ((x,y),(x,y+zr),3)

						if(x<7):
							if(self.Brett[x+1][y+zr]*zr*(-1)>0):
								if(not(y+zr)%7):					# Auf der Achten Reihe 0 oder 7
									yield ((x,y),(x+1,y+zr),8) 		# Umwandlung in die Dame etc
									yield ((x,y),(x+1,y+zr),4.5)
									yield ((x,y),(x+1,y+zr),3.5)
									yield ((x,y),(x+1,y+zr),3)
								else:
									yield ((x,y),(x+1,y+zr))
						
						if(x>0):
							if(self.Brett[x-1][y+zr]*zr*(-1)>0):
								if(not(y+zr)%7):
									yield ((x,y),(x-1,y+zr),8)
									yield ((x,y),(x-1,y+zr),4.5)
									yield ((x,y),(x-1,y+zr),3.5)
									yield ((x,y),(x-1,y+zr),3)
								else:
									yield ((x,y),(x-1,y+zr))

						# Hier muss ich noch EnPassant einbauen.
						if(y==int(3.5+zr*0.5) and self.enpassant==x+1 and x<7):
							yield ((x,y),(x+1,y+zr))

						if(y==int(3.5+zr*0.5) and self.enpassant==x-1 and x>0):
							yield ((x,y),(x-1,y+zr))

						continue
					#####################################################################
					elif(self.Brett[x][y]==3*zr):	# Springerzuege

						if(self.Auf_Brett(x+2,y+1)):
							if(self.Brett[x+2][y+1]*zr*(-1)>0):	# 1.
								yield ((x,y),(x+2,y+1))

						if(self.Auf_Brett(x+2,y-1)):
							if(self.Brett[x+2][y-1]*zr*(-1)>0):	# 2.
								yield ((x,y),(x+2,y-1))

						if(self.Auf_Brett(x+1,y+2)):
							if(self.Brett[x+1][y+2]*zr*(-1)>0): # 3.
								yield ((x,y),(x+1,y+2))

						if(self.Auf_Brett(x+1,y-2)):
							if(self.Brett[x+1][y-2]*zr*(-1)>0): # 4.
								yield ((x,y),(x+1,y-2))

						if(self.Auf_Brett(x-2,y+1)):
							if(self.Brett[x-2][y+1]*zr*(-1)>0): #5.
								yield ((x,y),(x-2,y+1))

						if(self.Auf_Brett(x-2,y-1)):
							if(self.Brett[x-2][y-1]*zr*(-1)>0): #6.
								yield ((x,y),(x-2,y-1))

						if(self.Auf_Brett(x-1,y+2)):
							if(self.Brett[x-1][y+2]*zr*(-1)>0): # 7.
								yield ((x,y),(x-1,y+2))

						if(self.Auf_Brett(x-1,y-2)):
							if(self.Brett[x-1][y-2]*zr*(-1)>0): # 8.
								yield ((x,y),(x-1,y-2))

						continue
					#####################################################################

					elif(self.Brett[x][y]==3.5*zr):	# Laeuferzuege
						for z in range(1,8):
							if(self.Auf_Brett(x+z,y+z)):
								if(self.Brett[x+z][y+z]*zr>0):
									break
								elif(self.Brett[x+z][y+z]*zr<0): # 8.
									yield ((x,y),(x+z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y-z)):
								if(self.Brett[x+z][y-z]*zr>0):
									break
								elif(self.Brett[x+z][y-z]*zr<0): # 8.
									yield ((x,y),(x+z,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y+z)):
								if(self.Brett[x-z][y+z]*zr>0):
									break
								elif(self.Brett[x-z][y+z]*zr<0): # 8.
									yield ((x,y),(x-z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y-z)):
								if(self.Brett[x-z][y-z]*zr>0):
									break
								elif(self.Brett[x-z][y-z]*zr<0): # 8.
									yield ((x,y),(x-z,y-z))
									break
							else:
								break
						continue
					#####################################################################

					elif(self.Brett[x][y]==4.5*zr):	# Turmzuege

						for z in range(1,8):
							if(self.Auf_Brett(x,y+z)):
								if(self.Brett[x][y+z]*zr>0):
									break
								elif(self.Brett[x][y+z]*zr<0): # 8.
									yield ((x,y),(x,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y)):
								if(self.Brett[x+z][y]*zr>0):
									break
								elif(self.Brett[x+z][y]*zr<0): # 8.
									yield ((x,y),(x+z,y))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x,y-z)):
								if(self.Brett[x][y-z]*zr>0):
									break
								elif(self.Brett[x][y-z]*zr<0): # 8.
									yield ((x,y),(x,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y)):
								if(self.Brett[x-z][y]*zr>0):
									break
								elif(self.Brett[x-z][y]*zr<0): # 8.
									yield ((x,y),(x-z,y))
									break
							else:
								break

						continue

					#####################################################################

					elif(self.Brett[x][y]==8*zr):	# Damenzuege
						# Die Turmzuege unter den Damenzuegen.
						for z in range(1,8):
							if(self.Auf_Brett(x,y+z)):
								if(self.Brett[x][y+z]*zr>0):
									break
								elif(self.Brett[x][y+z]*zr<0): # 8.
									yield ((x,y),(x,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y)):
								if(self.Brett[x+z][y]*zr>0):
									break
								elif(self.Brett[x+z][y]*zr<0): # 8.
									yield ((x,y),(x+z,y))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x,y-z)):
								if(self.Brett[x][y-z]*zr>0):
									break
								elif(self.Brett[x][y-z]*zr<0): # 8.
									yield ((x,y),(x,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y)):
								if(self.Brett[x-z][y]*zr>0):
									break
								elif(self.Brett[x-z][y]*zr<0): # 8.
									yield ((x,y),(x-z,y))
									break
							else:
								break
						#Die Laeuferzuege unter den Damenzuegen.

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y+z)):
								if(self.Brett[x+z][y+z]*zr>0):
									break
								elif(self.Brett[x+z][y+z]*zr<0): # 8.
									yield ((x,y),(x+z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x+z,y-z)):
								if(self.Brett[x+z][y-z]*zr>0):
									break
								elif(self.Brett[x+z][y-z]*zr<0): # 8.
									yield ((x,y),(x+z,y-z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y+z)):
								if(self.Brett[x-z][y+z]*zr>0):
									break
								elif(self.Brett[x-z][y+z]*zr<0): # 8.
									yield ((x,y),(x-z,y+z))
									break
							else:
								break

						for z in range(1,8):
							if(self.Auf_Brett(x-z,y-z)):
								if(self.Brett[x-z][y-z]*zr>0):
									break
								elif(self.Brett[x-z][y-z]*zr<0): # 8.
									yield ((x,y),(x-z,y-z))
									break
							else:
								break

						continue
					#####################################################################

					elif(self.Brett[x][y]==300*zr):	# Koenigszuege

					#Die Zuege nach Vorne
						if(x<7 and y<7):
							if(self.Brett[x+1][y+1]*zr<=0):
								yield ((x,y),(x+1,y+1))
						if(y<7):
							if(self.Brett[x][y+1]*zr<=0):
								yield ((x,y),(x,y+1))
						if(x>0 and y<7):
							if(self.Brett[x-1][y+1]*zr<=0):
								yield ((x,y),(x-1,y+1))	
					#Die Zuege zur Seite
						if(x<7):
							if(self.Brett[x+1][y]*zr<=0):
								yield ((x,y),(x+1,y))

						if(x>0):
							if(self.Brett[x-1][y]*zr<=0):
								yield ((x,y),(x-1,y))	
					#Die Zuege nach hinten	
						if(x<7 and y>0):
							if(self.Brett[x+1][y-1]*zr<=0):
								yield ((x,y),(x+1,y-1))
						if(y>0):
							if(self.Brett[x][y-1]*zr<=0):
								yield ((x,y),(x,y-1))
						if(x*y>0):
							if(self.Brett[x-1][y-1]*zr<=0):
								yield ((x,y),(x-1,y-1))	
					#Rochadezuege:
					#Problem: Rochieren über bedrohtes Feld --> Viele Abfragen.
					#Lösung: def Feld_bedroht(self,x,y):
						if(self.wKurzeRochade and self.W_am_Zug):
							if(self.Brett[5][0]==0 and self.Brett[6][0]==0):
								if(not self.Feld_bedroht(5,0,True)):
									if(not self.Feld_bedroht(4,0,True)):
										yield ((4,0),(6,0))	

						if(self.wLangeRochade and self.W_am_Zug):
							if(self.Brett[3][0]==0 and self.Brett[2][0]==0):
								if(not self.Feld_bedroht(3,0,True)):
									if(not self.Feld_bedroht(4,0,True)):
										yield ((4,0),(2,0))

						if(self.sKurzeRochade and not self.W_am_Zug):
							if(self.Brett[5][7]==0 and self.Brett[6][7]==0):
								if(not self.Feld_bedroht(5,7,False)):
									if(not self.Feld_bedroht(4,7,False)):
										yield ((4,7),(6,7))

						if(self.sLangeRochade and not self.W_am_Zug):
							if(self.Brett[3][7]==0 and self.Brett[2][7]==0):
								if(not self.Feld_bedroht(3,7,False)):
									if(not self.Feld_bedroht(4,7,False)):
										yield ((4,7),(2,7))






	# Ist noch total verbuggt:
	def Legal_Generator(self):
		# Was hier noch hinkommt: Der Fall, dass der Koenig im Schach ist.
		# Vielleicht Koenigsfeld merken ? Jetzt steht das bei self.W_Koenigsfeld

		# Alternative Idee: ImSchach andersrum überprüfen und wenn der Gegner im Schach steht nur den Schlagzug ausführen.
		# Dazu: Wenn der König geschlagen wird, dann wird das Brett mit den anderen Königen gefüllt.
		# Das ist eine einfache Lösung, die auch nicht zu teuer ist. Allerdings löst sie das Problem mit Matt erkennen nicht,
		# sondern macht das Programm nur etwas spielfähiger.
		# Eigener König im Schach muss vielleicht separat im Such_Alg gelöst werden.

		if(not self.W_am_Zug):
			imSchach=self.Feld_bedroht(self.S_Koenigsfeld[0],self.S_Koenigsfeld[1],False)
		else:
			imSchach=self.Feld_bedroht(self.W_Koenigsfeld[0],self.W_Koenigsfeld[1],True)
			
		if(imSchach):			
			for x in self.Zuggenerator():
				self.Analysebrett=copy.deepcopy(self.Brett)
				self.Analysebrett.Zug((x[0][0],x[0][1]),(x[1][0],x[1][1]))	# Das hier kann keine Rochade und kein EnPassant.	

				if(not self.W_am_Zug):
					NochimSchach=self.Analyse_Feld_bedroht(self.S_Koenigsfeld[0],self.S_Koenigsfeld[1],False)
				else:
					NochimSchach=self.Analyse_Feld_bedroht(self.W_Koenigsfeld[0],self.W_Koenigsfeld[1],True)

				if(not NochimSchach):	# Nur Zuege die das Schach abwehren.
					yield x



		# Ansonsten kommt einfach der normale Zuggenerator:	
		else:
			for x in self.Zuggenerator():
				yield x


	def Matt(self):
		if(not self.W_am_Zug):
			imSchach=self.Feld_bedroht(self.S_Koenigsfeld[0],self.S_Koenigsfeld[1],False)
		else:
			imSchach=self.Feld_bedroht(self.W_Koenigsfeld[0],self.W_Koenigsfeld[1],True)

		if imSchach:
			Zuege=[zug for zug in self.Zuggenerator()]
			if Zuege==[]:
				if self.W_am_Zug:
					print "White is checkmate!"
					sys.exit()
				else:
					print "Black is checkmate!"
					sys.exit()

	# Hier kommt die Überprüfung hin, ob ein Zug legal ist:
	def Zug_legal(self, zugtuple):
		# Wo ist der König. Steht er nach dem Zug im Schach?
		# for x in range(8):
		# 	for y in range(8):

		# Hier steckt ein Bug, der sagt, dass Umwandlungzuege illegal sind: Wegen des Triples statt 2-Tuples vermutlich.
		for zug in self.Zuggenerator():							# Eines Tages Legal_Generator
			if((zugtuple[0],zugtuple[1])==(zug[0],zug[1])):
				return True
		return False

	def Zug_Einlesen(self): 						
		z=""
		while(z==""):
			z = raw_input('Your move: ')				# Hier kommt Einlesen vom Terminal und verwandeln von "  a1 -d5" --> 'a1' 'd5' bzw "O- o-0 " --> 'e1' 'c1'
		z1=""
		z2=""
		print "You inputted {} ...".format(z)
		zeichen=1
		liste=['a','b','c','d','e','f','g','h']		#,'A','B','C','D','E','F','G','H' vielleicht später noch?
		for x in range(len(z)):
			if(zeichen==1 and z[x] in liste):
				z1+=z[x]
				zeichen=2
			if(zeichen==2 and z[x] in [str(i) for i in range(1,9)]):
				z1+=z[x]
				zeichen=3
			if(zeichen==3 and z[x] in liste):
				z2+=z[x]
				zeichen=4
			if(zeichen==4 and z[x] in [str(i) for i in range(1,9)]):
				z2+=z[x]
				zeichen=5
		# Rochade-Erkenner:
		r=0
		for x in range(len(z)):
			if(z[x]=='0' or z[x]=='o' or z[x]=='O'):
				r+=1
		if(self.W_am_Zug):
			if(r==2):
				z1="e1"
				z2="g1"
			if(r==3):
				z1="e1"
				z2="c1"
		elif(not self.W_am_Zug):
			if(r==2):
				z1="e8"
				z2="g8"
			if(r==3):
				z1="e8"
				z2="c8"
		
		# Jetzt wird der Zug noch ausgeführt
		if(z1 in Alg_Koord.keys() and z2 in Alg_Koord.keys()):
			print "I decided that you mean the move {}-{}.".format(z1,z2)
			# Überprüfung ob die richtige Farbe zieht.
			if((self.W_am_Zug and self.Brett[Alg_Koord[z1][0]][Alg_Koord[z1][1]]>0) or (not self.W_am_Zug and self.Brett[Alg_Koord[z1][0]][Alg_Koord[z1][1]]<0)):
				# Hier gehört noch die Bauernumwandlung hin. Und auch in self.Zug(). Oder zusätzliches self.Umwandlung() Jepp, das klingt gut.
				zugtuple=((Alg_Koord[z1][0],Alg_Koord[z1][1]),(Alg_Koord[z2][0],Alg_Koord[z2][1]))
				if(self.Zug_legal(zugtuple)):
					#self.Zug(z1,z2)
					#self.Umwandlung()
					return zugtuple
				else:
					print "Illegal move!"
					return self.Zug_Einlesen()
			else:
				if(self.W_am_Zug):
					print "White to move!"
				else:
					print "Black to move!"
				return self.Zug_Einlesen()
		else: 
			print "{}-{} ist kein Zug!".format(z1,z2)
# Ende der Stellungsklasse.

#######################################################################################################
# Partie-Klasse ########################################################################################
#######################################################################################################
# Partie-Klasse - Stellungszeug ausgelagert. Alles wieder schön übersichtlich.
# Hier kommen Aktionen zwischen verschiedenen Brettern hin und der Such_Alg, der sie benutzt.
class Partie():
	def __init__(self):
		self.Stellung=[Stellung()]		# Eine Liste von Stellungen. Stellung[0] ist dabei die Partiestellung.
		self.Anfangsstellung=Stellung() # Mit Partieverlauf -> Zugrücknahme möglich ohne rückwärts ziehen
		self.Partieverlauf=[] 	# Das Partieformular
		self.dreimalige={}

		self.Bew_Histo=[0.0]			# Darin werden die Bewertungen gespeichert um bei größerer Abweichung abzubrechen
		# Toleranz=3 				# Das ist die Größe der Abweichung
		self.Bew_Dict={}			# Hier werden die Bewertungen für Alpha-Beta gespeichert
		self.Variante=[]			# Da wird die Variante beim Vorausberechnen reingeschrieben.
		self.alpha_beta=[]
		
		for x in range(20):
			self.Variante.append( ((0,0),(0,0)) )
			self.alpha_beta.append(0)


	def Spieler_Zug(self):
		zugtuple=self.Stellung[0].Zug_Einlesen()
		self.Stellung[0].Zug(zugtuple)
		self.Stellung[0].Umwandlung()

	# Einer der springenden Punkte bei der Stellungsbewertung ist das weiterrechnen.
	# Brute Force Weiterrechnen bei Schlagzügen ist schnell zu teuer.
	# Schlagzug-Brute Force ist aber so gut, dass es Sinn macht, auch bei Nicht-Schlagzügen
	# so weiter zu rechnen. Das Problem ist, dass man dabei auf eine Stellung noch eine Reihe
	# von Räuberschachzügen draufsetzt und so nicht zu der "BeideSeitenoptimalgespielt"-Stellung kommt.
	# Eine Lösung könnte sein, dass man nach jedem Zug die Stellung bewertet und das Räuberschachzeug nur 
	# ein "Verbessern" versucht. Das taugt aber offensichtlich auch nichts, weil das "Verbessern" eben auch
	# durch eine kleine Auswahl der legalen Zuege zustande kommt.

	# Was eigentlich passieren muss, ist ein BruteForce-Weiterrechnen bei Schlagzügen mit A_B_Pruning.
	# Wenn man dabei noch die Schlagzuege vorsortiert, hat man eine Chance Schlagabtaeusche bis zum Ende zu rechnen
	def Stellungsbewertung(self,rek_ebene):
			# Material + Zentrumsbias:
			if(not self.Stellung[rek_ebene].Schlagzug or rek_ebene==6): 
				wert=0.0
				for x in range(8):
					for y in range(8):
						if(abs(self.Stellung[rek_ebene].Brett[x][y])!=300 and abs(self.Stellung[rek_ebene].Brett[x][y])!=4.5):
							wert+=self.Stellung[rek_ebene].Brett[x][y]*(1 - max(abs(x-3.5),abs(y-3.5))/100)
						else:
							wert+=self.Stellung[rek_ebene].Brett[x][y]

				# Königssicherheit:
				if(self.Stellung[rek_ebene].Brett[1][7]==-300 or self.Stellung[rek_ebene].Brett[2][7]==-300 or self.Stellung[rek_ebene].Brett[6][7]==-300):
					wert-=0.5
				if(self.Stellung[rek_ebene].Brett[1][0]==300 or self.Stellung[rek_ebene].Brett[2][0]==300 or self.Stellung[rek_ebene].Brett[6][0]==300):
					wert+=0.5
				# Entwicklung = leere Grundreihe:
				for x in range(8):
					if(self.Stellung[rek_ebene].Brett[x][7]==0 or self.Stellung[rek_ebene].Brett[x][7]==-300 or self.Stellung[rek_ebene].Brett[x][7]==-4.5):
						wert-=0.4
					if(self.Stellung[rek_ebene].Brett[x][0]==0 or self.Stellung[rek_ebene].Brett[x][7]==300 or self.Stellung[rek_ebene].Brett[x][7]==4.5):
						wert+=0.4
				# Zentrumsbauern:
				zentrumsbonus=0.0
				if(abs(self.Stellung[rek_ebene].Brett[3][3])==1):
					zentrumsbonus+=self.Stellung[rek_ebene].Brett[3][3]*0.2
				if(abs(self.Stellung[rek_ebene].Brett[4][4])==1):
					zentrumsbonus+=self.Stellung[rek_ebene].Brett[4][4]*0.2
				if(abs(self.Stellung[rek_ebene].Brett[4][3])==1):
					zentrumsbonus+=self.Stellung[rek_ebene].Brett[4][3]*0.2
				if(abs(self.Stellung[rek_ebene].Brett[3][4])==1):
					zentrumsbonus+=self.Stellung[rek_ebene].Brett[3][4]*0.2
				wert+=zentrumsbonus
				return wert

			# Bei Schlagzug muss noch weiter gerechnet werden:

			else:	# Hier für A_B_SuchAlg runter auf 4 gesetzt.
				if(len(self.Stellung) < rek_ebene+2):
					self.Stellung.append(Stellung())

				minmax=50000			#d.h. es werden schwarze Züge gemacht und die minimale Bewertung gesucht
				MM=-1
				if(self.Stellung[rek_ebene].W_am_Zug):		#d.h. es werden weiße Züge gemacht und die maximale Bewertung gesucht.
					minmax =-50000
					MM=1

				self.Stellung[rek_ebene+1]=copy.deepcopy(self.Stellung[rek_ebene]) 
				for zugtuple in self.Stellung[rek_ebene].Zuggenerator(): 		
					# self.Stellung[rek_ebene+1]=copy.deepcopy(self.Stellung[rek_ebene]) 
					self.Stellung[rek_ebene+1].Zug(zugtuple)
					wert=self.Stellungsbewertung(rek_ebene+1)

					self.Zurueck_Zug(rek_ebene,zugtuple) # Vielleicht schneller

					if(wert*MM > minmax*MM):
						minmax=wert

				return minmax
	
	def Zugprint(self,zugtuple):
		print "{}{}-{}{}".format(Koord_Alg[0][zugtuple[0][0]],Koord_Alg[1][zugtuple[0][1]],Koord_Alg[0][zugtuple[1][0]],Koord_Alg[1][zugtuple[1][1]])
	def Variantenprint(self,depth):
		for x in range(depth):
			print x+1,
			print ".",
			self.Zugprint(self.Variante[x]),
		print
	# Diese Funktion macht sparsam den Zug zugtuple auf Stellung[rek_ebene+1] rückgängig.
	def Zurueck_Zug(self,rek_ebene,zugtuple):
		# Debugging: Wow, mit der Einstellung kommt es zu totalem Crap: Und es ist schneller!
		# Der Crap kommt daher, dass ich nur das Brett kopiert habe und nicht das Zugrecht ...!!!
		# self.Stellung[rek_ebene+1].Brett=copy.deepcopy(self.Stellung[rek_ebene].Brett)
		# self.Stellung[rek_ebene+1].W_am_Zug=copy.deepcopy(self.Stellung[rek_ebene].W_am_Zug)
		# self.Stellung[rek_ebene+1].Schlagzug=copy.deepcopy(self.Stellung[rek_ebene].Schlagzug)
		# self.Stellung[rek_ebene+1].wKurzeRochade=copy.deepcopy(self.Stellung[rek_ebene].wKurzeRochade)
		# self.Stellung[rek_ebene+1].wLangeRochade=copy.deepcopy(self.Stellung[rek_ebene].wLangeRochade)
		# self.Stellung[rek_ebene+1].sKurzeRochade=copy.deepcopy(self.Stellung[rek_ebene].sKurzeRochade)
		# self.Stellung[rek_ebene+1].sLangeRochade=copy.deepcopy(self.Stellung[rek_ebene].sLangeRochade)
		# self.Stellung[rek_ebene+1].fifty_moves=copy.deepcopy(self.Stellung[rek_ebene].fifty_moves)
		# self.Stellung[rek_ebene+1].Over=copy.deepcopy(self.Stellung[rek_ebene].Over)
		# self.Stellung[rek_ebene+1].enpassant= copy.deepcopy(self.Stellung[rek_ebene].enpassant)
		# self.Stellung[rek_ebene+1].dreimalige=copy.deepcopy(self.Stellung[rek_ebene].dreimalige)
		self.Stellung[rek_ebene+1].W_am_Zug=copy.copy(self.Stellung[rek_ebene].W_am_Zug)
		self.Stellung[rek_ebene+1].Schlagzug=copy.copy(self.Stellung[rek_ebene].Schlagzug)
		self.Stellung[rek_ebene+1].wKurzeRochade=copy.copy(self.Stellung[rek_ebene].wKurzeRochade)
		self.Stellung[rek_ebene+1].wLangeRochade=copy.copy(self.Stellung[rek_ebene].wLangeRochade)
		self.Stellung[rek_ebene+1].sKurzeRochade=copy.copy(self.Stellung[rek_ebene].sKurzeRochade)
		self.Stellung[rek_ebene+1].sLangeRochade=copy.copy(self.Stellung[rek_ebene].sLangeRochade)
		self.Stellung[rek_ebene+1].fifty_moves=copy.copy(self.Stellung[rek_ebene].fifty_moves)
		self.Stellung[rek_ebene+1].Over=copy.copy(self.Stellung[rek_ebene].Over)
		self.Stellung[rek_ebene+1].enpassant= copy.copy(self.Stellung[rek_ebene].enpassant)
		#self.Stellung[rek_ebene+1].dreimalige=copy.copy(self.Stellung[rek_ebene].dreimalige)
		# Wurde das Brett mit Koenigen gefüllt, muss alles zurückgesetzt werden:
		if(self.Stellung[rek_ebene+1].Brett[0][0]+self.Stellung[rek_ebene+1].Brett[7][7] > 30000):
			self.Stellung[rek_ebene+1].Brett=copy.deepcopy(self.Stellung[rek_ebene].Brett)
		# Sonst reicht gezieltes Rückgängigmachen:
		else:
			self.Stellung[rek_ebene+1].Brett[zugtuple[0][0]][zugtuple[0][1]]=copy.deepcopy(self.Stellung[rek_ebene].Brett[zugtuple[0][0]][zugtuple[0][1]])
			self.Stellung[rek_ebene+1].Brett[zugtuple[1][0]][zugtuple[1][1]]=copy.deepcopy(self.Stellung[rek_ebene].Brett[zugtuple[1][0]][zugtuple[1][1]])
			# Wenn in der vorherigen Stellung ein Doppelzug kam, müssen wir mit einem EnPassantSchlagen rechnen:
			if(self.Stellung[rek_ebene].enpassant!=-1 and zugtuple[1][1]%7 != 0):
				self.Stellung[rek_ebene+1].Brett[zugtuple[1][0]][zugtuple[1][1]+1]=copy.deepcopy(self.Stellung[rek_ebene].Brett[zugtuple[1][0]][zugtuple[1][1]+1])
				self.Stellung[rek_ebene+1].Brett[zugtuple[1][0]][zugtuple[1][1]-1]=copy.deepcopy(self.Stellung[rek_ebene].Brett[zugtuple[1][0]][zugtuple[1][1]-1])
			# Wenn der Koenig geschlagen wurde muss das ganze Brett reset werden.
			if(abs(self.Stellung[rek_ebene].Brett[zugtuple[1][0]][zugtuple[1][1]])==300):
				self.Stellung[rek_ebene+1].Brett=copy.deepcopy(self.Stellung[rek_ebene].Brett)
			# Rochade muss auch sensibler rückgängig gemacht werden. Erstmal deepcopy bei Koenigszug.
			if(abs(self.Stellung[rek_ebene].Brett[zugtuple[0][0]][zugtuple[0][1]])==300):
				self.Stellung[rek_ebene+1].Brett=copy.deepcopy(self.Stellung[rek_ebene].Brett)
	# Zur Speicherung der Partiestellung und der Überprüfung dreimaliger Stellungswiederholung
	# Sollte irgendwann durch Stellung_zu_FEN ersetzt werden ...
	def Stellung_zu_String(self,rek_ebene):
		string=""
		for x in range(8):
			for y in range(8):
				string+=str(self.Stellung[rek_ebene].Brett[x][y])
		string+=str(self.Stellung[rek_ebene].W_am_Zug)
		string+=str(self.Stellung[rek_ebene].wKurzeRochade)
		string+=str(self.Stellung[rek_ebene].wLangeRochade)
		string+=str(self.Stellung[rek_ebene].sKurzeRochade)
		string+=str(self.Stellung[rek_ebene].sLangeRochade)
		string+=str(self.Stellung[rek_ebene].enpassant)
		return string
	# Es stellt sich heraus, dass Alpha-Beta-Pruning gar nicht das ist was ich dachte. Sondern das was ich schon
	# mehr oder weniger mache. Nämlich das Abbrechen von schlechten Suchbäumen. Nur kann man das wesentlich
	# besser machen, wenn man sich die bisher beste und die bisher schlechteste Bewertung merkt und dementsprechende
	# beim Maximieren und Minimieren abbricht.
	# Und indem man vorsortiert. Z.b. durch eine erst geringere Suchtiefe.
	# In Pseudo-Code der Such-Alg(naja, nicht so pseudo):

	def Such_Alg(self,depth1,rek_ebene, Toleranz):
		depth=depth1 			# Das ist wohl notwendig, damit nicht das globale depth immer größer wird
		while(len(self.Stellung) < depth+3):
			self.Stellung.append(Stellung())

		# Neuer Abschnitt der dynamischen Depth-Veränderung:
		if (rek_ebene==0):
			wmoeglich=0
			for zugtuple in self.Stellung[rek_ebene].Zuggenerator(): # Zugzahl für z.b. Weiß mit Zuggenerator weil Schach nicht wichtig.
				wmoeglich+=1
			self.Stellung[rek_ebene+1]=copy.deepcopy(self.Stellung[rek_ebene]) 
			self.Stellung[rek_ebene+1].W_am_Zug=not self.Stellung[rek_ebene+1].W_am_Zug

			smoeglich=0
			for zugtuple in self.Stellung[rek_ebene+1].Zuggenerator(): #Zugzahl für z.b. Schwarz
				smoeglich+=1

			moeglich=wmoeglich*smoeglich*Toleranz # vll log(Toleranz+1) oder so ?
			print "moeglich=w{}xs{}={}".format(wmoeglich,smoeglich,wmoeglich*smoeglich)
			# Was hier möglich ist, hängt stark von der Toleranz ab:
			# Aber wie stark? Und Toleranz wirkt sich fast nur bei dem besser stehenden aus, oder?
			# Das sollte man vielleicht einbeziehen ...
			# Oder mal die Anzahl tatsächlich bewerteter Stellungen ausgeben ...
			if(moeglich<400):
				depth+=2
			if(moeglich<100):
				depth+=2
			if(moeglich<50):
				depth+=2

		

		self.Stellung[rek_ebene+1]=copy.deepcopy(self.Stellung[rek_ebene]) 	# copy.deepcopy(x)

		# In diesem Abschnitt wird Stellungsbewertung aufgerufen und Bew_Dict benutzt und gefüllt:
		if(depth==0):
			# Dieser Alpha-Beta-Kram macht es leider noch langsamer - vll wenn die BewFunk langsamer ist.
			# key=tuple(sorted(self.Variante[:rek_ebene])) #Alpha Beta 
			# if(key in self.Bew_Dict.keys()):				#Alpha Beta
			# 	return self.Bew_Dict[key]					#Alpha Beta
			# else:
			# 	wert=self.Stellungsbewertung(rek_ebene+1)
			# 	if(self.Variante[0]!=-1):
			# 		self.Bew_Dict[key]=wert # Alpha Beta
			# 	return wert
			return self.Stellungsbewertung(rek_ebene+1)
		#Hier kommt die Unterscheidung zwischen Weiß und Schwarz
		minmax=500									#d.h. es werden schwarze Züge gemacht und die minimale Bewertung gesucht
		MM=-1
		if(self.Stellung[rek_ebene].W_am_Zug):		#d.h. es werden weiße Züge gemacht und die maximale Bewertung gesucht.
			minmax = -500
			MM=1

		# Hier kommt der rekursive Teil und damit das Variantenberechnen:
		kandidatenzug=((0,0),(0,0))
		for zugtuple in self.Stellung[rek_ebene].Zuggenerator():			# Eines Tages Legal_Generator

			self.Stellung[rek_ebene+1].Zug(zugtuple)	

			# if(not self.Stellung[rek_ebene+1].Schlagzug):		#Alpha-Beta
			# 	self.Variante[rek_ebene]=zugtuple 				#Alpha-Beta
			# else: 											#Alpha-Beta
			# 	self.Variante[0]=-1  							#Alpha-Beta

			# Was hier noch reinkommt:
			# Eine Überprüfung dreimaliger Stellungswiederholung und evtl Patt/Matt!
			string=self.Stellung_zu_String(1)
			if(string in self.dreimalige.keys() and self.dreimalige[string]==2):
				wert=0.0
			# Pattüberprüfung: Geht erst, wenn nur legale Züge ausgespuckt werden.

			else:
				wert=self.Such_Alg(depth-1,rek_ebene+1,Toleranz)

			if(wert*MM > minmax*MM):
				if(rek_ebene==0):
					kandidatenzug=zugtuple
					print "depth={}".format(depth),
					print "Wert: ",
					print wert,
					print "Zug: ",
					self.Zugprint(zugtuple)
					
				minmax=wert

				if(rek_ebene>0 and minmax*MM > (self.Bew_Histo[len(self.Bew_Histo)-1]+Toleranz*MM)*MM): 	# Falls die Bewertung schon sehr gut ist:
					break														# Raus aus der Zuggenerator-Schleife.

	
			#self.Stellung[rek_ebene+1]=copy.deepcopy(self.Stellung[rek_ebene]) 			# Das muss noch ersetzt werden
			self.Zurueck_Zug(rek_ebene,zugtuple) # Zurueck_Zug ist eine sparsame Version von self.Stellung[rek_ebene+1]=self.Stellung[rek_ebene]

		if(rek_ebene==0):
			self.Bew_Histo.append(minmax)
			return (kandidatenzug,minmax)
		else:
			return minmax

	# Hier kommt der Versuch hin, Alpha-Beta-Pruning richtig zu implementieren.
	# Damit steht und fällt im Grunde dieses Schachprogramm, weil es sonst einfach zu langsam ist.
	# Wie funktioniert das? alpha_beta[rek_ebene] ist der bisher optimale Zug auf dieser Ebene:
	# Eine Ebene drüber wird beim unterbieten von alpha_beta abgebrochen, weil damit dieser Zweig widerlegt ist
	# Initialisiert wird also für WeißamZug mit -500 für Schwarz mit 500

	def A_B_Such_Alg(self,depth1,rek_ebene):

		depth=depth1 			# Das ist wohl notwendig, damit nicht das globale depth immer größer wird
		# Hier werden mehr Bretter zur Verfügung gestellt:
		while(len(self.Stellung) < depth+3):
			self.Stellung.append(Stellung())

		# Hier wird das nächste Brett vorbereitet.
		self.Stellung[rek_ebene+1]=copy.deepcopy(self.Stellung[rek_ebene]) 	# copy.deepcopy(x)

		# In diesem Abschnitt wird Stellungsbewertung aufgerufen :
		if(depth==0):
			return self.Stellungsbewertung(rek_ebene+1)

		#Hier kommt die Unterscheidung zwischen Weiß und Schwarz
		minmax=50000									#d.h. es werden schwarze Züge gemacht und die minimale Bewertung gesucht
		self.alpha_beta[rek_ebene]=50000
		MM=-1
		if(self.Stellung[rek_ebene].W_am_Zug):		#d.h. es werden weiße Züge gemacht und die maximale Bewertung gesucht.
			minmax = -50000
			self.alpha_beta[rek_ebene]=-50000
			MM=1

		# Hier kommt der rekursive Teil und damit das Variantenberechnen:
		kandidatenzug=((0,0),(0,0))
		# Hier kommt das Vorsortieren - erstmal nur Tiefe 1.
		Zugsortiert=[]

		if rek_ebene<4: # Auf der letzten Ebene wird so oder so jeder Zug angeschaut, oder?
			for zugtuple in self.Stellung[rek_ebene].Zuggenerator():			# Eines Tages Legal_Generator		
				self.Stellung[rek_ebene+1].Zug(zugtuple)	
				Bewertung=MM*self.Stellungsbewertung(rek_ebene+1)*-1 			# Mal Minus Eins, weil vermutlich von klein zu groß sortiert wird.
				Zugsortiert.append((Bewertung,zugtuple))
				self.Zurueck_Zug(rek_ebene,zugtuple)
			Zugsortiert.sort()
		else:
			for zugtuple in self.Stellung[rek_ebene].Zuggenerator():
				Zugsortiert.append((0.0,zugtuple))

		# Ende des Vorsortieren

		#for zugtuple in self.Stellung[rek_ebene].Zuggenerator():			# Eines Tages Legal_Generator		
		for (Bewertung,zugtuple) in Zugsortiert:
			self.Stellung[rek_ebene+1].Zug(zugtuple)	
			# Was hier noch reinkommt:
			# Eine Überprüfung dreimaliger Stellungswiederholung und evtl Patt/Matt!
			string=self.Stellung_zu_String(1)
			if(string in self.dreimalige.keys() and self.dreimalige[string]==2):
				wert=0.0
			# Pattüberprüfung: Geht erst, wenn nur legale Züge ausgespuckt werden.

			else:
				wert=self.A_B_Such_Alg(depth-1,rek_ebene+1)

			if(wert*MM > minmax*MM):
				if(rek_ebene==0):
					kandidatenzug=zugtuple
					print "depth={}".format(depth),
					print "Eval: ",
					print wert,
					print "Move: ",
					self.Zugprint(zugtuple)
					
				minmax=wert
				self.alpha_beta[rek_ebene]=wert

				# Das hier ist ein Versuch mit Toleranz+A_B: 
				Toleranz=2
				if(rek_ebene>0 and minmax*MM > (self.Bew_Histo[len(self.Bew_Histo)-1]+Toleranz*MM)*MM): 	# Falls die Bewertung schon sehr gut ist:
					break														# Raus aus der Zuggenerator-Schleife.
				# Das lässt sich einfach löschen ...

			# Hier kommt der Alpha-Beta-Pruning-Break: Wird das eine Ebene weiter unten noch Auswirkungen haben?
			if(rek_ebene>0 and wert*MM>self.alpha_beta[rek_ebene-1]*MM):
				break
	
			#self.Stellung[rek_ebene+1]=copy.deepcopy(self.Stellung[rek_ebene]) 			# Das muss noch ersetzt werden
			self.Zurueck_Zug(rek_ebene,zugtuple) # Zurueck_Zug ist eine sparsame Version von self.Stellung[rek_ebene+1]=self.Stellung[rek_ebene]

		if(rek_ebene==0):

			return (kandidatenzug,minmax)
		else:
			return minmax


	def Computer_Zug(self,depth,Toleranz):
		# self.Bew_Dict={} 							# Alpha Beta
		(kandidatenzug,minmax)=self.Such_Alg(depth,0,Toleranz)
		self.Stellung[0].Zug(kandidatenzug)

	def A_B_Computer_Zug(self,depth):
		# self.Bew_Dict={} 							# Alpha Beta
		(kandidatenzug,minmax)=self.A_B_Such_Alg(depth,0)
		self.Stellung[0].Zug(kandidatenzug)
		


# Hier versuche ich die Spielfunction durchzuführen:

# Klassen-Test
WinningPoohPrint()

IchvsDu=Partie()
IchvsDu.Stellung[0].Brett.Aufbauen()
IchvsDu.Stellung[0].Edel_Ausgabe()

while(not IchvsDu.Stellung[0].Over):

	IchvsDu.Stellung[0].Matt()
	IchvsDu.Spieler_Zug()
	IchvsDu.Stellung[0].Edel_Ausgabe()

	start_time=time.time()

	IchvsDu.Stellung[0].Matt()
	IchvsDu.A_B_Computer_Zug(4)
	end_time=time.time()

	IchvsDu.Stellung[0].Edel_Ausgabe()

sys.exit()


# Klassen-Test

IchvsDu=Partie()
IchvsDu.Stellung[0].Brett.Aufbauen()
IchvsDu.Stellung[0].Edel_Ausgabe()

# Zwei ComputerGegner - definiert durch depth und Toleranz (später noch: Bewertungsfunktion )
C_Gegner=[[2,1],[2,5]]
amZug=0
Zeitverbrauch=[0.0,0.0]
#IchvsDu.Brett.Ausgabe()
while(not IchvsDu.Stellung[0].Over):

	# IchvsDu.Spieler_Zug()
	# IchvsDu.Stellung[0].Edel_Ausgabe()

	#for x in IchvsDu.Stellung[0].Zuggenerator():

	#	print Koord_Alg[0][x[0][0]],
	#	print Koord_Alg[1][x[0][1]],
	#	print "-",
	#	print Koord_Alg[0][x[1][0]], 
	#	print Koord_Alg[1][x[1][1]]

	#IchvsDu.Stellung[0].Info()
	if(amZug):
		start_time=time.time()
		IchvsDu.Computer_Zug(2,5) #C_Gegner[amZug][0],C_Gegner[amZug][1]
		end_time=time.time()
		Zeitverbrauch[amZug]+=end_time-start_time
	else:
		start_time=time.time()
		IchvsDu.A_B_Computer_Zug(4)
		end_time=time.time()
		Zeitverbrauch[amZug]+=end_time-start_time		

	# Stellungspeicherung:
	string=IchvsDu.Stellung_zu_String(0)
	if(string in IchvsDu.dreimalige.keys()):
		IchvsDu.dreimalige[string]+=1
	else:
		IchvsDu.dreimalige[string]=1

	print "Dieser Zug von Spieler {} benötigte {} Sekunden.".format(amZug+1,end_time-start_time)
	#print "Spieler {} hat depth {} und Toleranz {}".format(amZug+1,C_Gegner[amZug][0],C_Gegner[amZug][1])
	if(amZug):
		print "Das ist das alte Modell mit Toleranz ..."
	else:
		print "Das ist das neue Alpha-Beta-Modell vollkommen intolerant ..."
	IchvsDu.Stellung[0].Edel_Ausgabe()
	amZug=(amZug+1)%2

if(IchvsDu.Stellung[0].Over):
	print "Spieler {} gewonnen!".format(((amZug+1)%2)+1)
	print "Zeitverbrauch Spieler 1: {} Sekunden.".format(Zeitverbrauch[0])
	print "Zeitverbrauch Spieler 2: {} Sekunden.".format(Zeitverbrauch[1])
	#(kandidatenzug,minmax)=IchvsDu.Such_Alg(4,0)
	#print "Dies ist die Stellungsbewertung: {}".format(minmax)
	#print "Dies ist der Gegenzug: {}{}-{}{}".format(Koord_Alg[0][kandidatenzug[0][0]],Koord_Alg[1][kandidatenzug[0][1]],Koord_Alg[0][kandidatenzug[1][0]],Koord_Alg[1][kandidatenzug[1][1]])
	#IchvsDu.Brett.Ausgabe()


# Aktuell:
# Es gibt eine Reihe von Sachen die noch fehlen, die das Programm aber vorerst vollenden würden:
# - Vorsortieren beim A_B-Pruning um vll bis depth 6 zu kommen.
# - BruteForce-Weiterrechnen von Schlagzügen mit A_B-Pruning. (Sonst zu langsam und ohne - sinnlose Bew).
# - Direktes Schlagen von Koenigen bzw Erkennen von Schach, Matt, Patt am besten im Voraus.
# - Eine Spielen-Klasse, mit der man interaktiv verschiedene Modi wählen kann ohne Code zu ändern.
# - Kurze Algebraische Notation, Partieformular, Zugrücknahme, Tipp, Kommentare, ASCII-Art, ...
# - An der Bew-Funk feilen, eventuell verschiedene erstellen (Angriffs, Endspiel, Eroeffnung ...)

# Vorsortieren hat sich bisher noch nicht als der Hammer erwiesen.
# BruteForce-Weiterrechnen ist scheißlangsam - wie man da A_B reinkriegen soll, weiß ich nicht.
# Außerdem ein fieses Problem: Warum sieht er Schwarz immer im Vorteil?
# Außerdem stellt das alte Programm plötzlich Zeug ein ... warum?
# Und A_B-Zeug ist irgendwie wieder zu langsam - vielleicht wegen Schlagzugweiterrechnen.
# Auf der letzten Ebene nicht Vorsortieren ...  Ja, scheint ein Drittel schneller zu sein.
# Aber nur bei den allerersten Zügen, danach ist das deutlich weniger. Aber ok. 
# Das wird wichtiger bei tieferem Vorsortieren.

# Ich sollte auch bei A_B noch Toleranz-Pruning einbauen. 
# Gerade dann könnte sich besseres Vorsortieren lohnen.
# Dynamische Toleranz - bei Ausgleich höher sonst niedriger, könnte sich lohnen. 
# Bei schlechter Stellung keine Toleranz ... ;-)
# Das Vorsortieren sorgt zumindest dafür, dass der König sofort geschlagen wird.






