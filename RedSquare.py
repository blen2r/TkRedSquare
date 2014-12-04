########################
#                      #
# Pierre-Emmanuel Viau #
#                      #
# Jeu RedSquare        #
#                      #
########################
from Tkinter import *
from time import *
import tkMessageBox

################### Modele ###########################
class Fichier:  
    def __init__(self):
        pass
    
    def ouvrirFichier(self, nomFiche):
        fiche = file(nomFiche+".txt")
        donnees = fiche.readlines()
        fiche.close()
        return donnees
    
    def sauverFichier(self, nomFiche, donnees):
        fiche = file(nomFiche+".txt","w")
        
        for i in donnees:
            fiche.write(i)
        
        fiche.close()

####
####
class Score:
    def __init__(self):
        self.fichier = "score" #nom du fichier ou son stocker les scores
        self.load = Fichier()
        self.listeScore = []
        
    def loaderScore(self):
        self.listeScore = self.load.ouvrirFichier(self.fichier)
        for i in self.listeScore:
            i = i[:-1]
            
    def saverScore(self, nom, score): 
        self.loaderScore()
        
        #on load le fichier, on ajoute les nouveaux scores et on resave
        scoreAssemble ='A'+','+nom+','+str(score[0])+'\n'
        self.listeScore.append(scoreAssemble)
        scoreAssemble ='B'+','+nom+','+str(score[1])+'\n'
        self.listeScore.append(scoreAssemble)
        scoreAssemble ='C'+','+nom+','+str(score[2])+'\n'
        self.listeScore.append(scoreAssemble)
        
        self.load.sauverFichier(self.fichier, self.listeScore)
        
    def getMeilleurScore(self):
        self.loaderScore()
        
        #meilleur score et position dans la liste
        meilleurA = -1
        refMeilleurA = 0
        meilleurB = -1
        refMeilleurB = 0
        meilleurC = -1
        refMeilleurC = 0
        
        #on passe dans la liste des scores et on regarde si c'est le meilleur score pour son niveau, si oui on en garde une reference
        for i in self.listeScore:
            i = i[:-1]
            entree = i.split(',')
            if entree[0] == 'A':
                if float(entree[2]) > meilleurA:
                    meilleurA = float(entree[2])
                    refMeilleurA = i 
            if entree[0] == 'B':
                if float(entree[2]) > meilleurB:
                    meilleurB = float(entree[2])
                    refMeilleurB = i 
            if entree[0] == 'C':
                if float(entree[2]) > meilleurC:
                    meilleurC = float(entree[2])
                    refMeilleurC = i 
            
        return refMeilleurA, refMeilleurB, refMeilleurC

####
####
class Joueur:
    def __init__(self): 
        self.nom = ""
        self.dernierScore = [0,0,0]
        self.niveau = 'A'
        self.meilleurScoreSession = [0,0,0]
        
    def calcScore(self, score):
        #on update le dernier score et on regarde si c'est le meilleur de la session
        i = 0
        if self.niveau == 'A':
            i = 0
        elif self.niveau == 'B':
            i = 1
        else:
            i = 2
        
        self.dernierScore[i] = score
        if score > self.meilleurScoreSession[i]:
            self.meilleurScoreSession[i] = score

###################  Vue  #############################      
class Interface:
    def __init__(self, leController=None):
        ##TK
        self.root = Tk()
        self.largeur = 850
        self.hauteur = 600
        self.root.title("RedSquare P.E. Viau 2008")
        self.root.geometry("%dx%d%+d%+d" % (self.largeur, self.hauteur, 0, 0)) #taille fenetre
        self.leController=leController
        
        ##la zone de jeu
        self.largeurJeu = 550
        self.hauteurJeu = 600
        
        ##map
        self.map = Map(master=self.root, x=0, y=0, width=self.largeurJeu-5, height=self.hauteurJeu-5, leController=leController, interface=self)
        
        #les boutons et labels pour le score
        self.largeurZoneBut = self.largeur-self.largeurJeu
        self.hauteurZoneBut = 600
        self.zoneBoutons = Canvas(self.root,width=self.largeurZoneBut, height=self.hauteurZoneBut, highlightthickness=2, highlightbackground="black")
        
        self.nomTemp = StringVar()
        self.tNomJoueur = Label(self.zoneBoutons, textvariable=self.nomTemp, font=("Helvetica", 16))
        self.tNomJoueur.place(x=self.largeurZoneBut/2, y=50, anchor=N)
        
        
        self.bNivA = Button(master=self.zoneBoutons, command=self.comA, text="A", font=("Helvetica", 14))
        self.bNivA.place(x=self.largeurZoneBut/3-50, y=self.hauteurZoneBut-100, anchor=NW)
        
        self.bNivB = Button(master=self.zoneBoutons, command=self.comB, text="B", font=("Helvetica", 14))
        self.bNivB.place(x=self.largeurZoneBut/3*2-50, y=self.hauteurZoneBut-100, anchor=NW)
        
        self.bNivC = Button(master=self.zoneBoutons, command=self.comC, text="C", font=("Helvetica", 14))
        self.bNivC.place(x=self.largeurZoneBut-50, y=self.hauteurZoneBut-100, anchor=NW)
        
        self.bMeilleursScores = Button(master=self.zoneBoutons, command=self.comScores, text="Afficher les meilleurs", font=("Helvetica", 14))
        self.bMeilleursScores.place(x=self.largeurZoneBut/2, y=self.hauteurZoneBut/2+40, anchor=N)
        
        self.bReset = Button(master=self.zoneBoutons, command=self.reset, text="Reset", font=("Helvetica", 14))
        self.bReset.place(x=self.largeurZoneBut/3*2-70, y=self.hauteurZoneBut-170, anchor=NW)
        
        #affichage des scores
        self.tScore = Label(self.zoneBoutons, text="Scores       A         B         C", font=("Helvetica", 14))
        self.tScore.place(x=10, y=80, anchor=NW)
        
        self.meilleurTemp = StringVar()
        self.tMeilleur = Label(self.zoneBoutons, textvariable=self.meilleurTemp, font=("Helvetica", 14))
        self.tMeilleur.place(x=10, y=130, anchor=NW)
        
        self.sessionTemp = StringVar()
        self.tSession = Label(self.zoneBoutons, textvariable=self.sessionTemp, font=("Helvetica", 14))
        self.tSession.place(x=10, y=160, anchor=NW)
        
        self.dernierTemp = StringVar()
        self.tDernier = Label(self.zoneBoutons, textvariable=self.dernierTemp, font=("Helvetica", 14))
        self.tDernier.place(x=10, y=190, anchor=NW)
        
        #les meilleurs scores ainsi que le nom des joueurs de ces scores
        self.scoreMA = None
        self.scoreMB = None
        self.scoreMC = None
        self.nomMA = None
        self.nomMB = None
        self.nomMC = None
        
        
        #entrer le nom
        self.menu = Canvas(self.root,width=self.largeur, height=self.hauteur, highlightthickness=0)
        self.imageMenu = PhotoImage(file="fondMenu.gif")
        self.fondMenu = self.menu.create_image(0, 0, anchor=NW, image=self.imageMenu)
        
        self.EntreNom = Label(self.menu, text="Entrez votre nom", font=("Helvetica", 14), bg="white")
        self.EntreNom.place(x=(self.largeur - self.EntreNom.winfo_width())/2, y=self.hauteur-280,anchor=S)
        self.champTxt = Entry(self.menu)
        self.champTxt.place(x=(self.largeur - self.champTxt.winfo_width())/2, y=self.hauteur-220, anchor=S)
        self.butOk = Button(master=self.menu, text="Okay", command=self.appliquer)
        self.butOk.place(x=(self.largeur - self.butOk.winfo_width())/2, y=self.hauteur-180,anchor=S)
        
        #debut de l'application
        self.afficherMenu()
        self.root.protocol("WM_DELETE_WINDOW", self.quitter) #enregistrer les scores a la fermeture
        self.root.mainloop()
        
        
    def quitter(self):
        #enregistre les scores
        self.leController.quit() 
        self.root.destroy()
        sys.exit(1)
        
    def appliquer(self):
        #on enregistre le nom, cache le menu, affiche le score et le jeu 
        self.cacherMenu()
        self.leController.leJoueur.nom = self.champTxt.get()
        
        #meilleurs scores
        lesScoresM = self.leController.lesScores.getMeilleurScore()
        self.scoreMA = float(lesScoresM[0].split(',')[2])
        self.scoreMB = float(lesScoresM[1].split(',')[2])
        self.scoreMC = float(lesScoresM[2].split(',')[2])
        
        self.scoreMA = str(round(self.scoreMA,2))
        self.scoreMB = str(round(self.scoreMB,2))
        self.scoreMC = str(round(self.scoreMC,2))
        
        #noms des champions
        self.nomA = lesScoresM[0].split(',')[1]
        self.nomB = lesScoresM[1].split(',')[1]
        self.nomC = lesScoresM[2].split(',')[1]
        
        self.nomTemp.set("Nom: " + self.leController.leJoueur.nom)
        self.meilleurTemp.set("Meilleur:    "+self.scoreMA+"    "+self.scoreMB+"    "+self.scoreMC)
        self.sessionTemp.set("Session:     ")
        self.dernierTemp.set("Dernier:    ")
        
        self.afficher()        
       
        
    ##changer le niveau du jeu
    def comA(self):
        self.leController.leJoueur.niveau = 'A'
        self.reset()
    
    def comB(self):
        self.leController.leJoueur.niveau = 'B'
        self.reset()
    
    def comC(self):
        self.leController.leJoueur.niveau = 'C'
        self.reset()
        
    ##afficher un messageBox avec les meilleurs scores    
    def comScores(self):
        mess = "A: "+self.nomA+" "+self.scoreMA+"\n"+"B: "+self.nomB+" "+self.scoreMB+"\n"+"C: "+self.nomC+" "+self.scoreMC+"\n"
        tkMessageBox.showinfo("Meilleurs Scores", mess)
    
    def cacher(self):
        self.zoneBoutons.place_forget()
        self.map.cacher()
        
    def afficherMenu(self):
        self.menu.place(x=0, y=0, anchor=NW)
    
    def cacherMenu(self):
        self.menu.place_forget()
    
    def afficher(self):
        self.zoneBoutons.place(x=self.largeurJeu, y=0, anchor=NW)
        self.map.afficher()
        
    def reset(self):
        #on detruit la map (pour arretter tous les timers) et on refait une nouvelle map
        self.map.cacher()
        self.map.arretter()
        self.map.detruire()
        self.map = Map(master=self.root, x=0, y=0, width=self.largeurJeu-5, height=self.hauteurJeu-5, leController=self.leController, interface=self)
        self.afficher()
        
####
####   
class Map:
    def __init__(self, master=None, x=0, y=0, width=100, height=100, tempsDepl=10, leController=None, tempsDifficulte=5000, interface=None):
        self.master = master
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vueNoir = Canvas(master = self.master, background="black", width=self.width, height=self.height)
        self.vueBlanc = self.vueNoir.create_rectangle(25, 25, self.width-25, self.height-25, fill="white")
        self.leController=leController
        self.partieActive = False
        self.interface=interface
        
        self.leCarreRouge = None
        self.lesCarresBleus = []
        self.lesMines= []
        
        self.tempsDepl = tempsDepl #vitesse d'update du jeu
        
        self.tempsPasse = 0 
        self.tempsFin = 0
        self.tempsDebut = 0
        self.tempsDifficulte=tempsDifficulte #temps qui passe avant augmentation de la vitesse
        
        #carres bleus
        self.lesCarresBleus.append(CarreBleu(self.vueNoir,x=50,y=50,dx=1, dy=1, width=70, height=50, vitesse=2, partieEnCours=False, map=self))
        self.lesCarresBleus.append(CarreBleu(self.vueNoir,x=100,y=400,dx=1, dy=-1, width=110, height=40, vitesse=2, partieEnCours=False, map=self))
        self.lesCarresBleus.append(CarreBleu(self.vueNoir,x=400,y=300,dx=-1, dy=1, width=30, height=90, vitesse=2, partieEnCours=False, map=self))
        self.lesCarresBleus.append(CarreBleu(self.vueNoir,x=400,y=70,dx=-1, dy=1, width=50, height=50, vitesse=2, partieEnCours=False, map=self))
        self.lesCarresBleus.append(CarreBleu(self.vueNoir,x=300,y=400,dx=1, dy=1, width=60, height=60, vitesse=2, partieEnCours=False, map=self))
        
        #carres bleus additionnels
        if self.leController.leJoueur.niveau == 'B':
            self.lesCarresBleus.append(CarreBleu(self.vueNoir,x=200,y=200,dx=1, dy=1, width=30, height=30, vitesse=2, partieEnCours=False, map=self))
            self.lesCarresBleus.append(CarreBleu(self.vueNoir,x=400,y=400,dx=-1, dy=-1, width=110, height=40, vitesse=2, partieEnCours=False, map=self))
        #mines
        if self.leController.leJoueur.niveau == 'C':
            self.lesMines.append(Mine(master=self.vueNoir, x=200, y=200, width=50, height=50, map=self))
            self.lesMines.append(Mine(master=self.vueNoir, x=400, y=400, width=50, height=50, map=self))
            self.lesMines.append(Mine(master=self.vueNoir, x=150, y=450, width=50, height=50, map=self))
        
        #le carre rouge...
        self.leCarreRouge = CarreRouge(master=self.vueNoir, map=self, x=self.width/2, y=self.height/2)

    
    def detruire(self):
        self.vueNoir.destroy()
        
    def afficher(self):
        self.vueNoir.place(x=self.x, y=self.y, anchor=NW)
        
        for i in self.lesCarresBleus:
            i.afficher()
            
        self.update()
        self.leCarreRouge.afficher()
        
        
    def cacher(self):
        self.vueNoir.place_forget()

    def update(self):
        if self.partieActive==True: #si le jeu n'est pas arrete
            for i in self.lesCarresBleus:
                i.deplacer()
                
            for i in self.lesMines:
                i.collision()
    
            
            self.master.after(self.tempsDepl, self.update)
        
    def demarrer(self):
        self.partieActive = True
        self.tempsDebut = time()
        for i in self.lesCarresBleus:
            i.partieEnCours = True
        self.update()
        self.vueNoir.after(self.tempsDifficulte, self.augDiff) #acceler le jeu a toutes les x secondes
            
    def arretter(self):
        self.leCarreRouge.actif = False #paralyse le carre rouge
        if self.partieActive == True:
            self.tempsFin = time()
            self.tempsPasse = self.tempsFin - self.tempsDebut 
            
            self.leController.leJoueur.calcScore(self.tempsPasse) #attribue le score au joueur
            self.interface.dernierTemp.set("Dernier:    "+str(round(self.leController.leJoueur.dernierScore[0],2))+"   "+str(round(self.leController.leJoueur.dernierScore[1],2))+"  "+str(round(self.leController.leJoueur.dernierScore[2],2)))
            self.interface.sessionTemp.set("Session:   "+str(round(self.leController.leJoueur.meilleurScoreSession[0],2))+"   "+str(round(self.leController.leJoueur.meilleurScoreSession[1],2))+"  "+str(round(self.leController.leJoueur.meilleurScoreSession[2],2)))
            
            self.partieActive = False
        
        for i in self.lesCarresBleus: #paralyse les carres bleus
            i.partieEnCours = False
            
    def augDiff(self):
        for i in self.lesCarresBleus:
            i.vitesse = i.vitesse+2
        self.vueNoir.after(self.tempsDifficulte, self.augDiff)
    
####
####
class Mine:
    def __init__(self, master=None, x=50, y=50, color="green", width=50, height=50, map=None):
      self.master = master
      self.x = x
      self.y = y
      self.color = color
      self.width = width
      self.height = height
      self.vue = None
      self.map = map
      
      self.afficher()
            
    def collision(self):
        lesElements = self.master.find_overlapping(self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y +self.height/2)
        for i in lesElements:
            lesTags = self.master.gettags(i)
            if len(lesTags) > 0:
                if lesTags[0] == "carreRouge": #si le carre rouge lui touche
                    self.map.arretter()##declancher fin de jeu
    
    def cacher(self):
        self.master.delete(self.vue)
        self.vue = None
        
    def afficher(self):
        self.vue = self.master.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill=self.color, width=0, tags="carreBleu")

####
####
class CarreBleu:
    def __init__(self, master=None, x=50, y=50, color="blue", width=50, height=50, dx=0, dy=0, vitesse=0, partieEnCours=False, tempsDepl=100, map=None):
        self.master = master
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.vitesse = vitesse
        self.color = color
        self.width = width
        self.height = height
        self.vue = None
        self.partieEnCours = partieEnCours
        self.tempsDepl = tempsDepl
        self.map = map
        
    def deplacer(self):
        if self.partieEnCours == True:
            self.x = self.x + (self.dx*self.vitesse)
            self.y = self.y + (self.dy*self.vitesse)
            self.master.move(self.vue, self.dx*self.vitesse, self.dy*self.vitesse)
            self.collision()
            
    def collision(self): #collisions avec les bords
        if self.x-self.width/2 <= 0 or self.x+self.width/2 >= self.map.width:
            self.dx = -1 * self.dx
        if self.y-self.height/2 <= 0 or self.y+self.height/2 >= self.map.height:
            self.dy = -1 * self.dy
            
        lesElements = self.master.find_overlapping(self.x - self.width/2, self.y - self.height/2, self.x + self.width/2, self.y +self.height/2)
        for i in lesElements:
            lesTags = self.master.gettags(i)
            if len(lesTags) > 0:
                if lesTags[0] == "carreRouge": #si le carre rouge lui touche
                    self.map.arretter() ##declancher fin de jeu
    
    def cacher(self):
        self.master.delete(self.vue)
        self.vue = None
        
    def afficher(self):
        self.vue = self.master.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill=self.color, width=0, tags="carreBleu")
####
####
class CarreRouge:
    def __init__(self, master=None, x=50, y=50, color="red", width=50, height=50, map=None, actif=True):
        self.master = master
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.vue = None
        self.nbrClic = 0
        self.map = map
        self.actif = actif
        
    def cacher(self):
        self.master.delete(self.vue)
        self.vue = None
        
    def afficher(self):
        self.vue = self.master.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill=self.color, tags="carreRouge")
        self.master.tag_bind("carreRouge","<ButtonPress-1>", self.appuyer)
        self.master.tag_bind("carreRouge", "<ButtonRelease-1>", self.relacher)#
        
    def collisions(self):
        #collisions avec les bords
        if self.x - self.width/2 <= 25 or self.x + self.width/2 >= self.master.winfo_width()-25:
            self.map.arretter() ##declancher fin de jeu
            self.actif = False
            
        if self.y - self.height/2 <= 25 or self.y + self.height/2 >= self.master.winfo_height()-25:
            self.map.arretter()##declancher fin de jeu
            self.actif = False
    
    ###Drag 'n' Drop
    def appuyer(self, event):
        self.nbrClic = self.nbrClic+1
        if self.nbrClic == 1:
            self.map.demarrer() #demarrer partie
            
        self.master.tag_bind("carreRouge","<Motion>", self.deplacer)
    
    def deplacer(self, event):
        if self.actif == True:
            self.x = event.x
            self.y = event.y
            self.master.coords(self.vue, self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2)
        
        self.collisions()
    
    def relacher(self, event):
        self.master.tag_unbind("carreRouge","<Motion>")   
    
################### Controller ######################## 
class Controller:
    def __init__(self):
        self.lesScores = Score()
        self.leJoueur = Joueur()
        self.interface = Interface(leController=self)
        
    def quit(self):
        self.lesScores.saverScore(self.leJoueur.nom, self.leJoueur.meilleurScoreSession)
    
################### Main ##############################
if __name__ == "__main__": 
    test=Controller()