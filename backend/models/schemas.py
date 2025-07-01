from sqlalchemy import Column, Float, Date
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