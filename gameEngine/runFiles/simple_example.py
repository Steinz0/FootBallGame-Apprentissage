from soccersimulator import SoccerTeam, Simulation, show_simu
from profAI import RandomStrategy,FonceurStrategy,FonceurTestStrategy,DefenseurStrategy,get_team
from profAI import strategies as st
from celery import Celery
import random as random

# Last hit Class
class LastHit() :
    def __init__(self) :
        self.LH = (0,0)
    def update(self, key) :
        self.LH = key
    def reset(self) :
        self.LH = (0,0)

# celery_app = Celery('tasks', backend='amqp://guest:guest@rabbit:5672', broker='amqp://guest:guest@rabbit:5672')

# celery_app.conf.update(
#     CELERY_ROUTES = {"create_match": {"queue": "create_match"}},
# )


# @celery_app.task
# def create_match(max_steps=500):
#     print("IN CREATION")
#     ## Creation d'une equipe
#     pyteam = get_team(1)
#     thon = SoccerTeam(name="ThonTeam")
#     thon.add("PyPlayer",FonceurStrategy()) #Strategie qui fonce
#     thon.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

#     thon2 = SoccerTeam(name="ThonTeam2")
#     thon2.add("PyPlayer",st.CrazyPassStrategy(0.5, 0.5, 0.2)) #Strategie qui ne fait rien
#     thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

#     filename = str(random.random()*100000000)
#     #Creation d'une partie
#     simu = Simulation(thon2, thon, max_steps=max_steps, savefile=True, filename=filename)
#     #Jouer et afficher la partie
#     simu.start()

#     return filename

# create_match()
# Match test pour les strategies
max_steps=1000
lh = LastHit()

# Création Equipe 1
thon = SoccerTeam(name="Red Team")
thon.add("PyPlayer",st.DefenseurStrategy(lh)) #Strategie qui ne fait rien
thon.add("PyPlayer",st.DefenseurStrategy(lh)) #Strategie qui ne fait rien
thon.add("PyPlayer",st.ForwardStrategy(lh)) #Strategie qui fonce
thon.add("PyPlayer",st.ForwardStrategy(lh)) #Strategie qui fonce


# Création Equipe 2
thon2 = SoccerTeam(name="Blue Team")
thon2.add("PyPlayer",st.DefenseurStrategy(lh)) #Strategie qui ne fait rien
thon2.add("PyPlayer",st.DefenseurStrategy(lh)) #Strategie qui ne fait rien
thon2.add("PyPlayer",st.ForwardStrategy(lh)) #Strategie qui fonce
thon2.add("PyPlayer",st.ForwardStrategy(lh)) #Strategie qui ne fait rien

#Creation d'une partie
simu = Simulation(thon, thon2, max_steps=max_steps, lasthit=lh)
#Jouer et afficher la partie
simu.start()
show_simu(simu)