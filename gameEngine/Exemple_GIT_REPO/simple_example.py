from soccersimulator import SoccerTeam, Simulation, show_simu
from profAI import RandomStrategy,FonceurStrategy,FonceurTestStrategy,DefenseurStrategy,get_team
import pika
import json

# connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
# channel = connection.channel()
# channel.basic_qos(prefetch_count=1)
# channel.queue_declare(queue="tasks")
# channel.queue_declare(queue="results")

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
simu.start()


# def callback(ch, method, properties, body):
#     params = json.loads(body.decode('utf-8'))
#     type = str(params["type"])
#     image = params['image']

#     print("Worker received a new task...")
#     simu.start()

#     # send a message back
#     channel.basic_publish(
#         exchange="", 
#         routing_key="results", 
#         body=json.dumps('FINISH', ensure_ascii=False)
# )


# channel.basic_consume("tasks", callback, auto_ack=True)
# channel.start_consuming()