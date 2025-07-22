<<<<<<< HEAD
# Price Comparison API Backend

## Prerequisites
- Python 3.12
- PostgreSQL (or your preferred SQL database)

## Setup

1. **Clone the repository**

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On Mac/Linux:
  ```bash
  source venv/bin/activate
  ```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure your database**
- Copy `.env.example` to `.env` and set your database URL (see below).

6. **Run database migrations**
```bash
alembic upgrade head
```

7. **Start the API server**
```bash
uvicorn app.main:app --reload
```

8. **Open your browser to** [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.

---

## Environment Variables
Create a `.env` file in the root directory with:
```
DATABASE_URL=postgresql://user:password@localhost:5432/yourdb
```

---

## How to Use
- **/docs**: Interactive API documentation (Swagger UI)
- **/redoc**: Alternative API docs

Your coworker can POST scraped data to the API endpoints (see /docs for details).

---

## Project Structure
- `app/main.py`: FastAPI app entrypoint
- `app/db/`: Database models and session
- `app/api/endpoints/`: API route definitions
- `app/schemas/`: Pydantic schemas for request/response
- `alembic/`: Database migrations

---

## Need Help?
Just run the server and visit `/docs` for a full, interactive guide to all endpoints!
=======
# railways
>>>>>>> 040a9da9f7bcb0aead0faeafb754baea9352f0cc
