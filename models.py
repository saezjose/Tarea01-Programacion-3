#Modelos SQLAlchemy#
# models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    experiencia = Column(Integer, default=0)

    misiones = relationship("Mision", back_populates="personaje")

class Mision(Base):
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    personaje_id = Column(Integer, ForeignKey("personajes.id"))

    personaje = relationship("Personaje", back_populates="misiones")
