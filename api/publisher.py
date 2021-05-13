from flask import Flask, flash, abort, render_template
import celery
import random
from celery import signature
from decouple import config

CELERY_BROKER = config('CELERY_BROKER_URL', default='amqp://guest:guest@localhost:5672')
CELERY_BACKEND = config('CELERY_BACKEND_URL', default='amqp://guest:guest@localhost:5672')

celery_app = celery.Celery('publisher',
                           broker=CELERY_BROKER,
                           backend=CELERY_BACKEND)

flask_app = Flask(__name__)
flask_app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)
consumers = {"consumerA": {"task": "consumerA.task",
                           "queue": "consumer.A"},
             "consumerB": {"task": "consumerB.task",
                           "queue": "consumer.B"}
             }


@flask_app.route('/consumer/list', methods=['GET'])
def list_consumers():
    return consumers


@flask_app.route('/consumer/<consumer_name>/publish/<number_of_tasks>/', methods=['GET', 'POST'])
def publish_task(consumer_name, number_of_tasks=1):
    consumer = consumers.get(consumer_name, None)
    if not consumer:
        return abort(404)

    try:
        tasks_ids = []
        for i in range(int(number_of_tasks)):
            task = celery_app.send_task(consumer['task'],
                                        args=[random.randint(0, 100), random.randint(0, 100)],
                                        queue=consumer['queue'])
            tasks_ids.append(task.id)
    except Exception as e:
        return {"status": "error", "message": f"Could not send task do broker. Got error {e}"}
    return {"status": "success", "message": f"Sent tasks", "tasks_ids": tasks_ids}


if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=8001)
