# Script para limpiar conflictos de Git en base.html

archivo = r"proyecto_3\templates\base.html"

with open(archivo, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Eliminar marcadores de conflicto y contenido duplicado
lineas = contenido.split('\n')
lineas_limpias = []
saltando = False

for linea in lineas:
    if linea.startswith('<<<<<<< HEAD'):
        saltando = True
        continue
    elif linea.startswith('======='):
        continue
    elif linea.startswith('>>>>>>> diego'):
        saltando = False
        continue
    
    if not saltando:
        lineas_limpias.append(linea)

contenido_limpio = '\n'.join(lineas_limpias)

with open(archivo, 'w', encoding='utf-8') as f:
    f.write(contenido_limpio)

print("✓ Archivo base.html limpiado exitosamente")