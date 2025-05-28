from bson import ObjectId

class Producto:
    def __init__(self, nombre, precio, categoria, stock, imagen, _id=None):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not categoria:
            raise ValueError("La categoría no puede estar vacía.")
        
        # Convierte el _id a ObjectId si es string, o genera uno nuevo
        if _id is None:
            self.id = ObjectId()
        elif isinstance(_id, ObjectId):
            self.id = _id
        elif isinstance(_id, str):
            self.id = ObjectId(_id)
        else:
            raise TypeError("El _id debe ser None, str o ObjectId")
        
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.imagen = imagen

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
            "stock": self.stock,
            "imagen": self.imagen
        }

    @staticmethod
    def from_dict(diccionario):
        _id = diccionario.get("_id")
        if _id and isinstance(_id, str):
            _id = ObjectId(_id)
        return Producto(
            nombre=diccionario["nombre"],
            precio=diccionario["precio"],
            categoria=diccionario["categoria"],
            stock=diccionario["stock"],
            imagen=diccionario["imagen"],
            _id=_id
        )
    
    def __str__(self):
        return f"Producto({self.nombre}, ${self.precio}, {self.categoria}, stock: {self.stock})"
