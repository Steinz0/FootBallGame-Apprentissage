from soccersimulator import SoccerTeam, Simulation, show_simu
from profAI import RandomStrategy,FonceurStrategy,FonceurTestStrategy,DefenseurStrategy,get_team
from worker import celery_app

@celery_app.task
def print_hello():
    return "hello"

@celery_app.task
def create_match():
    ## Creation d'une equipe
    pyteam = get_team(1)
    thon = SoccerTeam(name="ThonTeam")
    thon.add("PyPlayer",FonceurStrategy()) #Strategie qui fonce
    thon.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

    thon2 = SoccerTeam(name="ThonTeam2")
    thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien
    thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien


    #Creation d'une partie
    simu = Simulation(thon2,thon)
    #Jouer et afficher la partie
    simu.start()