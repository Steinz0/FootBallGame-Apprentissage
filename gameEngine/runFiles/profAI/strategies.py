from soccersimulator  import Strategy, SoccerAction, Vector2D, settings
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from .tools import SuperState, Comportement, get_random_SoccerAction
from .briques import *
import pickle
import sys
sys.path.append('../..')
from extractData.fileExtract import get_features_y, transform_state
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier


class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        return get_random_SoccerAction()

############################################ STRATEGIES DEFENSIVES ##########################################

# Stratégie - Défenseur par défaut
class DefenseurStrategy(Strategy):
    def __init__(self, lastHit):
        Strategy.__init__(self, "Defenseur")
        self.last_hit = lastHit
    def compute_strategy(self,state,id_team,id_player):
        I = ConditionDefenseur(ComportementNaif(SuperState(state,id_team,id_player), self.last_hit))
        return defenseDT(I)

############################################ STRATEGIES OFFENSIVES ##########################################

# Stratégie - Fonceur par défaut
class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Fonceur")
    def compute_strategy(self,state,id_team,id_player):
        I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player), None))
        return fonceur(I)

class ForwardStrategy(Strategy):
    def __init__(self, lastHit):
        Strategy.__init__(self,"Attaquant")
        self.last_hit = lastHit
    def compute_strategy(self,state,id_team,id_player):
        # get_features(state)
        I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player), self.last_hit))
        return forwardDT(I)

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

############################################ STRATEGIES AI MODELS ##########################################

class KNNStrategy(Strategy):
    def __init__(self, x=None, y=None, n=None, algorithm='auto', weights='uniform', lastHit=None, same_strat_step=10, name="KNNStrat") -> None:
        super(KNNStrategy,self).__init__(name)
        self.x = x
        self.y = y
        self.n = n
        self.model = KNeighborsClassifier(n_neighbors=n, algorithm=algorithm, weights=weights)
        self.predicts = {}
        self.same_strat_step = same_strat_step
        self.last_hit = lastHit

    def set_data(self, x, y):
        self.x = x
        self.y = y

    def fit_model(self, x=None, y=None):
        if x and y:
            self.model.fit(x, y)
        elif x:
            self.model.fit(x, self.y)
        elif y:
            self.model.fit(self.x, y)
        else:
            self.model.fit(self.x, self.y)

    def predictOrders(self, x):
        return self.model.predict(x)

    def score(self, x, y):
        return self.model.score(x, y)

    def compute_strategy(self,state,id_team,id_player):

        if state.step == 0 or state.step % self.same_strat_step == 0:
            x = transform_state(state,id_team,id_player)
            features, _ = get_features_y(matrix=x, getY=False)
            
            predictOrder = self.predictOrders(features)
            self.predicts[(id_team, id_player)] = predictOrder

        if self.predicts[(id_team, id_player)] == "runAdvGoal":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.dribble()
        if self.predicts[(id_team, id_player)] == "defendGoal":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseur(I)
        if self.predicts[(id_team, id_player)] == "defendCenter":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseurMid(I)
        if self.predicts[(id_team, id_player)] == "defendBall":
            I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player), self.last_hit))
            return fonceur(I)
        if self.predicts[(id_team, id_player)] == "shootBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.shoot()
        if self.predicts[(id_team, id_player)] == "clearBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.degage()

    def get_force(self,position):
        if self.best_force is not None:
            return sorted([ ((position.x-k[0])**2+(position.y-k[1])**2,v) for (k,v) in self.best_force.items()])[0][1]
        if self.strength is not None:
            return self.strength
        return None 

class SVMStrategy(Strategy):
    def __init__(self, x=None, y=None, lastHit=None, same_strat_step=1, C=1, kernel='linear',  name="SVMStrat") -> None:
        super(SVMStrategy,self).__init__(name)
        self.x = x
        self.y = y
        self.model = SVC(C=C, kernel=kernel)
        self.predicts = {}
        self.same_strat_step = same_strat_step
        self.last_hit = lastHit

    def set_data(self, x, y):
        self.x = x
        self.y = y

    def fit_model(self, x=None, y=None):
        if x and y:
            self.model.fit(x, y)
        elif x:
            self.model.fit(x, self.y)
        elif y:
            self.model.fit(self.x, y)
        else:
            self.model.fit(self.x, self.y)

    def predictOrders(self, x):
        return self.model.predict(x)

    def score(self, x, y):
        return self.model.score(x, y)

    def compute_strategy(self,state,id_team,id_player):

        if state.step == 0 or state.step % self.same_strat_step == 0:
            x = transform_state(state,id_team,id_player)
            features, _ = get_features_y(matrix=x, getY=False)
            
            predictOrder = self.predictOrders(features)
            self.predicts[(id_team, id_player)] = predictOrder

        if self.predicts[(id_team, id_player)] == "runAdvGoal":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.dribble()
        if self.predicts[(id_team, id_player)] == "defendGoal":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseur(I)
        if self.predicts[(id_team, id_player)] == "defendCenter":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseurMid(I)
        if self.predicts[(id_team, id_player)] == "defendBall":
            I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player), self.last_hit))
            return fonceur(I)
        if self.predicts[(id_team, id_player)] == "shootBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.shoot()
        if self.predicts[(id_team, id_player)] == "clearBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.degage()


class ForestClassifierStrategy(Strategy):
    def __init__(self, model='randomForest', x=None, y=None, lastHit=None, same_strat_step=1, max_depth=2, criterion='gini', class_weight='balanced', name="ForestClassifier") -> None:
        super(ForestClassifierStrategy,self).__init__(name)
        self.x = x
        self.y = y
        if model == 'randomForest':
            self.model = RandomForestClassifier(max_depth=max_depth, criterion=criterion, class_weight=class_weight, random_state=0)
        elif model == 'decisionTree':
            self.model = DecisionTreeClassifier()

        self.predicts = {}
        self.same_strat_step = same_strat_step
        self.last_hit = lastHit

    def set_data(self, x, y):
        self.x = x
        self.y = y

    def fit_model(self, x=None, y=None):
        if x and y:
            self.model.fit(x, y)
        elif x:
            self.model.fit(x, self.y)
        elif y:
            self.model.fit(self.x, y)
        else:
            self.model.fit(self.x, self.y)

    def predictOrders(self, x):
        return self.model.predict(x)

    def score(self, x, y):
        return self.model.score(x, y)

    def compute_strategy(self,state,id_team,id_player):

        if state.step == 0 or state.step % self.same_strat_step == 0:
            x = transform_state(state,id_team,id_player)
            features, _ = get_features_y(matrix=x, getY=False)
            
            predictOrder = self.predictOrders(features)
            self.predicts[(id_team, id_player)] = predictOrder

        if self.predicts[(id_team, id_player)] == "runAdvGoal":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.dribble()
        if self.predicts[(id_team, id_player)] == "defendGoal":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseur(I)
        if self.predicts[(id_team, id_player)] == "defendCenter":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseurMid(I)
        if self.predicts[(id_team, id_player)] == "defendBall":
            I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player), self.last_hit))
            return fonceur(I)
        if self.predicts[(id_team, id_player)] == "shootBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.shoot()
        if self.predicts[(id_team, id_player)] == "clearBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.degage()

class BoostingClassifier(Strategy):
    def __init__(self, x=None, y=None, lastHit=None, same_strat_step=1, max_depth=2, loss='log_loss', n_estimators=100, name="BoostingClassifier") -> None:
        super(BoostingClassifier,self).__init__(name)
        self.x = x
        self.y = y
        self.model = GradientBoostingClassifier(max_depth=max_depth, loss=loss, n_estimators=n_estimators)
        self.predicts = {}
        self.same_strat_step = same_strat_step
        self.last_hit = lastHit

    def set_data(self, x, y):
        self.x = x
        self.y = y

    def fit_model(self, x=None, y=None):
        if x and y:
            self.model.fit(x, y)
        elif x:
            self.model.fit(x, self.y)
        elif y:
            self.model.fit(self.x, y)
        else:
            self.model.fit(self.x, self.y)

    def predictOrders(self, x):
        return self.model.predict(x)

    def score(self, x, y):
        return self.model.score(x, y)

    def compute_strategy(self,state,id_team,id_player):

        if state.step == 0 or state.step % self.same_strat_step == 0:
            x = transform_state(state,id_team,id_player)
            features, _ = get_features_y(matrix=x, getY=False)
            
            predictOrder = self.predictOrders(features)
            self.predicts[(id_team, id_player)] = predictOrder

        if self.predicts[(id_team, id_player)] == "runAdvGoal":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.dribble()
        if self.predicts[(id_team, id_player)] == "defendGoal":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseur(I)
        if self.predicts[(id_team, id_player)] == "defendCenter":
            I = ConditionDefenseur(ComportementNaif(SuperState(state, id_team, id_player), None))
            return defenseurMid(I)
        if self.predicts[(id_team, id_player)] == "defendBall":
            I = ConditionAttaque(ComportementNaif(SuperState(state,id_team,id_player), self.last_hit))
            return fonceur(I)
        if self.predicts[(id_team, id_player)] == "shootBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.shoot()
        if self.predicts[(id_team, id_player)] == "clearBall":
            I = ComportementNaif(SuperState(state,id_team,id_player), None)
            return I.degage()