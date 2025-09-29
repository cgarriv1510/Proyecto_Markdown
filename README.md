# Proyecto Markdown - Tienda Online

Este proyecto es una aplicacion web para la gestion y visualizacion de productos en una tienda online. Permite registrar clientes, gestionar pedidos y productos, y realizar compras desde una interfaz intuitiva.

# Caracteristicas principales

- Registro y autenticación de clientes.
- Gestion de productos (alta, baja, modificacion).
- Carrito de compras y pedidos.
- Panel de administracion para visualizar pedidos y usuarios.
- Interfaz responsive.

# Estructura del proyecto
```bash
-------------------------------------------------------------------------------------------------------------------------------------------
Proyecto_Markdown/
├── .idea/                 # Configuración de IDE (IntelliJ/PyCharm)
│   ├── Proyecto_Final.iml
│   ├── modules.xml
│   ├── vcs.xml
│   └── inspectionProfiles/
│       └── profiles_settings.xml
│
├── app.py                 # Archivo principal de la aplicación
│
├── docs/                  # Documentación
│   ├── ManualDelUsuario.md
│   └── ManualTecnico.md
│
├── models/                # Modelos de datos
│   ├── clientes.py
│   ├── pedidos.py
│   └── productos.py
│
├── plan_entorno_cliente.md
├── productos.json         # Datos de productos
├── README.md              # Documentación principal
├── requirements.txt       # Dependencias del proyecto
│
├── static/                # Archivos estáticos (CSS e imágenes)
│   ├── client.css
│   ├── login.css
│   ├── styles.css
│   └── images/
│       ├── bicicleta_montaña.jpeg
│       ├── cafetera_nespresso.jpg
│       ├── guitarra_acustica.jpg
│       ├── iphone_14.jpg
│       ├── lego_halcon.jpg
│       ├── libro_ahora.png
│       ├── libro_sapiens.jpg
│       ├── mackbook.jpg
│       ├── mesa_comedor.jpg
│       ├── muñeca_barbie.jpg
│       ├── robot_aspirador.jpg
│       ├── zapatillas_nike.jpg
│       └── ...
│
├── templates/             # Vistas HTML
│   ├── 404.html
│   ├── añadir_producto.html
│   ├── base.html
│   ├── base_cliente.html
│   ├── dashboard.html
│   ├── detalle_producto.html
│   ├── lista_pedidos.html
│   ├── lista_productos.html
│   ├── lista_usuarios.html
│   ├── login.html
│   ├── registro.html
│   ├── registro_cliente.html
│   └── public/
│       ├── carrito.html
│       ├── detalle_producto.html
│       ├── inicio.html
│       └── productos.html
-------------------------------------------------------------------------------------------------------------------------------------------
