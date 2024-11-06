from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use your PostgreSQL database URL provided by Render
SQLALCHEMY_DATABASE_URL = "postgresql://blog_app_twbj_user:fjofJHz8MHCdOZ9a2u6730cwsPrSKu2H@dpg-cslh203tq21c73eiigv0-a/blog_app_twbj"

# Create the engine without connect_args since it's no longer needed for PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
