from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

def dividir_texto(texto, max_caracteres=50):
    """Divide el texto en líneas que no excedan max_caracteres"""
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        if len(linea_actual + " " + palabra) <= max_caracteres:
            if linea_actual:
                linea_actual += " " + palabra
            else:
                linea_actual = palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    
    if linea_actual:
        lineas.append(linea_actual)
    
    return lineas

def optimizar_autores_en_lineas(autores_texto, max_caracteres_por_linea=60):
    """Optimiza los autores en líneas, poniendo varios en una misma línea SEPARADOS POR COMAS"""
    # Separar autores individuales (acepta múltiples separadores)
    separadores = [',', '-', ';', '|', '/', 'y']
    autores = []
    texto_limpio = str(autores_texto).strip()
    
    # Buscar el separador usado
    separador_encontrado = None
    for sep in separadores:
        if sep in texto_limpio:
            separador_encontrado = sep
            break
    
    if separador_encontrado:
        # Separar y limpiar autores
        autores = [autor.strip() for autor in texto_limpio.split(separador_encontrado) if autor.strip()]
    else:
        autores = [texto_limpio]
    
    # Optimizar distribución en líneas SIEMPRE con comas
    lineas_optimizadas = []
    linea_actual = ""
    
    for i, autor in enumerate(autores):
        # Si es el primer autor de la línea
        if not linea_actual:
            linea_actual = autor
        # Si el autor cabe en la línea actual
        elif len(linea_actual + ", " + autor) <= max_caracteres_por_linea:
            linea_actual += ", " + autor
        # Si no cabe, empezar nueva línea
        else:
            lineas_optimizadas.append(linea_actual)
            linea_actual = autor
    
    # Añadir la última línea
    if linea_actual:
        lineas_optimizadas.append(linea_actual)
    
    return lineas_optimizadas

def generar_certificado(autores, tipo_participacion, titulo, numero, carpeta_destino, ruta_plantilla):
    # Cargar plantilla desde la carpeta específica
    img = Image.open(ruta_plantilla)
    draw = ImageDraw.Draw(img)
    
    # Configurar fuente
    try:
        fuente_texto = ImageFont.truetype("arial.ttf", 36)
        fuente_titulo = ImageFont.truetype("arial.ttf", 34)
        fuente_marcador = ImageFont.truetype("arial.ttf", 20)
    except:
        fuente_texto = ImageFont.load_default()
        fuente_titulo = ImageFont.load_default()
        fuente_marcador = ImageFont.load_default()
    
    # PROCESAR AUTORES OPTIMIZADO (SIEMPRE CON COMAS)
    lineas_autores = optimizar_autores_en_lineas(str(autores), max_caracteres_por_linea=60)
    
    # Posición inicial del nombre (ABAJO)
    x_nombre = 192
    y_nombre_base = 678  # Posición original del nombre único
    
    # Si hay múltiples líneas, calcular nueva posición BASE (más arriba)
    if len(lineas_autores) > 1:
        espacio_entre_autores = 35
        # La posición base sube según la cantidad de líneas
        y_nombre_base = 678 - ((len(lineas_autores) - 1) * espacio_entre_autores)
    
    # Escribir autores optimizados (siempre con comas)
    for i, linea_autores in enumerate(lineas_autores):
        y_pos_autor = y_nombre_base + (i * 35)  # 35px entre líneas
        draw.text((x_nombre, y_pos_autor), linea_autores, fill="black", font=fuente_texto)
    
    # Marcar tipo de participación
    bbox = draw.textbbox((0, 0), "X", font=fuente_marcador)
    ancho_x = bbox[2] - bbox[0]
    alto_x = bbox[3] - bbox[1]
    
    centros = {
        "conferencista": (121, 847),
        "presentación oral": (541, 847),
        "presentacion oral": (541, 847),
        "póster": (1033, 847),
        "poster": (1033, 847)
    }
    
    tipo_limpio = tipo_participacion.lower().strip()
    if tipo_limpio in centros:
        centro_x, centro_y = centros[tipo_limpio]
        x_pos = centro_x - (ancho_x // 2)
        y_pos = centro_y - (alto_x // 2) - 3
        draw.text((x_pos, y_pos), "X", fill="black", font=fuente_marcador)
    else:
        print(f"⚠️  Tipo de participación no reconocido: '{tipo_participacion}'")
    
    # Escribir título con salto de línea automático
    lineas_titulo = dividir_texto(str(titulo), max_caracteres=50)
    
    x_titulo = 291
    y_titulo_base = 938
    espacio_entre_lineas = 38
    
    for i, linea in enumerate(lineas_titulo):
        y_pos_titulo = y_titulo_base + (i * espacio_entre_lineas)
        draw.text((x_titulo, y_pos_titulo), linea, fill="black", font=fuente_titulo)
    
    # Guardar certificado
    primer_autor = autores.split(',')[0].split('-')[0].strip() if any(sep in autores for sep in [',', '-']) else autores
    nombre_archivo = f"Certificado_{numero:03d}_{primer_autor.replace(' ', '_')}.pdf"
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
    img.save(ruta_completa)
    print(f"✅ Certificado {numero:03d} generado: {nombre_archivo}")
    print(f"   👥 Autores: {len(lineas_autores)} línea(s) - Original: '{autores}'")

def main():
    # Configurar rutas
    carpeta_plantillas = "plantillas_certificados"
    carpeta_origen = "certificados_trabajos_sin_generar"
    carpeta_destino = "certificados_trabajos_generados"
    
    # Crear carpeta destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
        print(f"📁 Carpeta creada: {carpeta_destino}")
    
    # Buscar plantilla
    ruta_plantilla = os.path.join(carpeta_plantillas, 'Certificado_trabajos.jpg')
    
    if not os.path.exists(ruta_plantilla):
        print(f"❌ Error: No se encuentra la plantilla en {ruta_plantilla}")
        return
    
    # Verificar archivo Excel
    archivos_posibles = [
        os.path.join(carpeta_origen, 'participantes.xlsx'),
        os.path.join(carpeta_origen, 'participantes.xls'),
        'participantes.xlsx',
        'participantes.xls'
    ]
    
    archivo_encontrado = None
    for archivo in archivos_posibles:
        if os.path.exists(archivo):
            archivo_encontrado = archivo
            break
    
    if not archivo_encontrado:
        print("❌ Error: No se encuentra el archivo Excel")
        return
    
    try:
        # Leer el archivo Excel
        print(f"📖 Leyendo datos desde: {archivo_encontrado}")
        datos = pd.read_excel(archivo_encontrado)
        
        # Verificar columnas
        columnas_requeridas = ['nombre', 'participacion', 'titulo']
        for columna in columnas_requeridas:
            if columna not in datos.columns:
                print(f"❌ Error: El Excel no tiene la columna '{columna}'")
                print(f"📋 Columnas encontradas: {list(datos.columns)}")
                return
        
        print(f"📊 Se encontraron {len(datos)} participantes")
        print("=" * 60)
        
        # Generar certificados
        for i, (index, fila) in enumerate(datos.iterrows(), 1):
            print(f"🔄 Procesando {i}/{len(datos)}: {fila['nombre'][:50]}...")
            
            generar_certificado(
                autores=str(fila['nombre']),
                tipo_participacion=str(fila['participacion']),
                titulo=str(fila['titulo']),
                numero=i,
                carpeta_destino=carpeta_destino,
                ruta_plantilla=ruta_plantilla
            )
        
        print("=" * 60)
        print(f"🎉 ¡Proceso completado! Se generaron {len(datos)} certificados")
        print(f"📂 Certificados guardados en: {carpeta_destino}")
        
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")

if __name__ == "__main__":
    main()