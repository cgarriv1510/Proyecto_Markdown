from bson import ObjectId
from datetime import date

class Pedido:
    def __init__(self, cliente_id, productos, fecha=None, _id=None):
    
        self._id = _id or ObjectId()
        self.cliente_id = ObjectId(cliente_id)
        self.fecha = fecha or date.today().isoformat()

        self.productos = []
        self.total = 0

        for p in productos:
            producto_id = ObjectId(p["producto_id"])
            cantidad = int(p["cantidad"])
            precio = float(p["precio"])
            subtotal = round(precio * cantidad, 2)
            self.productos.append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": subtotal
            })
            self.total += subtotal

        self.total = round(self.total, 2)

    def to_dict(self):
        return {
            "_id": self._id,
            "cliente_id": self.cliente_id,
            "fecha": self.fecha,
            "productos": self.productos,
            "total": self.total
        }

    @staticmethod
    def from_dict(data):
        return Pedido(
            cliente_id=data["cliente_id"],
            productos=data["productos"],
            fecha=data.get("fecha"),
            _id=data.get("_id")
        )
