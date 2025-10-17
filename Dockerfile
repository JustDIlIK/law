FROM python:3.12

WORKDIR /law

COPY req.txt .

RUN pip install -r req.txt

COPY . .

CMD alembic upgrade head && \
    gunicorn app.main:app \
        --bind 0.0.0.0:10001 \
        --workers 3 \
        --timeout 300 \
        --worker-class uvicorn.workers.UvicornWorker \
        --forwarded-allow-ips="*"