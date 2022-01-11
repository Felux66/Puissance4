import math
import random
import time
 
LONG = 12 #CONSTANTE DESIGNANT LA LONGUEUR DU TABLEAU
HAUT = 6 #CONSTANTE DESIGNANT LA LONGUEUR DU TABLEAU
PROF = 4 #CONSTANTE DESIGNANT LA PROFONDEUR DE RECHERCHE DE L'IA
############################## ALGO PRINCIPAL #####################################################
 
def game(IAFirst=False,IASecond=False):
    """Fonction principale permettant de jouer, IAFirst si l'IA joue en premier, IASecond sinon"""
    TheBoard = defBoard() #On définit le plateau de jeu
    tour=0 #On initialise le tour à 0
    turn = 'X' #Le premier joueur à jouer est 'X'
    j = ['X','O'] #Variable permettant de changer le joueur facilement (passée en paramètres dans plusieurs fonctions)
    tempsIA=0 #Le temps total mis par l'IA
    while (True):
        printBoard(TheBoard)
        if (IAFirst and tour%2==0): #Si l'IA joue en premier, elle joue lorsque tour%2 = 0
            t0 = time.time() #On initialise le temps du tour
            movement(TheBoard,alphaBetaMaxSearch(TheBoard,j,tour),turn) #On joue le pion de l'ia, déterminé par la fonction AlphaBetaMax car elle joue en premier
            Ttour=time.time()-t0
            tempsIA+=Ttour
            print(Ttour)
        elif (IASecond and tour%2==1): #Si l'IA joue en second, elle joue lorsque tour%2 = 1
            t0 = time.time() #On initialise le temps du tour
            movement(TheBoard,alphaBetaMinSearch(TheBoard,j,tour),turn) #On joue le pion de l'ia, déterminé par la fonction AlphaBetaMin car elle joue en second
            Ttour=time.time()-t0
            tempsIA+=Ttour
            print(Ttour)
            
        else:
            print("It's your turn," + turn + ".Move to which place?")
            move=13 #On initialise le move a 13 afin de rentrer dans le while
            while(move>11 or move<0): #On boucle tant que le joueur ne rentre pas un nombre entre 0 et 11 
                move = int(input())-1 
                if  TheBoard[5][move] != ' ': #Si le coup n'est pas disponible car la colonne est pleine, on boucle à nouveau
                    move=13
            movement(TheBoard,move,turn) #On effectue le mouvement du joueur
        
            
        if (tour>=6): #On ne va pas tester la victoire les 6 premiers coup car c'est impossible
            if (test_victoire(TheBoard)!=0): #Si la partie est terminée
                printBoard(TheBoard)
                print("\nGame Over.\n")                
                print(" **** " + turn + " won. ****")
                print("temps IA moyen:",tempsIA/(tour+1/2)+1)
                return turn,tempsIA,tour
        
        if tour >= 41: #La limite de jetons est de 42
            print(" **** Match nul. ****")   
            return 'Partie Nulle',tempsIA,tour
        
        if turn =='X':
            turn = 'O'
        else:
            turn = 'X'
        tour+=1
        
###################################### FONCTIONS AYANT TRAIT AU JEU DU PUISSANCE 4 #################################
        
def defBoard():
    """Fonction permettant d'initialiser TheBoard, qui servira de plateau de jeu pour le reste de la partie"""
    TheBoard = []
    for i in range(HAUT):
        TheBoard.append([])
        for j in range (LONG):
            TheBoard[i].append(' ')
    return(TheBoard)
 
 
def printBoard(TheBoard):
    """Affichage du plateau actuel dans le terminal"""
    for i in range(HAUT-1,0,-1):
        for j in range(LONG-1):
            print(' ' + TheBoard[i][j] + ' |', end='')
        print(' ' + TheBoard[i][j+1])
        print('---+---+---+---+---+---+---+---+---+---+---+---')
    for j in range(LONG-1):
        print(' ' + TheBoard[0][j] + ' |', end='')
    print(' ' + TheBoard[0][j+1])
    print ('\n 1   2   3   4   5   6   7   8   9   10  11  12 ') 
 
def movement(TheBoard,move,j):
    """Place le pion de la couleur 'j' à la position 'move' du tableau"""
    for i in range(6):
        if TheBoard[i][move]==' ':
            TheBoard[i][move]=j
            break
        
def test_victoire(TheBoard):
    """parcoure toutes les lignes,colonnes,diagonales afin de tester si un puissance 4 est sur le plateau"""
    for i in range(HAUT-1,2,-1):
        for j in range(LONG):
            "Teste toutes les colonnes du plateau"
            if (TheBoard[i][j] == TheBoard[i-1][j] and TheBoard[i][j] == TheBoard[i-2][j] and TheBoard[i][j] == TheBoard[i-3][j] and TheBoard[i][j]!=' '):
                return TheBoard[i][j]
        for j in range(LONG-3):
            "Teste toutes les diagonales Nord-Ouest / Sud-Est"
            if (TheBoard[i][j] == TheBoard[i-1][j+1] and TheBoard[i][j] == TheBoard[i-2][j+2] and TheBoard[i][j] == TheBoard[i-3][j+3] and TheBoard[i][j]!=' '):
                return TheBoard[i][j]
    for j in range(LONG-3):
        for i in range(HAUT):
            "Teste toutes les lignes"
            if (TheBoard[i][j] == TheBoard[i][j+1] and TheBoard[i][j] == TheBoard[i][j+2] and TheBoard[i][j] == TheBoard[i][j+3] and TheBoard[i][j]!=' '):
                return TheBoard[i][j]
        for i in range(HAUT-3):
            """Teste toutes les diagonales Sud-Ouest / Nord_Est"""
            if (TheBoard[i][j] == TheBoard[i+1][j+1] and TheBoard[i][j] == TheBoard[i+2][j+2] and TheBoard[i][j] == TheBoard[i+3][j+3] and TheBoard[i][j]!=' '):
                return TheBoard[i][j]
    return 0
 
 
        
################ •Partie IA ALPHA BETA• ############################
 
def alphaBetaMaxSearch(TheBoard,j,tour):
    """Fonction appelant la fonction récursive MinValue et retourne le coup optimal selon l'IA, recoit le plateau de jeu, le tableau des deux joueurs et le tour actuel.""" 
    actions = liste_actions(TheBoard) #On récupère tous les coups disponibles pour l'IA
    alpha=-math.inf 
    beta=math.inf
    v = alpha #On initialise alpha,beta et v en suivant le modèle alpha beta
    centres=[5.4,5.6] 
    valint=random.randint(0,1)
    centre = centres[valint] #random pour que le sorted renvoie 5 d'abord ou 6 d'abord
    action=actions[0]    
    actions = sorted(actions,key=lambda x:abs(x-centre)) #On trie les actions possibles avec leur proximité au centre
    for a in actions: 
        if(test_victoire(result(TheBoard, a, j[tour%2]))==j[tour%2]): #Si le coup est gagnant, on le joue
            return a
        v_temp = MinValue(result(TheBoard,a,j[tour%2]),alpha,beta,tour+1,j,1) #On appelle la fonction MinValue pour évaluer le coup
        if v_temp>v:
            v = v_temp
            action = a
        alpha = max(alpha,v) # On suit le principe de l'AlphaBeta
    return action
 
def alphaBetaMinSearch(TheBoard,j,tour):
    """Fonction appelant la fonction récursive MaxValue et retourne le coup optimal selon l'IA, recoit le plateau de jeu, le tableau des deux joueurs et le tour actuel.""" 
    actions = liste_actions(TheBoard) #On récupère tous les coups disponibles pour l'IA
    alpha=-math.inf
    beta=math.inf
    v = beta #On initialise alpha,beta et v en suivant le modèle alpha beta
    centres=[5.4,5.6] 
    valint=random.randint(0,1)
    centre = centres[valint] #random pour que le sorted renvoie 5 d'abord ou 6 d'abord
    action=actions[0]
    actions = sorted(actions,key=lambda x:abs(x-centre)) #On trie les actions possibles avec leur proximité au centre
    for a in actions:
        if(test_victoire(result(TheBoard, a, j[tour%2]))==j[tour%2]): #Si le coup est gagnant, on le joue
            return a
        v_temp = MaxValue(result(TheBoard,a,j[tour%2]),alpha,beta,tour+1,j,1) #On appelle la fonction MaxValue pour évaluer le coup
        if v_temp<v:
            v = v_temp
            action = a
        beta = min(beta,v) # On suit le principe de l'AlphaBeta
    return action
 
def MaxValue(TheBoard,alpha,beta,tour,j,count):
    """Fonction appelant recursivement MinValue(), TheBoard est le plateau de jeu, alpha le minimum actuel, beta le maximum actuel, tour le tour actuel, count la profondeur de recherche. Cette methode retourne la valeure maximale atteignable par l'IA""" 
    if (test_victoire(TheBoard)=='X'): # On renvoie +inf ou -inf si le jeu est termina avec les coups joués
        return math.inf
    if (test_victoire(TheBoard)=='O'):
        return -math.inf
    if (tour==42):
        return 0
    if (count==PROF): #Limite de profondeur de recherche de coup à 4 afin de limiter le temps de recherche de l'IA
        return init_score(TheBoard) #Fonction evaluant le score pour un tableau donné.
    v=-math.inf
    actions=liste_actions(TheBoard) #Listes de colonnes n'etant pas pleines.
    for a in actions: # On parcoure les actions disponibles
        v = max(v,MinValue(result(TheBoard,a,j[tour%2]),alpha,beta,tour+1,j,count+1)) #On suit l'algorithme MinMax 
        if v > beta: #Elagage alpha beta
            return v
        alpha = max(alpha,v)
    return v
    
def MinValue(TheBoard,alpha,beta,tour,j,count):
    """Fonction appelant recursivement MaxValue(), TheBoard est le plateau de jeu, alpha le minimum actuel, beta le maximum actuel, tour le tour actuel, count la profondeur de recherche. Cette methode retourne la valeure minimale atteignable par l'IA""" 
    if (test_victoire(TheBoard)=='X'): # On renvoie +inf ou -inf si le jeu est termina avec les coups joués
        return math.inf
    if (test_victoire(TheBoard)=='O'):
        return -math.inf
    if (tour==42):
        return 0
    if (count==PROF): #Limite de profondeur de recherche de coup à 4 afin de limiter le temps de recherche de l'IA
        return init_score(TheBoard) #Fonction evaluant le score pour un tableau donné.
    v=math.inf
    actions=liste_actions(TheBoard) #Listes de colonnes n'etant pas pleines.
    for a in actions: # On parcoure les actions disponibles
        v = min(v,MaxValue(result(TheBoard,a,j[tour%2]),alpha,beta,tour+1,j,count+1)) #On suit l'algorithme MinMax 
        if v<=alpha: #Elagage alpha beta
            return v
        beta = min(beta,v)
    return v
 
####################### •Partie IA Fonctions secondaires• ############################
 
def liste_actions(TheBoard):
    """Fonction retournant les colonnes qui ne sont pas pleines actuellement"""
    liste=[]
    for i in range(LONG):
        for j in range(HAUT):
            if (TheBoard[j][i]==' '): #si la colonne contient une case vide 
                liste.append(i)
                break
    return liste
 
def result(TheBoard,a,joueur):
    """Crée et renvoie un plateau de jeu contenant en plus le coup 'a' joué par le joueur 'joueur'"""
    tab=[]
    for i in range(HAUT):
        tab.append([])
        for j in range(LONG):
            tab[i].append(TheBoard[i][j])
    for i in range(HAUT):
        if tab[i][a]==' ':
            tab[i][a]=joueur
            break
    return tab
 
def pieces_manquantes(TheBoard,i,j):
    """Fonction renvoyant le nombres de cases vide sous la ligne i de la colonne j"""
    for haut in range(i):
        if TheBoard[haut][j]==" ":
            return i-haut
    return 0
 
def init_score(TheBoard):
    """Fonction permettant d'evaluer le score d'un plateau à l'heure actuelle.
    On analyse chaque suite de 4 cases en lignes, colonnes ou diagonales qu'on passe a la fonction score.
    courant va contenir les 4 cases ainsi que le nombre de pions manquants pour atteindre ces 4 cases."""
    note = 0
    courant=[]
    for i in range(HAUT-1,2,-1):
        for j in range(LONG):
            if (TheBoard[i][j]==TheBoard[i-1][j] and TheBoard[i][j]==TheBoard[i-2][j] and TheBoard[i][j]==" "):
              note+=0
              continue
            courant.append(TheBoard[i][j])
            courant.append(TheBoard[i-1][j])
            courant.append(TheBoard[i-2][j])
            courant.append(TheBoard[i-3][j])
            courant.append(HAUT-pieces_manquantes(TheBoard,i,j))
            courant.append(HAUT-pieces_manquantes(TheBoard,i-1,j))
            courant.append(HAUT-pieces_manquantes(TheBoard,i-2,j))
            courant.append(HAUT-pieces_manquantes(TheBoard,i-3,j))
            note += score(courant)
            courant = []
        for j in range(LONG-3):
            if (TheBoard[i][j]==TheBoard[i-1][j+1] and TheBoard[i][j]==TheBoard[i-2][j+2] and TheBoard[i][j]==" "):
              note+=0
              continue
            courant.append(TheBoard[i][j])
            courant.append(TheBoard[i-1][j+1])
            courant.append(TheBoard[i-2][j+2])
            courant.append(TheBoard[i-3][j+3])
            courant.append(HAUT-pieces_manquantes(TheBoard,i,j))
            courant.append(HAUT-pieces_manquantes(TheBoard,i-1,j+1))
            courant.append(HAUT-pieces_manquantes(TheBoard,i-2,j+2))
            courant.append(HAUT-pieces_manquantes(TheBoard,i-3,j+3))
            note += score(courant)
            courant = []
    for j in range(LONG-3):
        for i in range(HAUT):
            if (TheBoard[i][j]==TheBoard[i][j+1] and TheBoard[i][j]==TheBoard[i][j+2] and TheBoard[i][j]==" "):
              note+=0
              continue
            courant.append(TheBoard[i][j])
            courant.append(TheBoard[i][j+1])
            courant.append(TheBoard[i][j+2])
            courant.append(TheBoard[i][j+3])
            courant.append(HAUT-pieces_manquantes(TheBoard,i,j))
            courant.append(HAUT-pieces_manquantes(TheBoard,i,j+1))
            courant.append(HAUT-pieces_manquantes(TheBoard,i,j+2))
            courant.append(HAUT-pieces_manquantes(TheBoard,i,j+3))
            note += score(courant)
            courant = []
        for i in range(HAUT-3):
            if (TheBoard[i][j]==TheBoard[i+1][j+1] and TheBoard[i][j]==TheBoard[i+2][j+2] and TheBoard[i][j]==" "):
              note+=0
              continue
            courant.append(TheBoard[i][j])
            courant.append(TheBoard[i+1][j+1])
            courant.append(TheBoard[i+2][j+2])
            courant.append(TheBoard[i+3][j+3])
            courant.append(HAUT-pieces_manquantes(TheBoard,i,j))
            courant.append(HAUT-pieces_manquantes(TheBoard,i+1,j+1))
            courant.append(HAUT-pieces_manquantes(TheBoard,i+2,j+2))
            courant.append(HAUT-pieces_manquantes(TheBoard,i+3,j+3))
            note += score(courant)
            courant = []
    return note
 
def score(ligne):
    """Cette fonction recoit un tableau de 8 cases, les 4 premières contiennent les pions d'une ligne
    et les 4 suivantes le nombre de coup minimum necessaire pour atteindre respectivement chacune des cases"""
    for i in range(4):
        if (ligne[i]==' '):
            if (ligne[(i+1)%4]==' ' and ligne[(i+2)%4]==ligne[(i+3)%4]): #On teste ici si la ligne est de la forme "X- - -X" ou " -X-X- ", resp "O- - -0" ou " -0-0- " 
                if (i!=1): #On differencie ici "X- - -X" de " -X-X- ", resp "O- - -0" de " -0-0- "
                    if (ligne[(i+2)%4]=='X'): #On somme si c'est une ligne contenant des "X"
                        return(16 + min(ligne[i+4],ligne[((i+1)%4)+4]))
                    elif (ligne[(i+2)%4]=='O'): #On soustrait si c'est une ligne contenant des "O"
                        return(-1*(16 + min(ligne[i+4],ligne[((i+1)%4)+4])))
                else:
                    if (ligne[(i+2)%4]=='X'): 
                        return(8 + min(ligne[i+4],ligne[((i+1)%4)+4]))
                    elif (ligne[(i+2)%4]=='O'):
                        return(-1*(8 + min(ligne[i+4],ligne[((i+1)%4)+4])))
            if (ligne[(i+2)%4]==' ' and ligne[(i+1)%4]==ligne[(i+3)%4]): #On teste ici si la ligne est de la forme "X- -X- " ou " -X- -X", resp "O- -O- " ou " -O- -O"
                if (ligne[(i+1)%4]=='X'):
                    return(12 + min(ligne[i+4],ligne[((i+2)%4)+4]))
                elif (ligne[(i+1)%4]=='O'):
                    return(-1*(12 + min(ligne[i+4],ligne[((i+2)%4)+4])))
            if (ligne[(i+1)%4]==ligne[(i+2)%4] and ligne[(i+1)%4]==ligne[(i+3)%4]): #On teste ici si la ligne est de la forme " -X-X-X", "X- -X-X", "X-X- -X" ou "X-X-X- ", resp " -O-O-O", "O- -O-O", "O-O- -O" ou "O-O-O- "
                if (ligne[(i+1)%4]=='X'):
                    return(40 + ligne[i+4])
                elif (ligne[(i+1)%4]=='O'):
                    return(1*(40 + ligne[i+4]))
    return 0
