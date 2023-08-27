import os
import feedparser
import unicodedata
import re
from datetime import datetime

# URL del RSS del podcast
podcast_rss_url = "https://anchor.fm/s/5879dae4/podcast/rss"

def remove_special_characters(text):
    # Normalizar el texto y eliminar caracteres especiales
    normalized_text = unicodedata.normalize("NFKD", text)
    cleaned_text = ''.join([c for c in normalized_text if not unicodedata.combining(c) and c != ":"])
    return cleaned_text


def format_pub_date(pub_date):
    # Analizar la fecha desde el formato del pubDate del RSS
    pub_date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
    
    # Formatear la fecha en el formato deseado (YYYY-MM-DD-)
    formatted_date = pub_date_obj.strftime("%Y-%m-%d-")
    return formatted_date

def create_file_content(entry):
    content = f"---\n"
    content += f"layout: post\n"
    clean_entry_title = remove_special_characters(entry.title)
    content += f"title: {clean_entry_title}\n"
    # Get the season and episode information
    season = entry.itunes_season  # Access the itunes:season tag
    episode_number = entry.itunes_episode  # Access the itunes:episode tag
    content += f"subtitle: Episodio {episode_number} de la temporada {season}\n"
    content += f"cover-img: {entry.image.url}\n"
    content += f"thumbnail-img: {entry.image.url}\n"
    content += f"share-img: {entry.image.url}\n"
    content += f"tags: [episode]\n"
    content += f"---\n\n"
    # Manejar el caso en el que la descripción no existe
    if 'description' in entry:
        # Buscar y reemplazar URLs con enlaces Markdown
        description_with_links = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                        r'[\g<0>](\g<0>)', entry.description)
        content += description_with_links + '\n'
    else:
        content += f"\n"
    return content

def main():
    # Directorio destino de los episodios
    posts_directory = "../website/_posts/"

    feed = feedparser.parse(podcast_rss_url)
    
    # Aquí puedes procesar la información del feed como desees
    # Por ejemplo, imprimir los títulos de los episodios recientes
    for entry in feed.entries:
        words = entry.title.split()[:6]
        file_name_prefix = "-".join(words)
        clean_file_name_prefix = remove_special_characters(file_name_prefix)

        # Obtener la fecha del pubDate del RSS
        pub_date = entry.published
        
        # Formatear la fecha
        formatted_date = format_pub_date(pub_date)    
        
        # Crear el nombre completo del archivo en el directorio destino
        file_name = os.path.join(posts_directory, formatted_date + clean_file_name_prefix + ".md")
        
        # Crear el contenido del archivo
        file_content = create_file_content(entry)

        # Crear y escribir en el archivo
        with open(file_name, "w") as file:
            file.write(file_content)
            print(f"Archivo '{file_name}' creado.")
    
if __name__ == "__main__":
    main()
