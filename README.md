please check requirements.txt file

Running the Application & Tests
To run unit tests:
pytest tests/
To launch the FastAPI application:
uvicorn app.main:app --reload
The application is implemented as a REST API. Once running, visit Swagger documentation at:
http://127.0.0.1:8000/docs




