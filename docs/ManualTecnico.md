# TecnoMarket

**TecnoMarket** Aplicación web hecha con **Flask** y **MongoDB** que permite gestionar una tienda online.  
Los usuarios pueden registrarse, iniciar sesión, ver productos, agregarlos al carrito y realizar pedidos.  
El administrador puede gestionar clientes, productos y pedidos.

---

## Tecnologías utilizadas

- Python 3
- Flask
- MongoDB
- PyMongo
- Jinja2 (para las plantillas HTML)
- Werkzeug (para encriptar contraseñas)

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/usuario/tecknomarket.git
cd tecknomarket
```
## Como crear el entorno virtual:
- python -m venv venv
# Activar:
# Windows: venv\Scripts\activate


## Dependencias necesarias 
- pip install -r requirements.txt
## Como ejecutar
python app.py

# Funcionalidades principales del programa 
- Para el administrador

- Ver lista de clientes y añadir/eliminar clientes.

- Ver lista de productos y añadir/editar productos.

- Ver lista de pedidos y eliminar pedidos.

- Panel de estadísticas de clientes, pedidos y stock.

- Para los usuarios

- Registro y login.

- Navegar por la tienda y filtrar productos por categoría.

- Ver detalle de productos.

- Agregar productos al carrito.

- Realizar pedidos.
# Rutas principales

---
| `/` | GET | Redirige al login. |
| `/dashboard` | GET | Página de inicio del panel de administración. Muestra estadísticas de productos, clientes y pedidos. |

---

# Clases

## C. Cliente
-  La clase **Cliente** representa a un cliente de la tienda.  
Se utiliza para guardar y gestionar los datos de cada cliente en la aplicación.

## C. Pedido
- La clase **Pedido** representa un pedido realizado por un cliente en la tienda.  
Se utiliza para guardar los productos comprados, el cliente que lo realizó, la fecha y el total.

## C. Producto
- La clase **Producto** representa un producto que se vende en la tienda.  
Se utiliza para guardar información como nombre, precio, categoría, stock e imagen del producto.
