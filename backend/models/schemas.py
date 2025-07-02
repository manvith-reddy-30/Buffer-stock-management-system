from sqlalchemy import Column, Float, Date,Integer,String
from sqlalchemy.orm import relationship
from config.database import Base

class Hyderabad(Base):

    __tablename__ = 'hyderabad'

    date = Column(Date,primary_key=True,index=True)
    price = Column(Float, nullable=False)

class Medak(Base):
    __tablename__ = 'medak'
    date = Column(Date, primary_key=True, index=True)
    price = Column(Float, nullable=False)

class Warangal(Base):
    __tablename__ = 'warangal'
    date = Column(Date, primary_key=True, index=True)
    price = Column(Float, nullable=False)

class RangaReddy(Base):
    __tablename__ = 'rangareddy'
    date = Column(Date, primary_key=True, index=True)
    price = Column(Float, nullable=False)

class Nalgonda(Base):
    __tablename__ = 'nalgonda'
    date = Column(Date, primary_key=True, index=True)
    price = Column(Float, nullable=False)

class User(Base):
    __tablename__ = 'user_table'

    govt_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)

class BufferClass(Base):

    __tablename__ = 'buffer_table'

    place = Column(String,primary_key=True, nullable=False)
    user_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    last_modified_date = Column(Date,primary_key=True,index=True)

    
