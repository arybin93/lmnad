import os

broker_url = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost//')
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'rpc://')
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
