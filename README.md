# interact-poc
POC for an interactive seminar app

## Steps for local deployment

1. Setup a virtual environment
1. Activate virtual environment
1. Install required packages: ``pip install -r requirements.txt``
1. Copy example.config.json to config.json and set a suitable SECRET_KEY
1. Generate database:
    1. ``flask --app app.py db init``
    1. ``flask --app app.py db migrate``
    1. ``flask --app app.py db upgrade``
1. Seed the database: `python seed.py`
1. Run the app: ``python app.py``

## Steps for GCP build an deployment

1. (only once) ``gcloud auth login``
1. (only once) ``gcloud config set project flask-on-gcp-419112``
1. (only once) ``gcloud services enable run.googleapis.com``
1. ``gcloud builds submit --tag gcr.io/flask-on-gcp-419112/flask-app``
1. ``gcloud run deploy flask-app --image gcr.io/flask-on-gcp-419112/flask-app --platform managed --region europe-west1 --allow-unauthenticated``
