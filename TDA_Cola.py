# TDA_Cola.py

class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.items.pop(0)

    def esta_vacia(self):
        return len(self.items) == 0

    def ver_primero(self):
        if self.esta_vacia():
            return None
        return self.items[0]

    def __len__(self):
        return len(self.items)

    def obtener_todos(self):
        return self.items.copy()
