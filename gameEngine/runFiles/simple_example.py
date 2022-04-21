from soccersimulator import SoccerTeam, Simulation#, show_simu
from profAI import RandomStrategy,FonceurStrategy,FonceurTestStrategy,DefenseurStrategy,get_team
from profAI import strategies as st
from celery import Celery
import random as random

# Last hit Class (permet de savoir qui a tapé la balle en dernier)
class LastHit() :
    def __init__(self) :
        self.LH = (0,0)
    def update(self, key) :
        self.LH = key
    def reset(self) :
        self.LH = (0,0)
    
celery_app = Celery('tasks', backend='amqp://guest:guest@rabbit:5672', broker='amqp://guest:guest@rabbit:5672')

celery_app.conf.update(
    CELERY_ROUTES = {"create_match": {"queue": "create_match"}},
)



@celery_app.task
def create_match(max_steps=2000):
    # Affichage d'initialisation
    print("IN CREATION")

    # Création de la variable Last Hit
    lh = LastHit()

    start = [st.ForwardStrategy(lh), st.DefenseurStrategy(lh)]
    # Création de l'équipe 1
    pyteam = get_team(1)
    thon = SoccerTeam(name="Team 1")
    thon.add("PyPlayer",start[random.randint(0,1)]) 
    thon.add("PyPlayer",start[random.randint(0,1)])
    thon.add("PyPlayer",start[random.randint(0,1)])
    thon.add("PyPlayer",start[random.randint(0,1)])

    # Création de l'équipe 2
    thon2 = SoccerTeam(name="Team 2")
    thon2.add("PyPlayer",start[random.randint(0,1)]) 
    thon2.add("PyPlayer",start[random.randint(0,1)]) 
    thon2.add("PyPlayer",start[random.randint(0,1)]) 
    thon2.add("PyPlayer",start[random.randint(0,1)]) 

    # Création du nom du fichier
    filename = str(random.random()*100000000)

    #Creation d'une partie
    simu = Simulation(thon2, thon, max_steps=max_steps, savefile=True, filename=filename, lasthit=lh)

    #Jouer et afficher la partie
    simu.start()
    # On retourne le nom du fichier correspondant au match venant d'être simulé
    return filename

# create_match()
# Match test pour les strategies
# max_steps=1000

# lh = LastHit()

# start = [st.ForwardStrategy(lh), st.DefenseurStrategy(lh)]
# # Création de l'équipe 1
# pyteam = get_team(1)
# thon = SoccerTeam(name="Team 1")
# thon.add("PyPlayer",start[random.randint(0,1)]) 
# thon.add("PyPlayer",start[random.randint(0,1)])
# thon.add("PyPlayer",start[random.randint(0,1)])
# thon.add("PyPlayer",start[random.randint(0,1)])

# # Création de l'équipe 2
# thon2 = SoccerTeam(name="Team 2")
# thon2.add("PyPlayer",start[random.randint(0,1)]) 
# thon2.add("PyPlayer",start[random.randint(0,1)]) 
# thon2.add("PyPlayer",start[random.randint(0,1)]) 
# thon2.add("PyPlayer",start[random.randint(0,1)]) 

# #Creation d'une partie
# simu = Simulation(thon,thon2,max_steps=max_steps, lasthit=lh)
# #Jouer et afficher la partie
# simu.start()
# show_simu(simu)
