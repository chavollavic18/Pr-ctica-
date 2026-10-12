# Práctica MongoDB - Conexión a MongoDB Atlas

Script en Python que se conecta a **MongoDB Atlas** y ejecuta operaciones CRUD
y una agregación sobre una colección de productos.

---

## 📦 1. Instalar dependencias

Abre una terminal y ejecuta:

```bash
pip install pymongo dnspython
```

> `dnspython` es obligatorio para conexiones `mongodb+srv://` (Atlas). Sin él,
> la conexión falla con error de DNS.

---

## ⚙️ 2. Configurar credenciales en el script

Abre el archivo `practica_mongodbentrega.py` con cualquier editor de texto y
localiza la sección **1. CONFIGURACIÓN Y CONEXIÓN A ATLAS** (al inicio del archivo):

```python
USUARIO = ""
PASSWORD_RAW = ""
```

Rellena ambas variables con las credenciales del usuario de MongoDB Atlas:

```python
USUARIO = "tu_usuario_de_atlas"
PASSWORD_RAW = "tu_contraseña_de_atlas"
```

> 🔒 La contraseña se codifica automáticamente con `urllib.parse.quote_plus()`
> en la línea siguiente, así que **no** hay que preocuparse por caracteres
> especiales (`@`, `#`, `%`, etc.).

Guarda el archivo después de editarlo.

---

## 🌐 3. Autorizar la IP en MongoDB Atlas

Para que la conexión funcione, la red desde donde se ejecuta el script debe
estar autorizada en Atlas:

1. Entra a https://cloud.mongodb.com
2. Selecciona tu proyecto → **Network Access** (menú izquierdo).
3. Clic en **Add IP Address**.
4. Opciones:
   - **Add Current IP Address** → autoriza solo tu IP actual.
   - **Allow Access from Anywhere** (`0.0.0.0/0`) → autoriza cualquier IP
     (útil para pruebas o si el profesor lo ejecuta desde otra red).
5. Clic en **Confirm**.

> ⚠️ Si la IP no está autorizada, el script falla con timeout o error de
> conexión, aunque las credenciales sean correctas.

---

## 👤 4. Verificar permisos del usuario en Atlas

El usuario debe tener permisos de lectura/escritura sobre la base de datos:

1. En Atlas ve a **Database Access** (menú izquierdo).
2. Verifica que el usuario exista y tenga el rol:
   - **Read and write to any database** (recomendado), o
   - **Atlas admin**.
3. Si no existe, créalo con **Add New Database User** y guarda usuario y
   contraseña.

---

## ▶️ 5. Ejecutar el script

Desde la terminal, ubicado en la carpeta del archivo:

```bash
python practica_mongodbentrega.py
```

Si todo está correcto, verás:

```
Conectando a MongoDB Atlas...
✅ ¡Conexión y autenticación exitosas en MongoDB Atlas!
```

Y a continuación la ejecución de las operaciones **CREATE**, **READ**,
**UPDATE**, **DELETE** y la **AGGREGATION**.

---

## ❌ Solución de errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'pymongo'` | Falta el driver | `pip install pymongo` |
| `ModuleNotFoundError: No module named 'dns'` | Falta dnspython | `pip install dnspython` |
| `❌ ERROR DE AUTENTICACIÓN` | Usuario o contraseña incorrectos | Revisar en Atlas → **Database Access** |
| Timeout / `ServerSelectionTimeoutError` | IP no autorizada | Agregar IP en Atlas → **Network Access** |
| `bad auth: Authentication failed` | Usuario sin permisos en la BD | Asignar rol `readWrite` en **Database Access** |
