from flask import Flask, render_template, request, redirect, flash, session, url_for
from datetime import date
from pymongo import MongoClient
from models.clientes import Cliente
from models.productos import Producto
from models.pedidos import Pedido
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "Password"

# Conexión a MongoDB
cliente = MongoClient("mongodb+srv://afercor2806:LCrXK9Mqkj78BJY8@cluster0.t9bfnum.mongodb.net/")
db = cliente["tecknomarket"]
productos_coleccion = db["productos"]
clientes_coleccion = db["clientes"]
pedidos_coleccion = db["pedidos"]

# Datos generales
nombre_admin = "Alejandro Fernandez"
nombre_admin2 = "Oscar Manuel Benito Martin"
tienda = "TecnoMarket"
fecha = date.today()

@app.route("/")
def index():
    return redirect("/login")

@app.route("/dashboard")
def pagina_inicio():
    if "cliente_id" not in session:
        return redirect("/login")

    productos = list(productos_coleccion.find())
    total_stock = sum([p["stock"] for p in productos])

    clientes = [Cliente.from_dict(c) for c in clientes_coleccion.find()]
    clientes_activos = sum(1 for c in clientes if c.activo)
    cliente_top = max(clientes, key=lambda c: c.pedidos) if clientes else None

    pedidos = list(pedidos_coleccion.find())
    ingreso_total = sum(p["total"] for p in pedidos)

    return render_template("dashboard.html",
        nombre_admin=nombre_admin,
        nombre_admin2=nombre_admin2,
        tienda=tienda,
        fecha=fecha,
        pagina="inicio",
        productos=productos,
        total_stock=total_stock,
        clientes=clientes,
        clientes_activos=clientes_activos,
        cliente_top=cliente_top,
        pedidos=pedidos,
        ingreso_total=ingreso_total)

# Clientes
@app.route('/clientes')
def pagina_clientes():
    pagina = "clientes"
    clientes_raw = list(clientes_coleccion.find())
    clientes = []
    for c in clientes_raw:
        cliente_obj = Cliente.from_dict(c)
        cliente_obj._id = str(c["_id"])
        clientes.append(cliente_obj)

    clientes_activos = sum(1 for c in clientes if c.activo)
    cliente_top = max(clientes, key=lambda c: c.pedidos) if clientes else None

    return render_template("lista_usuarios.html",
        pagina=pagina,
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha,
        clientes=clientes,
        clientes_activos=clientes_activos,
        cliente_top=cliente_top)

@app.route("/clientes_nuevo", methods=["POST"])
def nuevo_cliente():
    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    activo_str = request.form.get("activo", "false").lower()
    activo = True if activo_str == "true" else False

    try:
        pedidos = int(request.form.get("pedidos", 0))
    except ValueError:
        flash("El número de pedidos debe ser un número válido.")
        return redirect("/clientes_nuevo")

    if not nombre or not email:
        flash("El nombre y el correo electrónico no pueden estar vacíos.")
        return redirect("/clientes_nuevo")

    # Para este método, no se usa password porque es un registro administrativo

    nuevo = Cliente(nombre=nombre, email=email, activo=activo, pedidos=pedidos)
    clientes_coleccion.insert_one(nuevo.to_dict())
    flash("Cliente registrado correctamente.")
    return redirect("/clientes")

@app.route("/clientes_nuevo", methods=["GET"])
def formulario_nuevo_cliente():
    return render_template("registro_usuario.html",
        pagina="clientes",
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha)

@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    cliente_id = request.form.get("cliente_id")
    if not cliente_id:
        flash("ID de cliente no proporcionado.")
        return redirect("/clientes")

    try:
        result = clientes_coleccion.delete_one({"_id": ObjectId(cliente_id)})
        if result.deleted_count == 1:
            flash("Cliente eliminado correctamente.")
        else:
            flash("No se encontró el cliente.")
    except Exception as e:
        flash(f"Error al eliminar cliente: {str(e)}")

    return redirect("/clientes")

# Pedidos
@app.route('/pedidos')
def pagina_pedidos():
    pagina = "pedidos"
    pedidos = list(pedidos_coleccion.find())
    ingreso_total = sum(p["total"] for p in pedidos)

    return render_template('lista_pedidos.html',
        pagina=pagina,
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha,
        pedidos=pedidos,
        ingreso_total=ingreso_total)

@app.route("/pedidos_nuevo", methods=["GET", "POST"])
def nuevo_pedido():
    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        try:
            total = float(request.form.get("total", 0))
        except ValueError:
            flash("Total inválido.")
            return redirect("/pedidos_nuevo")

        fecha_pedido = request.form.get("fecha", date.today().isoformat())
        nuevo = {"cliente": cliente, "total": total, "fecha": fecha_pedido}
        pedidos_coleccion.insert_one(nuevo)
        flash("Pedido registrado correctamente.")
        return redirect("/pedidos")

    return render_template("registro_pedido.html",
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha,
        pagina="pedidos")

@app.route("/eliminar_pedido", methods=["POST"])
def eliminar_pedido():
    pedido_id = request.form.get("pedido_id")
    if not pedido_id:
        flash("ID de pedido no proporcionado.")
        return redirect("/pedidos")

    try:
        result = pedidos_coleccion.delete_one({"_id": ObjectId(pedido_id)})
        if result.deleted_count == 1:
            flash("Pedido eliminado correctamente.")
        else:
            flash("No se encontró el pedido.")
    except Exception as e:
        flash(f"Error al eliminar pedido: {str(e)}")

    return redirect("/pedidos")

# Productos
@app.route('/productos')
def pagina_productos():
    datos_productos = productos_coleccion.find()
    productos = [Producto.from_dict(p) for p in datos_productos]
    total_stock = sum(producto.stock for producto in productos)

    return render_template('lista_productos.html',
        productos=productos,
        total_stock=total_stock,
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha)

@app.route('/producto/<producto_id>')
def detalle_producto(producto_id):
    producto_data = productos_coleccion.find_one({"_id": ObjectId(producto_id)})
    if not producto_data:
        flash("Producto no encontrado.")
        return redirect("/productos")

    producto = Producto.from_dict(producto_data)
    return render_template("detalle_producto.html",
        producto=producto,
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha)

@app.route("/productos_nuevo", methods=["POST", "GET"])
def nuevo_producto():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "").strip()

        try:
            precio = float(request.form.get("precio", 0))
            stock = int(request.form.get("stock", 0))
        except ValueError:
            flash("Precio y stock deben ser valores numéricos.")
            return redirect("/productos_nuevo")

        if not nombre or not categoria:
            flash("El nombre y la categoría no pueden estar vacíos.")
            return redirect("/productos_nuevo")
        if precio < 0:
            flash("El precio no puede ser negativo.")
            return redirect("/productos_nuevo")
        if stock < 0:
            flash("El stock no puede ser negativo.")
            return redirect("/productos_nuevo")

        producto_existente = productos_coleccion.find_one({
            "nombre": {"$regex": f"^{nombre}$", "$options": "i"},
            "categoria": categoria
        })

        if producto_existente:
            productos_coleccion.update_one(
                {"_id": producto_existente["_id"]},
                {"$set": {"precio": precio, "stock": stock}}
            )
            flash("Producto existente actualizado.")
        else:
            producto = Producto(nombre=nombre, precio=precio, categoria=categoria, stock=stock)
            productos_coleccion.insert_one(producto.to_dict())
            flash("Producto añadido correctamente.")

        return redirect("/productos")

    return render_template("añadir_producto.html",
        pagina="productos_nuevo",
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha)

# Tienda pública
@app.route("/tienda")
def tienda_inicio():
    if "cliente_id" not in session:
        return redirect("/login")

    productos = list(productos_coleccion.find())
    categoria_seleccionada = request.args.get('categoria', None)
    if categoria_seleccionada:
        productos = [producto for producto in productos if producto['categoria'].lower() == categoria_seleccionada.lower()]
    categorias = list(productos_coleccion.distinct("categoria"))

    return render_template("public/inicio.html",
        productos=productos,
        categorias=categorias,
        tienda=tienda,
        fecha=fecha)

@app.route("/tienda/productos")
def tienda_productos():
    productos = list(productos_coleccion.find())
    return render_template("public/productos.html",
        productos=productos,
        tienda=tienda,
        fecha=fecha)

# LOGIN
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        cliente = clientes_coleccion.find_one({"email": email})
        if cliente and "password" in cliente:
            if check_password_hash(cliente["password"], password):
                session["cliente_id"] = str(cliente["_id"])
                session["cliente_nombre"] = cliente["nombre"]
                flash(f"Bienvenido, {cliente['nombre']}!")
                return redirect("/tienda")
            else:
                flash("Contraseña incorrecta.")
                return redirect("/login")
        else:
            flash("Correo no registrado.")
            return redirect("/login")
    return render_template("login.html")

# REGISTRO
@app.route('/registro', methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.")
            return redirect("/registro")

        if clientes_coleccion.find_one({"email": email}):
            flash("Este correo ya está registrado.")
            return redirect("/registro")
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.")
            return redirect("/registro")

        hashed_password = generate_password_hash(password)

        nuevo_cliente = {
            "nombre": nombre,
            "email": email,
            "password": hashed_password,
            "activo": True,
            "pedidos": 0
        }

        clientes_coleccion.insert_one(nuevo_cliente)
        flash("Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect("/login")

    return render_template("registro_cliente.html")

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect("/login")

# ERROR 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



#CARRITO

@app.route("/carrito/agregar", methods=["POST"])
def agregar_al_carrito():
    if "cliente_id" not in session:
        flash("Debes iniciar sesión para agregar productos al carrito.")
        return redirect("/login")

    producto_id = request.form.get("producto_id")
    if not producto_id:
        flash("No se especificó el producto para agregar.")
        return redirect(request.referrer or "/")

    # Verificar que el producto existe y tiene stock
    producto_data = productos_coleccion.find_one({"_id": ObjectId(producto_id)})
    if not producto_data:
        flash("Producto no encontrado.")
        return redirect(request.referrer or "/")

    stock_disponible = producto_data.get("stock", 0)
    if stock_disponible <= 0:
        flash("El producto está agotado.")
        return redirect(request.referrer or "/")

    # Obtener carrito actual de la sesión o crear uno nuevo
    carrito = session.get("carrito", {})

    cantidad_actual = carrito.get(producto_id, 0)

    # Controlar que no se exceda el stock
    if cantidad_actual + 1 > stock_disponible:
        flash(f"No hay suficiente stock para agregar más unidades del producto '{producto_data['nombre']}'.")
        return redirect(request.referrer or "/")

    # Incrementar la cantidad del producto en el carrito
    carrito[producto_id] = cantidad_actual + 1

    session["carrito"] = carrito
    flash(f"Producto '{producto_data['nombre']}' agregado al carrito.")
    return redirect(request.referrer or "/")


@app.route("/tienda/producto/<producto_id>")
def tienda_detalle_producto(producto_id):
    producto_data = productos_coleccion.find_one({"_id": ObjectId(producto_id)})
    if not producto_data:
        flash("Producto no encontrado.")
        return redirect("/tienda/productos")

    producto = Producto.from_dict(producto_data)
    producto.id = str(producto_data["_id"])  # Para usar en formularios

    return render_template("public/detalle_producto.html",
        producto=producto,
        tienda=tienda,
        fecha=fecha)


    
@app.route("/carrito")
def mostrar_carrito():
    if "cliente_id" not in session:
        flash("Debes iniciar sesión para ver el carrito.")
        return redirect("/login")

    carrito = session.get("carrito", {})
    productos_carrito = []
    total = 0.0

    for producto_id, cantidad in carrito.items():
        producto_data = productos_coleccion.find_one({"_id": ObjectId(producto_id)})
        if producto_data:
            subtotal = producto_data["precio"] * cantidad
            total += subtotal
            productos_carrito.append({
                "id": str(producto_data["_id"]),
                "nombre": producto_data["nombre"],
                "precio": producto_data["precio"],
                "cantidad": cantidad,
                "subtotal": subtotal
            })

    return render_template("carrito.html",
                           productos=productos_carrito,
                           total=total,
                           nombre_admin=nombre_admin,
                           tienda=tienda,
                           fecha=fecha)
if __name__ == '__main__':
    app.run(debug=True)


