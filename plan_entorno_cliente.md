
# ✅ Plan de Trabajo: Implementación del Entorno Cliente en TecnoMarket

---

## 🧱 ETAPA 1: Estructura y Configuración Base  
🎯 **Objetivo:** Separar el entorno de cliente del de administrador

### Tareas:
- [ ] Crear una plantilla base nueva: `base_cliente.html`
- [ ] Crear una nueva carpeta para vistas públicas: `templates/public/`
- [ ] Crear ruta pública principal: `/tienda` o `/inicio`
- [ ] Añadir navbar para navegación del cliente: "Inicio", "Productos", "Carrito", "Login"
- [ ] Crear diseño de página de productos públicos (sin botones de edición)

---

## 🔐 ETAPA 2: Sistema de Autenticación de Clientes  
🎯 **Objetivo:** Permitir que los clientes se registren e inicien sesión

### Tareas:
- [ ] Crear modelo `Cliente` con: nombre, email, contraseña (hasheada), etc.
- [ ] Implementar rutas:
  - `/registro_cliente` (GET/POST)
  - `/login_cliente` (GET/POST)
  - `/logout_cliente` (GET)
- [ ] Guardar sesiones del cliente autenticado (`session["cliente_id"]`)
- [ ] Asegurar rutas solo accesibles si hay sesión activa
- [ ] Mostrar nombre del cliente en el navbar si está logueado

---

## 🛍️ ETAPA 3: Carrito de Compras  
🎯 **Objetivo:** Que los clientes puedan agregar productos y visualizarlos

### Tareas:
- [ ] Añadir botón **"Agregar al carrito"** en cada producto (visible solo en entorno cliente)
- [ ] Guardar carrito en `session["carrito"]` (estructura: lista de dicts con id, nombre, cantidad, precio)
- [ ] Crear vista `/carrito` con resumen del carrito, total y botón "Realizar pedido"
- [ ] Permitir modificar cantidades o eliminar productos del carrito

---

## 💳 ETAPA 4: Simulación de Pedido y Pasarela  
🎯 **Objetivo:** Simular proceso de compra y enviar confirmación

### Tareas:
- [ ] Crear vista `/checkout`:
  - Mostrar resumen de pedido
  - Formulario con dirección, teléfono, observaciones
- [ ] Crear ruta `/procesar_pedido` que:
  - Valide los datos
  - Guarde un pedido en la BBDD
  - Envíe correo de confirmación al cliente (usando `smtplib`)
  - Vacíe el carrito tras el pedido

---

## 📧 ETAPA 5: Envío de Correo de Confirmación  
🎯 **Objetivo:** Enviar confirmación al cliente con resumen de compra

### Tareas:
- [ ] Configurar SMTP seguro (Mailtrap o Gmail)
- [ ] Crear función reutilizable para enviar correos
- [ ] Incluir en el correo: nombre del cliente, productos, total, dirección

---

## 🔒 ETAPA 6: Restricción de Acceso  
🎯 **Objetivo:** Separar cliente de administrador completamente

### Tareas:
- [ ] Añadir decoradores para restringir acceso a rutas del admin (ej: `@login_required_admin`)
- [ ] Redireccionar usuarios no autenticados si intentan acceder a rutas protegidas
- [ ] Ocultar botones y opciones de administración en las vistas si no está en sesión el admin

---

## 🧪 ETAPA 7: Testing y Refinamiento  
🎯 **Objetivo:** Probar todos los flujos y corregir errores

### Tareas:
- [ ] Probar flujo completo: registro → login → carrito → checkout → confirmación
- [ ] Verificar que el admin no pueda acceder al entorno cliente y viceversa
- [ ] Validar datos del formulario correctamente
- [ ] Probar envío de correo en entorno real o de prueba

---

## 🎁 BONUS: Funcionalidades Extra (Opcionales)

- [ ] Historial de pedidos por cliente
- [ ] Valoraciones o reseñas de productos
- [ ] Recuperar contraseña por email
- [ ] Paginación o filtros en productos
- [ ] Modo oscuro / claro
