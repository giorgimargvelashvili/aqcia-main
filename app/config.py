import os

# Use PostgreSQL by default
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:password@localhost:5432/shopdb')
# In production, set the DATABASE_URL environment variable to your Render Postgres connection string
