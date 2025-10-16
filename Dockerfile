FROM python:3.12

WORKDIR /law

COPY req.txt .

RUN pip install -r req.txt

COPY . .

CMD alembic upgrade head && gunicorn app.main:app --timeout 300 --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:10001 --forwarded-allow-ips='*'
