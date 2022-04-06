from tabnanny import verbose
from soccersimulator import SoccerTeam, Simulation, show_simu
from profAI import RandomStrategy,FonceurStrategy,FonceurTestStrategy,DefenseurStrategy,get_team
from celery import Celery
import random as random

celery_app = Celery('tasks', backend='amqp://localhost:5672', broker='amqp://localhost:5672')

celery_app.conf.update(
    CELERY_ROUTES = {"create_match": {"queue": "create_match"}},
)

@celery_app.task
def create_match(max_steps=500):
    ## Creation d'une equipe
    pyteam = get_team(1)
    thon = SoccerTeam(name="ThonTeam")
    thon.add("PyPlayer",FonceurStrategy()) #Strategie qui fonce
    thon.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

    thon2 = SoccerTeam(name="ThonTeam2")
    thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien
    thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

    filename = str(random.random()*100000000)
    #Creation d'une partie
    simu = Simulation(thon2, thon, max_steps=max_steps, savefile=True, filename=filename)
    #Jouer et afficher la partie
    simu.start()

    return filename

# Match test pour les strategies
max_steps=1000
thon = SoccerTeam(name="ThonTeam")
thon.add("PyPlayer",FonceurStrategy()) #Strategie qui fonce
thon.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

for p in thon.players :
    print(p)

thon2 = SoccerTeam(name="ThonTeam2")
thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien
thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

#Creation d'une partie
simu = Simulation(thon,thon2,max_steps=max_steps)
#Jouer et afficher la partie
simu.start()
show_simu(simu)