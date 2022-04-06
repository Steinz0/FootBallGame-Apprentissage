from typing_extensions import Self
from .tools import SuperState, Comportement, ProxyObj
from soccersimulator import Vector2D,SoccerAction
from soccersimulator.settings import PLAYERS_PER_TEAM, maxPlayerShoot, maxPlayerSpeed,maxPlayerAcceleration

############################################ CLASSE COMPORTEMENT RACINE ##########################################

class ComportementNaif(Comportement):
    # Coefficients d'actions
    RUN_COEF = maxPlayerAcceleration
    GO_COEF = maxPlayerAcceleration / 3.

    SHOOT_COEF = maxPlayerShoot
    DRIBBLE_COEF = maxPlayerShoot / 3.
    THROW_COEF = maxPlayerShoot
    PASS_COEF = maxPlayerShoot / 2.

    # Coefficients de situation

    # Init
    def __init__(self,state):
        super(ComportementNaif,self).__init__(state)

    # Action - Courir vers
    def run(self,p):
        return SoccerAction(acceleration=(p-self.me).normalize()*self.RUN_COEF)
    
    # Action - Se déplacer vers
    def go(self,p):
        return SoccerAction(acceleration=(p-self.me).normalize()*self.GO_COEF)

    # Action - Tirer la balle
    def shoot(self,shoot_coef=None):
        if shoot_coef is None:
            shoot_coef = self.SHOOT_COEF
        if self.can_kick:
            return SoccerAction(shoot=(self.his_goal-self.ball_p).normalize()*self.SHOOT_COEF)
        return SoccerAction()

    # Action - Dégager la balle
    def degage(self):
        if self.can_kick:
            return SoccerAction(shoot=(self.his_goal-self.ball_p).normalize()*self.THROW_COEF)
        return SoccerAction()

    # Action - Tirer la balle dans une direction précision
    def kick(self, p) :
        if self.can_kick :
            # On récupère les coéquipiers
            return SoccerAction(shoot=(p - self.ball_p).normalize()*self.PASS_COEF)
        return SoccerAction()

    # Action - Marquer le joueur adverse le plus proche de moi
    def marquageProche(self) :
        # Variables de recherche
        markDistance = 1000000
        markID = 0

        # On itère sur les joueurs adverses
        for id in range(PLAYERS_PER_TEAM) :
            dist = self.me.distance(self.player_state(self.his_team, id).position)
            if (dist < markDistance) :
                markDistance = dist
                markID = id

        # On se déplace vers le joueur adverse ciblé
        targetPos = self.player_state(self.his_team, markID).position
        return SoccerAction(acceleration=(targetPos - self.me).normalize()*self.RUN_COEF)

    # Action - Marquer le joueur adverse le plus proche des cages
    def marquageProcheBalle(self) :
        # On recupere la position de l'adversaire le plus proche de la balle
        pos = self.advClosestBall()
        return self.go(pos)

    # Recherche - Coéquipier le plus proche et renvoie sa position
    def findClosestTeammate(self) :
        # Variables de recherche
        tmDistance = 1000000
        tmID = 0
        (idT , idP) = self.key # Indice à ne pas étudier (il s'agit du joueur lui-même)

        # On itère sur les joueurs de l'équipe
        for id in range(PLAYERS_PER_TEAM) :
            if (id != idP) :
                dist = self.me.distance(self.player_state(idT, idP).position)
                if (dist < tmDistance) :
                    tmDistance = dist
                    tmID = id

        # On retourne la position du coéquipier
        return self.player_state(idT, tmID).position

    # Recherche - Retourne la position de l'adversaire le plus proche de soi
    def advClosestSelf(self) :
        # Variables de recherche
        advDistance = 1000000
        advID = 0

        # On itère sur les joueurs adverses
        for id in range(PLAYERS_PER_TEAM) :
            dist = self.me.distance(self.player_state(self.his_team, id).position)
            if (dist < advDistance) :
                advDistance = dist
                advID = id

        # On se déplace vers le joueur adverse ciblé
        return self.player_state(self.his_team, advID).position

    # Recherche - Retourne la position de l'adversaire le plus proche de la balle
    def advClosestBall(self) :
        # Variables de recherche
        advDistance = 1000000
        advID = 0

        # On itère sur les joueurs adverses
        for id in range(PLAYERS_PER_TEAM) :
            dist = self.ball_p.distance(self.player_state(self.his_team, id).position)
            if (dist < advDistance) :
                advDistance = dist
                advID = id

        # On se déplace vers le joueur adverse ciblé
        return self.player_state(self.his_team, advID).position

############################################ CONDITIONS DEFENSIVES ##########################################

# Condition - Defenseur par défaut
class ConditionDefenseur(ProxyObj):
    COEF_DEF = 0.3 
    def __init__(self,state):
        super(ConditionDefenseur,self).__init__(state)
    
    # Status - Est en défense
    def is_defense(self):
        return self.ball_p.distance(self.my_goal)<self.COEF_DEF*self.width

# Action - Defenseur par défaut
def defenseur(I):
    if I.is_defense():
        return I.degage()+I.run(I.ball_p)
    return I.go((I.ball_p-I.my_goal).normalize()*I.width*0.1+I.my_goal)

# Condition - Defenseur Traditionnel
class ConditionTraditionalDefender(ProxyObj) :
    def __init__(self, state, coefDef, coefBall):
        super(ConditionTraditionalDefender,self).__init__(state)
        self.COEF_DEF = coefDef
        self.COEF_BALL = coefBall

    # Status - Est en défense
    def is_defense(self):
        return self.ball_p.distance(self.my_goal)<self.COEF_DEF*self.width

    # Status - Est proche de la balle
    def close_ball(self):
        return self.me.distance(self.ball_p)<self.COEF_BALL*self.width

# Action - Défenseur traditionnel
def tradDefenseur(I) :
    if I.is_defense() :
        if I.close_ball() :
            return I.degage() + I.run(I.ball_p) # On court vers la balle la dégager le plus fort possible
        else :
            return I.go((I.ball_p-I.my_goal).normalize()*I.width*0.1+I.my_goal)
    else :
        return I.run(I.advClosestSelf())

############################################ CONDITIONS MILIEU ##############################################

# Condition - Passeur fou
class ConditionCrazyPass(ProxyObj) :
    def __init__(self, state, coefPass, coefBall, coefGoal) :
        super(ConditionCrazyPass,self).__init__(state)
        self.COEF_PASS = coefPass
        self.COEF_BALL = coefBall
        self.COEF_GOAL = coefGoal

    # Status - Est proche d'un coéquipier
    def close_teammate(self) :
        return self.me.distance(self.findClosestTeammate()) < self.COEF_PASS * self.width

    # Status - Est proche de la balle
    def close_ball(self):
        return self.me.distance(self.ball_p)<self.COEF_BALL*self.width

# Action
def crazyPasser(I) :
    if I.close_ball() :
        if I.can_kick :
            if I.close_teammate() :
                return I.kick(I.findClosestTeammate())
            else :
                if I.close_goal() :
                    return I.degage()
                else :
                    return I.shoot()
        else :
            return I.run(I.ball_p)
    else :
        return I.run(I.ball_p)

            

############################################ CONDITIONS OFFENSIVES ##########################################

# Condition Attaquant par défaut
class ConditionAttaque(ProxyObj):
    COEF_SHOOT = 0.2
    COEF_BALL = 0.1
    def __init__(self,state):
        super(ConditionAttaque,self).__init__(state)
    def close_goal(self):
        return self.me.distance(self.his_goal)<self.COEF_SHOOT*self.width
    def close_ball(self):
        return self.me.distance(self.ball_p)<self.COEF_BALL*self.width

# Action de fonceur par défaut
def fonceur(I) :
    if not I.can_kick :
        if I.close_ball() :
            return I.run(I.ball_p)
        else :
            return I.run(I.ball_p)
    else :
        if I.close_goal() :
            return I.shoot()
    return I.degage()


