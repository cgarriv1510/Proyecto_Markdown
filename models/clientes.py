class Cliente:
    def __init__(self, nombre, email, activo=True, pedidos=0, password=None):
        self.nombre = nombre
        self.email = email
        self.activo = activo
        self.pedidos = pedidos
        self.password = password  # Añadido campo contraseña
        self._id = None

    @classmethod
    def from_dict(cls, data):
        cliente = cls(
            nombre=data.get("nombre"),
            email=data.get("email"),
            activo=data.get("activo", True),
            pedidos=data.get("pedidos", 0),
            password=data.get("password")  # Incluye password
        )
        cliente._id = str(data.get("_id"))
        return cliente

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "email": self.email,
            "activo": self.activo,
            "pedidos": self.pedidos,
            "password": self.password  # Asegura que la password se guarde
        }
