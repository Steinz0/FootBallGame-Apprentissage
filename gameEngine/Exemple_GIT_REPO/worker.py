from celery import Celery

celery_app = Celery(
    main="football_tasks",
    broker="amqp://",
    backend="amqp://",
    include= [
        "Exemple_GIT_REPO.simple_example"
    ]
)

celery_app.conf.task_routes = {"Exemple_GIT_REPO.*" : {"queue": "match_tasks"}}

if __name__ == "__main__":
    celery_app.start()