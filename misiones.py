# misiones.py

from models import Personaje, Mision
from database import SessionLocal
from Exceptions import PersonajeNoEncontrado, MisionNoDisponible
from TDA_Cola import Cola

# Diccionario que guarda las colas de misiones por personaje
colas_misiones = {}

def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crear_personaje(nombre):
    db = SessionLocal()
    personaje = Personaje(nombre=nombre)
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    colas_misiones[personaje.id] = Cola()
    db.close()
    return personaje

def asignar_mision(personaje_id, descripcion):
    db = SessionLocal()
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if not personaje:
        raise PersonajeNoEncontrado("Personaje no encontrado")

    nueva_mision = Mision(descripcion=descripcion, personaje_id=personaje.id)
    db.add(nueva_mision)
    db.commit()
    db.refresh(nueva_mision)

    # Asegurarse de que el personaje tenga una cola
    if personaje_id not in colas_misiones:
        colas_misiones[personaje_id] = Cola()
    colas_misiones[personaje_id].encolar(nueva_mision)

    db.close()
    return nueva_mision

def completar_mision(personaje_id):
    db = SessionLocal()
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if not personaje:
        raise PersonajeNoEncontrado("Personaje no encontrado")

    cola = colas_misiones.get(personaje_id)
    if not cola or cola.esta_vacia():
        raise MisionNoDisponible("No hay misiones para completar")

    mision = cola.desencolar()

    # Simular recompensa
    personaje.experiencia += 50
    db.delete(mision)
    db.commit()
    db.refresh(personaje)
    db.close()
    return {"mensaje": "Misión completada", "xp_total": personaje.experiencia}

def ver_misiones(personaje_id):
    cola = colas_misiones.get(personaje_id)
    if not cola:
        return []
    return [m.descripcion for m in cola.obtener_todos()]
