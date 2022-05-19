from soccersimulator import SoccerTeam, Simulation, KeyboardStrategy,DTreeStrategy,load_jsonz,dump_jsonz, show_simu
from soccersimulator import apprend_arbre, build_apprentissage, genere_dot
from profAI import FonceurStrategy,DefenseurStrategy,SuperState
from profAI import strategies as st
import sklearn
import numpy as np
import pickle

assert sklearn.__version__ >= "0.18.1","Updater sklearn !! (pip install -U sklearn --user )"

class LastHit() :
    def __init__(self) :
        self.LH = (0,0)
    def update(self, key) :
        self.LH = key
    def reset(self) :
        self.LH = (0,0)

### Transformation d'un etat en features : state,idt,idp -> R^d

def my_get_features(state,idt,idp):
    """ extraction du vecteur de features d'un etat, ici distance a la balle, distance au but, distance balle but """
    state = SuperState(state,idt,idp)
    f1 = state.distance(state.ball_p)
    f2 = state.distance(state.my_goal)
    f3 = state.ball_p.distance(state.my_goal)
    return [f1,f2,f3]

my_get_features.names = ["dball","dbut","dballbut"]


def entrainer(fname):
    #Creation d'une partie
    
    lh = LastHit()
    
    kb_strat = KeyboardStrategy()
    kb_strat.add("a",st.ForwardStrategy(lh))
    kb_strat.add("z",st.DefenseurStrategy(lh))
    
    team1 = SoccerTeam(name="Contol Team")
    team2 = SoccerTeam(name="Sparing")
    team1.add("ControlPlayer",kb_strat)
    team2.add("Player",st.ForwardStrategy(lh)) 
    simu = Simulation(team1,team2)
    #Jouer, afficher et controler la partie
    show_simu(simu)
    print("Nombre d'exemples : "+str(len(kb_strat.states)))
    # Sauvegarde des etats dans un fichier
    dump_jsonz(kb_strat.states,fname)

def apprendre(exemples, get_features,fname=None):
    #genere l'ensemble d'apprentissage
    data_train, data_labels = build_apprentissage(exemples,get_features)
    ## Apprentissage de l'arbre
    dt = apprend_arbre(data_train,data_labels,depth=10,feature_names=get_features.names)
    ##Sauvegarde de l'arbre
    if fname is not None:
        with open(fname,"wb") as f:
            pickle.dump(dt,f)
    return dt

if __name__=="__main__":
    entrainer("test_kb_strat.jz")

    lh = LastHit()
    dic_strategy = {st.ForwardStrategy(lh).name:st.ForwardStrategy(lh), st.DefenseurStrategy(lh).name:st.DefenseurStrategy(lh)}

    states_tuple = load_jsonz("test_kb_strat.jz")
    apprendre(states_tuple,my_get_features,"tree_test.pkl")
    with open("tree_test.pkl","rb") as f:
        dt = pickle.load(f)
    # Visualisation de l'arbre
    genere_dot(dt,"test_arbre.dot")
    #Utilisation de l'arbre : arbre de decision, dico strategy, fonction de transformation etat->variables
    treeStrat1 = DTreeStrategy(dt,dic_strategy,my_get_features)
    treeteam = SoccerTeam("Arbre Team")
    team2 = SoccerTeam(name="Sparing")
    treeteam.add("Joueur 1",treeStrat1)
    treeteam.add("Joueur 2",treeStrat1)
    team2.add("Joueur 1", st.ForwardStrategy(lh))
    team2.add("Joueur 2",st.DefenseurStrategy(lh))
    simu = Simulation(treeteam,team2)
    show_simu(simu)

