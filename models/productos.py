from bson import ObjectId

class Producto:
    def __init__(self, nombre, precio, categoria, stock, _id=None):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not categoria:
            raise ValueError("La categoría no puede estar vacía.")
        
        self.id = _id or ObjectId()
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock

    def actualizar_stock(self, cantidad):
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.stock = nuevo_stock

    def to_dict(self):
        return {
            "_id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "stock": self.stock
        }

    @staticmethod
    def from_dict(diccionario):
        return Producto(
            nombre=diccionario["nombre"],
            precio=diccionario["precio"],
            categoria=diccionario["categoria"],
            stock=diccionario["stock"],
            _id=diccionario["_id"]
        )
    
    def __str__(self):
        return f"Producto({self.nombre}, ${self.precio}, {self.categoria}, stock: {self.stock})"
