wsgi_app = "backend.main:app"
bind = "0:8001"
worker_class = "uvicorn.workers.UvicornWorker"
