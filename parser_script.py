import os
import feedparser

# URL del RSS del podcast
podcast_rss_url = "https://anchor.fm/s/5879dae4/podcast/rss"

def main():
    # Obtener el directorio actual
    current_directory = os.getcwd()

    feed = feedparser.parse(podcast_rss_url)
    
    # Aquí puedes procesar la información del feed como desees
    # Por ejemplo, imprimir los títulos de los episodios recientes
    for entry in feed.entries:
        # Obtener las primeras 5 palabras del título
        words = entry.title.split()[:5]
        
        # Crear el nombre del archivo sustituyendo espacios por guiones
        file_name = "-".join(words) + ".md"
        
        # Crear y escribir en el archivo temporal
        with open(os.path.join(current_directory, file_name), "w") as file:
            file.write(entry.title)
            print(f"Archivo '{file_name}' creado.")
    
if __name__ == "__main__":
    main()
