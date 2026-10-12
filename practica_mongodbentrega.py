import sys
import urllib.parse
from pymongo import MongoClient
from pymongo.errors import OperationFailure

# ==========================================
# 1. CONFIGURACIÓN Y CONEXIÓN A ATLAS
# ==========================================
USUARIO = ""
PASSWORD_RAW = "" 

# Codificamos la contraseña por seguridad en la URL
PASSWORD = urllib.parse.quote_plus(PASSWORD_RAW)

MONGO_URI = f"mongodb+srv://{USUARIO}:{PASSWORD}@cluster0.slazngi.mongodb.net/?appName=Cluster0"

print("Conectando a MongoDB Atlas...")
client = MongoClient(MONGO_URI)

# Validamos la conexión inmediatamente antes de ejecutar comandos
try:
    client.admin.command('ping')
    print("✅ ¡Conexión y autenticación exitosas en MongoDB Atlas!\n")
except OperationFailure:
    print("\n❌ ERROR DE AUTENTICACIÓN: Usuario o contraseña incorrectos.")
    print("👉 Revisa las credenciales en MongoDB Atlas -> Database Access.\n")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error al conectar con Atlas: {e}\n")
    sys.exit(1)

# Selección de la Base de Datos y Colección
db = client["tienda_db"]
coleccion = db["productos"]

# Limpiamos la colección previa para evitar duplicados
coleccion.delete_many({})


# ==========================================
# 2. OPERACIÓN: CREATE (INSERTAR)
# ==========================================
print("--- 1. CREATE (Insertar datos) ---")

productos = [
    {
        "sku": "PROD-001",
        "nombre": "Laptop Pro 15",
        "categoria": "Electrónica",
        "precio": 1250.00,
        "stock": 15,
        "activo": True,
        "especificaciones": {"ram": "16GB", "almacenamiento": "512GB SSD"},
        "etiquetas": ["computación", "trabajo"]
    },
    {
        "sku": "PROD-002",
        "nombre": "Smartphone X",
        "categoria": "Electrónica",
        "precio": 800.00,
        "stock": 30,
        "activo": True,
        "especificaciones": {"ram": "8GB", "pantalla": "6.1 pulgadas"},
        "etiquetas": ["móvil", "oferta"]
    },
    {
        "sku": "PROD-003",
        "nombre": "Silla Ergonómica",
        "categoria": "Muebles",
        "precio": 250.00,
        "stock": 8,
        "activo": True,
        "especificaciones": {"material": "Malla", "color": "Negro"},
        "etiquetas": ["oficina", "hogar"]
    },
    {
        "sku": "PROD-004",
        "nombre": "Monitor 4K 27\"",
        "categoria": "Electrónica",
        "precio": 450.00,
        "stock": 20,
        "activo": True,
        "especificaciones": {"resolucion": "3840x2160"},
        "etiquetas": ["computación", "gaming"]
    }
]

resultado_insert = coleccion.insert_many(productos)
print(f"-> Insertados {len(resultado_insert.inserted_ids)} productos correctamente.\n")


# ==========================================
# 3. OPERACIÓN: READ (CONSULTAR)
# ==========================================
print("--- 2. READ (Consultar datos) ---")

# Consulta 1: Buscar por SKU
prod_unico = coleccion.find_one({"sku": "PROD-001"})
print(f"Producto encontrado: {prod_unico['nombre']} (${prod_unico['precio']})")

# Consulta 2: Productos con filtro y proyección
print("\nProductos de Electrónica con precio >= 500:")
filtro = {"categoria": "Electrónica", "precio": {"$gte": 500}}
proyeccion = {"_id": 0, "nombre": 1, "precio": 1}

for p in coleccion.find(filtro, proyeccion):
    print(f" - {p['nombre']}: ${p['precio']}")
print()


# ==========================================
# 4. OPERACIÓN: UPDATE (ACTUALIZAR)
# ==========================================
print("--- 3. UPDATE (Actualizar datos) ---")

filtro_update = {"sku": "PROD-002"}
actualizaciones = {
    "$set": {"precio": 750.00},
    "$push": {"etiquetas": "descuento_especial"}
}

res_update = coleccion.update_one(filtro_update, actualizaciones)
print(f"-> Documentos modificados: {res_update.modified_count}\n")


# ==========================================
# 5. OPERACIÓN: DELETE (ELIMINAR)
# ==========================================
print("--- 4. DELETE (Eliminar datos) ---")

res_delete = coleccion.delete_one({"sku": "PROD-003"})
print(f"-> Documentos eliminados: {res_delete.deleted_count}\n")


# ==========================================
# 6. OPERACIÓN: AGGREGATION (AGREGACIÓN)
# ==========================================
print("--- 5. AGGREGATION (Métricas por categoría) ---")

pipeline = [
    {"$match": {"activo": True}},
    {
        "$group": {
            "_id": "$categoria",
            "total_productos": {"$sum": 1},
            "precio_promedio": {"$avg": "$precio"},
            "valor_inventario": {"$sum": {"$multiply": ["$precio", "$stock"]}}
        }
    },
    {"$sort": {"valor_inventario": -1}},
    {
        "$project": {
            "_id": 0,
            "categoria": "$_id",
            "total_productos": 1,
            "precio_promedio": {"$round": ["$precio_promedio", 2]},
            "valor_inventario": 1
        }
    }
]

resultados = list(coleccion.aggregate(pipeline))

for res in resultados:
    print(f"Categoría: {res['categoria']}")
    print(f"  • Total productos: {res['total_productos']}")
    print(f"  • Precio promedio: ${res['precio_promedio']}")
    print(f"  • Valor inventario: ${res['valor_inventario']}\n")

# Cierre de conexión
client.close()