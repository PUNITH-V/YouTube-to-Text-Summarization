import multiprocessing
multiprocessing.set_start_method("fork", force=True)  # Fix for Mac multiprocessing

import uvicorn
from app import flask_app  # Import Flask app
import app.main  # Ensure Flask routes are loaded
from app.fastapi_app import app as fastapi_app

# Function to run FastAPI
def run_fastapi():
    uvicorn.run("app.fastapi_app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == '__main__':
    # Start FastAPI in a separate process
    p = multiprocessing.Process(target=run_fastapi)
    p.start()

    # Run Flask app
    flask_app.run(debug=True, use_reloader=False, port=5000)
