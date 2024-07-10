# My Flask App

This is a Flask application to interact with the SETU Account Aggregator API.

## Setup

1. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

## API Endpoints

- `POST /consent`: Create a consent request.
- `POST /consent/approve`: Approve a consent request.
- `POST /session`: Create a data session.
- `POST /data`: Fetch data from a session.
