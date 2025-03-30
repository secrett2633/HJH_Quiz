wsgi_app = "backend.main:app"
bind = "0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
