from soccersimulator import SoccerTeam, Simulation, show_simu
from profAI import RandomStrategy,FonceurStrategy,FonceurTestStrategy,DefenseurStrategy,get_team


## Creation d'une equipe
pyteam = get_team(1)
thon = SoccerTeam(name="ThonTeam")
thon.add("PyPlayer",FonceurStrategy()) #Strategie qui ne fait rien
thon.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

thon2 = SoccerTeam(name="ThonTeam2")
thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien
thon2.add("PyPlayer",RandomStrategy()) #Strategie qui ne fait rien

#Creation d'une partie
simu = Simulation(thon2,thon)
#Jouer et afficher la partie
simu.reset()
simu.start()
