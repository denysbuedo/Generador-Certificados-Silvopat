from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

def generar_certificado_participacion(nombre, tipo_participacion, numero, carpeta_destino, ruta_plantilla):
    # Cargar plantilla desde la carpeta específica
    img = Image.open(ruta_plantilla)
    draw = ImageDraw.Draw(img)
    
    # Configurar fuente
    try:
        fuente_texto = ImageFont.truetype("arial.ttf", 36)
        fuente_marcador = ImageFont.truetype("arial.ttf", 20)
    except:
        fuente_texto = ImageFont.load_default()
        fuente_marcador = ImageFont.load_default()
    
    # Escribir nombre (SUBIDO 1px MÁS - total 8px desde original)
    draw.text((192, 670), nombre, fill="black", font=fuente_texto)  # 678 - 8 = 670
    
    # Marcar tipo de participación - COORDENADAS AJUSTADAS
    bbox = draw.textbbox((0, 0), "X", font=fuente_marcador)
    ancho_x = bbox[2] - bbox[0]
    alto_x = bbox[3] - bbox[1]
    
    centros = {
        "delegado": (181, 891),
        "invitado": (526, 891),
        "expositor": (870, 894),  # AJUSTADO: 892 → 894 (bajado 2px más)
        "comité organizador": (181, 961),
        "comite organizador": (181, 961),
        "comité científico": (720, 961),
        "comite cientifico": (720, 961)
    }
    
    # Buscar el tipo de participación
    tipo_limpio = tipo_participacion.lower().strip()
    if tipo_limpio in centros:
        centro_x, centro_y = centros[tipo_limpio]
        x_pos = centro_x - (ancho_x // 2)
        y_pos = centro_y - (alto_x // 2) - 3
        draw.text((x_pos, y_pos), "X", fill="black", font=fuente_marcador)
        print(f"   ✅ Marcado como: {tipo_participacion}")
    else:
        print(f"⚠️  Tipo de participación no reconocido: '{tipo_participacion}'")
    
    # Guardar certificado
    nombre_archivo = f"Certificado_Participacion_{numero:03d}_{nombre.replace(' ', '_')}.pdf"
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
    img.save(ruta_completa)
    print(f"✅ Certificado Participación {numero:03d} generado: {nombre_archivo}")

def main_participacion():
    # Configurar rutas
    carpeta_plantillas = "plantillas_certificados"
    carpeta_origen = "certificados_participacion_sin_generar"
    carpeta_destino = "certificados_participacion_generados"
    
    # Crear carpetas si no existen
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
        print(f"📁 Carpeta creada: {carpeta_destino}")
    
    if not os.path.exists(carpeta_origen):
        os.makedirs(carpeta_origen)
        print(f"📁 Carpeta creada: {carpeta_origen}")
    
    # Buscar plantilla
    nombre_plantilla = "Certificado_participacion.jpg"
    ruta_plantilla = os.path.join(carpeta_plantillas, nombre_plantilla)
    
    if not os.path.exists(ruta_plantilla):
        print(f"❌ Error: No se encuentra la plantilla en {ruta_plantilla}")
        print("💡 Asegúrate de que la plantilla esté en la carpeta 'plantillas_certificados'")
        return
    
    # Verificar archivo Excel
    archivos_posibles = [
        os.path.join(carpeta_origen, 'participantes_participacion.xlsx'),
        os.path.join(carpeta_origen, 'participantes_participacion.xls'),
        os.path.join(carpeta_origen, 'participantes.xlsx'),
        os.path.join(carpeta_origen, 'participantes.xls')
    ]
    
    archivo_encontrado = None
    for archivo in archivos_posibles:
        if os.path.exists(archivo):
            archivo_encontrado = archivo
            break
    
    if not archivo_encontrado:
        print("❌ Error: No se encuentra el archivo Excel")
        print(f"💡 Buscando en: {carpeta_origen}")
        return
    
    try:
        # Leer el archivo Excel
        print(f"📖 Leyendo datos desde: {archivo_encontrado}")
        datos = pd.read_excel(archivo_encontrado)
        
        # Verificar que tenga las columnas necesarias
        columnas_requeridas = ['nombre', 'participacion']
        for columna in columnas_requeridas:
            if columna not in datos.columns:
                print(f"❌ Error: El Excel no tiene la columna '{columna}'")
                print(f"📋 Columnas encontradas: {list(datos.columns)}")
                return
        
        print(f"📊 Se encontraron {len(datos)} participantes")
        print("=" * 60)
        
        # Generar certificados para cada participante
        for i, (index, fila) in enumerate(datos.iterrows(), 1):
            print(f"🔄 Procesando {i}/{len(datos)}: {fila['nombre']}")
            
            generar_certificado_participacion(
                nombre=str(fila['nombre']),
                tipo_participacion=str(fila['participacion']),
                numero=i,
                carpeta_destino=carpeta_destino,
                ruta_plantilla=ruta_plantilla
            )
        
        print("=" * 60)
        print(f"🎉 ¡Proceso completado! Se generaron {len(datos)} certificados de participación")
        print(f"📂 Certificados guardados en: {carpeta_destino}")
        
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")

if __name__ == "__main__":
    main_participacion()