from .celery import app
from .services import get_everyday_statistics


@app.task
def send_email():
    get_everyday_statistics()

