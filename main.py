#FastAPI App#
# main.py

from fastapi import FastAPI, HTTPException
from misiones import crear_personaje, asignar_mision, completar_mision, ver_misiones
from Exceptions import PersonajeNoEncontrado, MisionNoDisponible
from models import Base
from database import engine

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API RPG - Misiones")

@app.post("/personajes/")
def crear_nuevo_personaje(nombre: str):
    personaje = crear_personaje(nombre)
    return {"id": personaje.id, "nombre": personaje.nombre, "experiencia": personaje.experiencia}

@app.post("/misiones/")
def agregar_mision(personaje_id: int, descripcion: str):
    try:
        mision = asignar_mision(personaje_id, descripcion)
        return {"mensaje": "Misión asignada", "descripcion": mision.descripcion}
    except PersonajeNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/misiones/completar/")
def terminar_mision(personaje_id: int):
    try:
        resultado = completar_mision(personaje_id)
        return resultado
    except PersonajeNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MisionNoDisponible as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/misiones/")
def obtener_misiones(personaje_id: int):
    return {"misiones_pendientes": ver_misiones(personaje_id)}
