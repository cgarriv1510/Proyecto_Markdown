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

## Rutas de Clientes

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/clientes` | GET | Muestra la lista de clientes registrados y estadísticas (clientes activos, cliente top). |
| `/clientes_nuevo` | GET | Muestra el formulario para registrar un nuevo cliente. |
| `/clientes_nuevo` | POST | Recibe los datos del formulario y crea un nuevo cliente en la base de datos. |
| `/eliminar_cliente` | POST | Elimina un cliente según su ID. |

---

## Rutas de Pedidos

| Ruta | Método | Descripción |

| `/pedidos` | GET | Muestra la lista de pedidos realizados, con detalle de productos y total de ingresos. |
| `/pedidos_nuevo` | GET | Muestra el formulario para crear un nuevo pedido. |
| `/pedidos_nuevo` | POST | Crea un nuevo pedido con los datos recibidos del formulario. |
| `/eliminar_pedido` | POST | Elimina un pedido según su ID. |

---

## Rutas de Productos

| Ruta | Método | Descripción |

| `/productos` | GET | Muestra la lista de productos con su stock total. |
| `/producto/<producto_id>` | GET | Muestra el detalle de un producto específico. |
| `/productos_nuevo` | GET | Muestra el formulario para agregar un nuevo producto. |
| `/productos_nuevo` | POST | Recibe los datos del formulario y crea o actualiza un producto en la base de datos. |

---

## Rutas de la tienda pública

| Ruta | Método | Descripción |

| `/tienda` | GET | Muestra la tienda principal con todos los productos. Permite filtrar por categoría. |
| `/tienda/productos` | GET | Muestra todos los productos disponibles en la tienda. |
| `/tienda/producto/<producto_id>` | GET | Muestra el detalle de un producto en la tienda pública. |

---

## Rutas de autenticación

| Ruta | Método | Descripción |

| `/login` | GET | Muestra el formulario de login. |
| `/login` | POST | Valida el correo y contraseña del cliente y crea la sesión. |
| `/registro` | GET | Muestra el formulario de registro de cliente. |
| `/registro` | POST | Recibe los datos del formulario y crea un nuevo cliente con contraseña en la base de datos. |
| `/logout` | GET | Cierra la sesión del cliente. |

---

## Rutas del carrito

| Ruta | Método | Descripción |

| `/carrito` | GET | Muestra los productos agregados al carrito y el total. |
| `/carrito/agregar` | POST | Agrega un producto al carrito de la sesión, controlando el stock disponible. |
| `/carrito/eliminar` | POST | Elimina un producto del carrito. |
| `/realizar_pedido` | POST | Convierte los productos del carrito en un pedido, actualiza el stock y vacía el carrito. |

---

## Rutas de error

| Ruta | Método | Descripción |

| `404` | GET | Página de error cuando la ruta no existe. |
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

# 4. Templates del Cliente

## 4.1. Template base: `base_cliente.html`

**Descripción:**  
Este archivo actúa como **plantilla principal** del lado cliente. Define la estructura general de la interfaz y contiene los bloques que son sobrescritos por los demás templates.  

**Bloques definidos en `base_cliente.html`:**  
- `title`: permite a cada vista personalizar el título de la página.  
- `content`: área principal donde cada template inserta su contenido específico.  

**Uso:**  
Todos los templates de la aplicación cliente extienden de `base_cliente.html`, asegurando una estructura uniforme y facilitando el mantenimiento.  

---

## 4.2. Templates derivados

Cada uno de los templates extiende de `base_cliente.html` y sobrescribe los bloques necesarios:

### 4.2.1. Template: `inicio.html`

**Descripción:**  
Página de **inicio de la tienda online**. Muestra un mensaje de bienvenida, una breve descripción de la tienda y un acceso directo al catálogo de productos.  

**Bloques sobrescritos:**  
- `content`  

**Variables esperadas:**  
- `tienda`: nombre de la tienda.  

**Funciones backend relacionadas:**  
- `tienda_productos`: redirige al catálogo general.  

**Comportamiento:**  
1. Encabezado de bienvenida con el nombre de la tienda.  
2. Descripción introductoria.  
3. Botón de acceso al catálogo de productos.  
4. Imagen ilustrativa de portada.  

---

### 4.2.2. Template: `detalle_producto.html`

**Descripción:**  
Muestra el **detalle de un producto específico** con información como imagen, nombre, precio, categoría y stock. Permite agregarlo al carrito si está disponible.  


**Variables:**  
- `producto`: objeto/diccionario con los atributos:  
  - `id`  
  - `nombre`  
  - `precio`  
  - `categoria`  
  - `stock`  
  - `imagen` (opcional)  

**Funciones backend relacionadas:**  
- `agregar_al_carrito`: añade el producto al carrito.  
- `tienda_productos`: redirige al catálogo.  

**Que hace:**  
1. Muestra imagen o mensaje alternativo.  
2. Despliega datos principales del producto.  
3. Si hay stock, muestra botón **Agregar al Carrito**; si no, indica que está agotado.  
4. Botón para volver al catálogo.  

---

### 4.2.3. Template: `carrito.html`

**Descripción:**  
Muestra el **carrito de compras** del cliente con los productos añadidos, sus cantidades, subtotales y total general. Permite eliminar productos o realizar un pedido.  


**Variables:**  
- `productos`: lista de objetos/diccionarios con los atributos:  
  - `id`  
  - `nombre`  
  - `imagen`  
  - `precio`  
  - `cantidad`  
  - `subtotal`  
- `total`: monto total del carrito.  

**Funciones backend:**  
- `eliminar_del_carrito`: elimina un producto del carrito.  
- `realizar_pedido`: confirma el pedido.  
- `tienda_inicio`: redirige a la tienda cuando el carrito está vacío.  

**Que hace:**  
1. Si hay productos, los lista en tabla con imagen, nombre, precio, cantidad, subtotal y opción de eliminar.  
2. Muestra el total y botón para **Realizar pedido**.  
3. Si el carrito está vacío, muestra mensaje y botón para volver a la tienda.  

---
### 4.2.4. Template: `catalogo.html`

**Descripción:**  
Este template corresponde al **catálogo general de productos** de la tienda. Muestra una lista de todos los productos disponibles, incluyendo imagen, nombre, categoría, precio y stock. Cada producto incluye un botón para ver sus detalles.   

**Variables:**  
- `productos`: lista de objetos/diccionarios con los atributos:  
  - `_id`: identificador único del producto.  
  - `nombre`: nombre del producto.  
  - `categoria`: categoría a la que pertenece.  
  - `precio`: precio unitario.  
  - `stock`: unidades disponibles.  
  - `imagen`: ruta/URL de la imagen.  

**Funciones backend relacionadas:**  
- `tienda_detalle_producto`: recibe el `producto_id` y muestra el detalle de un producto específico.  

**Que hace:**  
1. Muestra un encabezado de *“Catálogo de Productos”*.  
2. Itera sobre la lista de productos con un bucle `for`.  
3. Para cada producto, muestra:  
   - Imagen.  
   - Nombre.  
   - Categoría.  
   - Precio.  
   - Stock disponible.  
4. Incluye un botón para acceder a la vista de detalle de cada producto.  

---
