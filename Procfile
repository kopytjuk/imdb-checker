celery: celery -A celery_tasks worker --loglevel=INFO --without-heartbeat --without-gossip --without-mingle
web: uvicorn app:app --log-level info --host=0.0.0.0 --port=${PORT:-5000}
