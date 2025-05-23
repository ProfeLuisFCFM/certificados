import hashlib
import datetime
import pytz

def generar_codigo(nombre, codigo_curso, fecha=None):
    tz = pytz.timezone("America/Monterrey")
    if fecha is None:
        fecha = datetime.datetime.now(tz)
    timestamp = int(fecha.timestamp())
    print(timestamp)
    
    base = f"{nombre}-{codigo_curso}-{timestamp}"
    hash_ = hashlib.sha256(base.encode()).hexdigest().upper()
    codigo = "-".join([hash_[i:i+4] for i in range(0, 16, 4)])
    return codigo

# Ejemplo de uso
nombre = "Claudia Estefania Pacheco Aguirre"
curso = "PPFEA2505"
codigo = generar_codigo(nombre, curso)
print("Código único: ", codigo.lower())
