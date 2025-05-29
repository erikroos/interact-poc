FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN flask --app app.py db init || true
RUN flask --app app.py db migrate -m "initial"
RUN flask --app app.py db upgrade
RUN python seed.py

ENV PORT=8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]