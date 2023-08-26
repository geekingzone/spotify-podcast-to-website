import os
import feedparser
import unicodedata

# URL del RSS del podcast
podcast_rss_url = "https://anchor.fm/s/5879dae4/podcast/rss"

def remove_special_characters(text):
    # Normalizar el texto y eliminar caracteres especiales
    normalized_text = unicodedata.normalize("NFKD", text)
    cleaned_text = ''.join([c for c in normalized_text if not unicodedata.combining(c)])
    return cleaned_text

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
        
        # Crear el nombre completo del archivo en el directorio destino
        file_name = os.path.join(posts_directory, clean_file_name_prefix + ".md")
        
        # Crear y escribir en el archivo
        with open(file_name, "w") as file:
            file.write(entry.title)
            print(f"Archivo '{file_name}' creado.")
    
if __name__ == "__main__":
    main()
