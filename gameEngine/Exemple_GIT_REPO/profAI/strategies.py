from soccersimulator  import Strategy, SoccerAction, Vector2D, settings
from .tools import SuperState, Comportement, get_random_SoccerAction
from .briques import *
import pickle

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return get_random_SoccerAction()

############################################ STRATEGIES DEFENSIVES ##########################################

# Stratégie - Défenseur par défaut
class DefenseurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defenseur")
    def compute_strategy(self,state,id_team,id_player):
        I = ConditionDefenseur(ComportementNaif(SuperState(state,id_team,id_player)))
        return defenseur(I)

# Stratégie - Défenseur traditionnel
class TradDefStrategy(Strategy) :
    # Init
    def __init__(self, coefDef, coefBall):
        Strategy.__init__(self, "Defenseur Traditionnel")
        self.COEF_DEF = coefDef
        self.COEF_BALL = coefBall

    # Calcul de strategie
    def compute_strategy(self, state, id_team, id_player):
        I = ConditionTraditionalDefender(ComportementNaif(SuperState(state,id_team,id_player)), self.COEF_DEF, self.COEF_BALL)
        return tradDefenseur(I)

############################################ STRATEGIES EQUILIBREES ##########################################

# Stratégie - Passeur fou
class CrazyPassStrategy(Strategy) :
    # Init
    def __init__(self, coefPass, coefBall, coefGoal):
        Strategy.__init__(self, "Passeur Fou")
        self.COEF_PASS = coefPass
        self.COEF_BALL = coefBall
        self.COEF_GOAL = coefGoal

    # Calcul de stratégie
    def compute_strategy(self, state, id_team, id_player):
        I = ConditionCrazyPass(ComportementNaif(SuperState(state, id_team, id_player)), self.COEF_PASS, self.COEF_BALL, self.COEF_GOAL)
        return crazyPasser(I)

############################################ STRATEGIES OFFENSIVES ##########################################

# Stratégie - Fonceur par défaut
class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Fonceur")
    def compute_strategy(self,state,id_team,id_player):
        I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player)))
        return fonceur(I)

class FonceurTestStrategy(Strategy):
    def __init__(self, strength=None,fn=None):
        Strategy.__init__(self,"Fonceur")
        self.strength = strength
        self.best_force = None
        if fn is not None:
            import os
            fn=os.path.join(os.path.dirname(os.path.realpath(__file__)),fn)
            with open(fn,"rb") as f:
                self.best_force = pickle.load(f)
    def compute_strategy(self,state,id_team,id_player):
        C = ComportementNaif(SuperState(state,id_team,id_player))
        shoot_coef = self.get_force(C.me)
        if shoot_coef is not None:
            C.SHOOT_COEF = shoot_coef
        I = ConditionAttaque(C)
        return fonceur(I)
    def get_force(self,position):
        if self.best_force is not None:
            return sorted([ ((position.x-k[0])**2+(position.y-k[1])**2,v) for (k,v) in self.best_force.items()])[0][1]
        if self.strength is not None:
            return self.strength
        return None 