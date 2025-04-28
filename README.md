# interact-poc
POC for an interactive seminar app

## steps

1. Setup a virtual environment
1. Activate virtual environment
1. Install required packages: ``pip install -r requirements.txt``
1. Generate database:
    1. ``flask --app app.py db init``
    1. ``flask --app app.py db migrate``
    1. ``flask --app app.py db upgrade``
1. Seed the database: `python seed.py`
1. Run the app: ``python app.py``
