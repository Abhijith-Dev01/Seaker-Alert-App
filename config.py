from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database_url = 'postgresql+psycopg2://postgres:postgres@db:5432/system_monitoring'
Database_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/system_monitoring'

engine = create_engine(Database_url)
sessionLocal = sessionmaker(autoflush=True,autocommit=False,bind=engine)
Base = declarative_base()
