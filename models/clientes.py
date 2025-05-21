class Cliente:
    #Por defecto estará activo y sus pedidos serán 0
    def __init__(self, nombre, email, activo=True, pedidos=0):
        self.nombre = nombre
        self.email = email
        self.activo = activo
        self.pedidos = pedidos


    #Convertir los datos del cliente en un diccionario
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "email": self.email,
            "activo": self.activo,
            "pedidos": self.pedidos
        }


    #Convertir Diccionario con los datos a Objeto 
    @classmethod
    def from_dict(cls, data):
        return cls(
            nombre=data.get("nombre"),
            email=data.get("email"),
            activo=data.get("activo", True),
            pedidos=data.get("pedidos", 0)
        )
