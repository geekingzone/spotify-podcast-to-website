import os
import feedparser
import unicodedata
from datetime import datetime

# URL del RSS del podcast
podcast_rss_url = "https://anchor.fm/s/5879dae4/podcast/rss"

def remove_special_characters(text):
    # Normalizar el texto y eliminar caracteres especiales
    normalized_text = unicodedata.normalize("NFKD", text)
    cleaned_text = ''.join([c for c in normalized_text if not unicodedata.combining(c)])
    return cleaned_text

def format_pub_date(pub_date):
    # Analizar la fecha desde el formato del pubDate del RSS
    pub_date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
    
    # Formatear la fecha en el formato deseado (YYYY-MM-DD-)
    formatted_date = pub_date_obj.strftime("%Y-%m-%d-")
    return formatted_date

def main():
    # Directorio destino de los episodios
    posts_directory = "../website/_posts/"

    feed = feedparser.parse(podcast_rss_url)
    
    # Aquí puedes procesar la información del feed como desees
    # Por ejemplo, imprimir los títulos de los episodios recientes
    for entry in feed.entries:
        words = entry.title.split()[:5]
        file_name_prefix = "-".join(words)
        clean_file_name_prefix = remove_special_characters(file_name_prefix)

        # Obtener la fecha del pubDate del RSS
        pub_date = entry.published  # Aquí debes usar el campo correcto del RSS
        
        # Formatear la fecha
        formatted_date = format_pub_date(pub_date)    
        
        # Crear el nombre completo del archivo en el directorio destino
        file_name = os.path.join(posts_directory, formatted_date + clean_file_name_prefix + ".md")
        
        # Crear y escribir en el archivo
        with open(file_name, "w") as file:
            file.write(entry.title)
            print(f"Archivo '{file_name}' creado.")
    
if __name__ == "__main__":
    main()
