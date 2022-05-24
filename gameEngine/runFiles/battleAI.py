from soccersimulator import SoccerTeam, Simulation, SoccerTournament
from profAI import strategies as st
import sys
sys.path.append('../..')
from extractData.fileExtract import get_features_y

# Last hit Class (permet de savoir qui a tapé la balle en dernier)
class LastHit():
    def __init__(self) :
        self.LH = (0,0)
    def update(self, key) :
        self.LH = key
    def reset(self) :
        self.LH = (0,0)
    

def tournoi():

    list_scores = []
    nbtournoi = 5
    #Pour creer un tournoi d equipes a 2 joueurs, de duree 2000, avec match retour

    features, y = get_features_y(filename='../../extractData/order.txt')

    lh = LastHit()

    knn3 = st.KNNStrategy(features, y, 3, 'auto', 'distance', lh)
    knn3.fit_model()
    print("Fit KNN3 Finish")
    knn5 = st.KNNStrategy(features, y, 5, 'auto', 'distance', lh)
    knn5.fit_model()
    print("Fit KNN5 Finish")
    knn10 = st.KNNStrategy(features, y, 10, 'auto', 'distance', lh)
    knn10.fit_model()
    print("Fit KNN10 Finish")
    svm = st.SVMStrategy(features, y, lh, C=1, kernel='linear')
    svm.fit_model()
    print("Fit SVM Finish")
    randomForest = st.ForestClassifierStrategy('randomForest', features, y, lh, max_depth=6, criterion='entropy', class_weight='balanced')
    randomForest.fit_model()
    print("Fit RandomForest Finish")
    boosting = st.BoostingClassifier(features, y, lh, max_depth=2, loss='deviance', n_estimators=50)
    boosting.fit_model()
    print("Fit Boosting Finish")

    for i in range(nbtournoi):
        tournoi = SoccerTournament(nb_players=4, max_steps=2000,retour=True)

        teamKNN3 = SoccerTeam(name="Team KNN 3")
        teamKNN3.add("PyPlayer",knn3) 
        teamKNN3.add("PyPlayer",knn3)
        teamKNN3.add("PyPlayer",knn3)
        teamKNN3.add("PyPlayer",knn3)

        teamKNN5 = SoccerTeam(name="Team KNN 5")
        teamKNN5.add("PyPlayer",knn5) 
        teamKNN5.add("PyPlayer",knn5)
        teamKNN5.add("PyPlayer",knn5)
        teamKNN5.add("PyPlayer",knn5)

        teamKNN10 = SoccerTeam(name="Team KNN 10")
        teamKNN10.add("PyPlayer",knn10) 
        teamKNN10.add("PyPlayer",knn10)
        teamKNN10.add("PyPlayer",knn10)
        teamKNN10.add("PyPlayer",knn10)

        teamSVM = SoccerTeam(name="Team SVM")
        teamSVM.add("PyPlayer",svm) 
        teamSVM.add("PyPlayer",svm)
        teamSVM.add("PyPlayer",svm)
        teamSVM.add("PyPlayer",svm)

        teamRandomForest = SoccerTeam(name="Team RandomForest")
        teamRandomForest.add("PyPlayer",randomForest) 
        teamRandomForest.add("PyPlayer",randomForest)
        teamRandomForest.add("PyPlayer",randomForest)
        teamRandomForest.add("PyPlayer",randomForest)

        teamBoosting = SoccerTeam(name="Team Boosting")
        teamBoosting.add("PyPlayer",boosting) 
        teamBoosting.add("PyPlayer",boosting)
        teamBoosting.add("PyPlayer",boosting)
        teamBoosting.add("PyPlayer",boosting)

        #ajouter une equipe
        tournoi.add_team(teamKNN3)
        tournoi.add_team(teamKNN5)
        tournoi.add_team(teamKNN10)
        tournoi.add_team(teamSVM)
        tournoi.add_team(teamRandomForest)
        tournoi.add_team(teamBoosting)
        #Jouer un tournoi (lance tous les matchs a la suite)
        tournoi.play()
        #afficher les scores
        tournoi.format_scores()
        tournoi.print_scores()

        list_scores.append(tournoi.format_scores())
    
    print(list_scores)
tournoi()
