from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlalchemy_database_URL = 'mysql+pymysql://BigBoss:letmein1@127.0.0.1:3306/todos'
#sqlalchemy_database_URL = 'postgresql://postgres:letmein1@localhost/TodosApplicationDatbase'

engine = create_engine(sqlalchemy_database_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()