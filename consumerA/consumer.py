import celery
from decouple import config

CELERY_BROKER = config('CELERY_BROKER_URL', default='amqp://guest:guest@localhost:5672')
CELERY_BACKEND = config('CELERY_BACKEND_URL', default='amqp://guest:guest@localhost:5672')

app = celery.Celery('consumerA_app',
                    broker=CELERY_BROKER,
                    backend=CELERY_BACKEND,
                    )

data = [1] * 100000000


@app.task(name="consumerA.task")
def add(x, y):
    print(f"Starting A..")
    result = 0
    for i in range(0, 50000000):
        result += i ** 0.33
    print(f"Result = {result}")
    return result
