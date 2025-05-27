from flask import Flask, render_template, request, redirect, flash, session, url_for
from datetime import date
from pymongo import MongoClient
from models.productos import Producto
from models.clientes import Cliente
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "Password"

# Conexión a la base de datos MongoDB
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
def pagina_inicio():
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

@app.route("/productos_nuevo", methods=["POST"])
def nuevo_producto():
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
        flash("Producto existente actualizado con nuevo stock y precio.")
    else:
        try:
            producto = Producto(nombre=nombre, precio=precio, categoria=categoria, stock=stock)
            productos_coleccion.insert_one(producto.to_dict())
            flash("Producto añadido correctamente.")
        except ValueError as e:
            flash(f"Error al crear el producto: {str(e)}")
            return redirect("/productos_nuevo")

    return redirect("/productos")

@app.route("/productos_nuevo", methods=["GET"])
def formulario_nuevo_producto():
    return render_template("añadir_producto.html",
        pagina="productos_nuevo",
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha)

# Tienda pública
@app.route("/tienda", methods=["GET", "POST"])
def tienda_inicio():
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
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        
        # Buscar cliente por email
        cliente = clientes_coleccion.find_one({"email": email})
        if cliente:
            session["cliente_id"] = str(cliente["_id"])
            session["cliente_nombre"] = cliente["nombre"]
            flash(f"Bienvenido, {cliente['nombre']}!")
            return redirect(url_for("pagina_inicio"))
        else:
            flash("Correo no registrado.")
            return redirect("/login")

    return render_template("login.html")
from werkzeug.security import generate_password_hash

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


@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect("/login")


# Página de error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
