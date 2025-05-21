from flask import Flask, render_template, request, redirect, flash
from datetime import date
from pymongo import MongoClient
from models.productos import Producto
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key= "Password" #Es necesario para usar flash

#Conexion a la BBDD
cliente = MongoClient("mongodb+srv://afercor2806:LCrXK9Mqkj78BJY8@cluster0.t9bfnum.mongodb.net/")
db = cliente["tecknomarket"]
productos_coleccion = db["productos"]





# Datos generales
nombre_admin = "Alejandro Fernandez"
nombre_admin2 = "Oscar Manuel Benito Martin"
tienda = "TecnoMarket"
fecha = date.today()

clientes = [
        {"nombre": "Ana Torres", "email": "ana@mail.com", "activo": True, "pedidos": 4},
        {"nombre": "Luis Pérez", "email": "luis@mail.com", "activo": False, "pedidos": 1},
        {"nombre": "Marta García", "email": "marta@mail.com", "activo": True, "pedidos": 7},
        {"nombre": "Carlos Ruiz", "email": "carlos@mail.com", "activo": False, "pedidos": 0}
    ]

pedidos = [
        {"cliente": "Ana Torres", "total": 1500.0, "fecha": "2025-05-01"},
        {"cliente": "Marta García", "total": 240.0, "fecha": "2025-05-03"},
        {"cliente": "Luis Pérez", "total": 800.0, "fecha": "2025-04-30"},
        {"cliente": "Marta García", "total": 120.0, "fecha": "2025-05-05"}
    ]

#  Por defecto la pagina te redirige a inicio
@app.route("/")
def pagina_inicio():
    productos = list(productos_coleccion.find())
    total_stock = sum([p["stock"] for p in productos])

    
    clientes_activos = sum(1 for c in clientes if c["activo"])
    cliente_top = max(clientes, key=lambda c: c["pedidos"])

    
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




#Clientes
@app.route('/clientes')
def pagina_clientes():
    pagina = "clientes"



    # Conteo de clientes activos
    clientes_activos = 0
    for cliente in clientes:
        if cliente["activo"]:
            clientes_activos += 1

    # Cliente con más pedidos
    cliente_top = clientes[0]
    for cliente in clientes:
        if cliente["pedidos"] > cliente_top["pedidos"]:
            cliente_top = cliente

    return render_template("lista_usuarios.html", 
                           pagina = pagina,
                           nombre_admin=nombre_admin,
                           tienda=tienda,
                           fecha=fecha,
                           clientes=clientes,
                           clientes_activos=clientes_activos,
                           cliente_top=cliente_top,)



#Registrar Cliente POST
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
        return redirect("/registrar_usuario")

    if not nombre or not email:
        flash("El nombre y el correo electrónico no pueden estar vacíos.")
        return redirect("/registro_usuario")

    nuevo = {
        "nombre": nombre,
        "email": email,
        "activo": activo,
        "pedidos": pedidos
    }

    clientes.append(nuevo)
    flash("Cliente registrado correctamente.")
    return redirect("/clientes")

#Registrar Cliente GET
@app.route("/clientes_nuevo", methods=["GET"])
def formulario_nuevo_cliente():
    return render_template("registro_usuario.html", 
        pagina="clientes",
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha
    )



#Pedidos
@app.route('/pedidos')
def pagina_pedidos():
    pagina = "pedidos"
    # Lista de pedidos
    pedidos = [
        {"cliente": "Ana Torres", "total": 1500.0, "fecha": "2025-05-01"},
        {"cliente": "Marta García", "total": 240.0, "fecha": "2025-05-03"},
        {"cliente": "Luis Pérez", "total": 800.0, "fecha": "2025-04-30"},
        {"cliente": "Marta García", "total": 120.0, "fecha": "2025-05-05"}
    ]

    # Cálculo de ingreso total
    ingreso_total = 0
    for pedido in pedidos:
        ingreso_total += pedido["total"]

    return render_template(
        'lista_pedidos.html',
        pagina = pagina,
        nombre_admin=nombre_admin,
        tienda=tienda,
        fecha=fecha,
        pedidos=pedidos,
        ingreso_total=ingreso_total
    )
    



#Productos
@app.route('/productos')
def pagina_productos():
    datos_productos = productos_coleccion.find()  # Datos sin procesar
    productos = [Producto.from_dict(p) for p in datos_productos]  # Convertir a objetos Producto
    
    total_stock = sum(producto.stock for producto in productos)

    return render_template('lista_productos.html',
                           productos=productos,
                           total_stock=total_stock,
                           nombre_admin=nombre_admin,
                           tienda=tienda,
                           fecha=fecha)
#Detalle Producto
@app.route('/producto/<producto_id>')
def detalle_producto(producto_id):
    # Buscar el producto en MongoDB por _id
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


#Formulario
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

    # Buscar producto existente por nombre (insensible a mayúsculas) y categoría
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



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/tienda", methods=["GET", "POST"])
def tienda_inicio():
    productos = list(productos_coleccion.find())

    categoria_seleccionada = request.args.get('categoria', None)
    if categoria_seleccionada:
        productos = [producto for producto in productos if
                     producto['categoria'].lower() == categoria_seleccionada.lower()]

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


if __name__ == '__main__':
    app.run(debug=True)