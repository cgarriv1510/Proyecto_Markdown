from bson import ObjectId
from datetime import date

class Pedido:
    def __init__(self, cliente_id, productos, fecha=None, _id=None):
        self._id = _id or ObjectId()
        self.cliente_id = ObjectId(cliente_id)
        self.productos = productos  # Lista de dicts con producto_id, cantidad, etc.
        self.fecha = fecha or date.today().isoformat()
        self.total = sum(p["subtotal"] for p in productos)

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
