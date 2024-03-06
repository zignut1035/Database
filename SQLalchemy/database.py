from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///carDatabase.db", echo = False, future = True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

#Model for a car
class Car(Base):
    __tablename__ = "cars"
    carId = Column(Integer, primary_key = True, autoincrement = True)
    manufacturer = Column(String, nullable = False)
    model = Column(String, nullable = False)
    invoices = relationship("Invoice", back_populates="cars")
#Model for a car invoice
class Invoice(Base):
    __tablename__ = "invoices"
    InvoiceId = Column(Integer, primary_key = True, autoincrement = True)
    carId = Column(Integer, ForeignKey("cars.carId"))
    description = Column(String, nullable = True)
    amount = Column(Float, nullable = False)
    cars = relationship("Car", back_populates = "invoices")

Base.metadata.create_all(engine)

#Create session to interact with the database
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)

