#!/usr/bin/python3

import requests
import re
import os
import stat
import subprocess

def extraer_ultima_version_comunidad_linux():
    url = "https://portswigger.net/burp/releases/community/latest"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error al obtener la página.")
        return None
    
    html = response.text
    
    version_match = re.search(r'Professional / Community (\d+\.\d+\.\d+)', html)
    if not version_match:
        print("No se encontró la versión en la página.")
        return None
    
    version = version_match.group(1)
    print(f"Versión detectada: {version}")
    
    download_url = f"https://portswigger.net/burp/releases/download?product=community&version={version}&type=Linux"
    
    return version, download_url

def descargar_burpsuite_linux(url, version):
    file_name = f"burpsuite_community_linux_v{version}_64.sh"
    
    print(f"Descargando desde: {url}")
    
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            print(f"Error al descargar: Status code {r.status_code}")
            return None
        
        with open(file_name, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print(f"Archivo descargado: {file_name}")
    return file_name

def dar_permisos_ejecucion(file_path):
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)
    print(f"Permisos de ejecución asignados a: {file_path}")

def ejecutar_instalador_con_sudo(file_path):
    print(f"Ejecutando instalador con sudo: {file_path}")
    try:
        subprocess.run(["sudo", f"./{file_path}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el instalador: {e}")

if __name__ == "__main__":
    resultado = extraer_ultima_version_comunidad_linux()
    if resultado:
        version, url_descarga = resultado
        archivo = descargar_burpsuite_linux(url_descarga, version)
        if archivo:
            dar_permisos_ejecucion(archivo)
            ejecutar_instalador_con_sudo(archivo)
