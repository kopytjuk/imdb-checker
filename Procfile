celery: celery -A celery_tasks worker --loglevel=INFO
web: uvicorn app:app --log-level info --host=0.0.0.0 --port=${PORT:-5000}
