
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


DATABASE_URL = URL.create(

    drivername='postgresql+psycopg2',

    username='jojo_rabbit_user',
    password='nmmdCrlXXBl5VfVHVxUUskSgp1F8DM6N',
    host='dpg-d7110d4r85hc739fvn50-a.singapore-postgres.render.com',
    port=5432,
    database='jojo_rabbit'
)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
