import requests
from geopy.geocoders 
import Nominatim

def obtener_coordenadas(ciudad):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(ciudad)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def calcular_viaje(origen_coord, destino_coord, api_key):
    url = f"https://graphhopper.com/api/1/route?point={origen_coord[0]},{origen_coord[1]}&point={destino_coord[0]},{destino_coord[1]}&vehicle=car&locale=es&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "paths" in data:
        distance_km = data['paths'][0]['distance'] / 1000  
        time_seconds = data['paths'][0]['time'] / 1000 
        return distance_km, time_seconds
    else:
        print(f"Error en la respuesta de la API: {data}")
        return None, None

def convertir_tiempo(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    return horas, minutos, segundos

def mostrar_narrativa(origen, destino, distance_km, horas, minutos, segundos):
    print(f"\nNarrativa del viaje:")
    print(f"De: {origen}")
    print(f"A: {destino}")
    print(f"Distancia: {distance_km:.2f} km")
    print(f"Duración: {horas} horas, {minutos} minutos, {segundos} segundos")

if __name__ == "__main__":
    api_key = "a83a40a3-bed5-47a1-bfd3-ecd940ea34e4"

    while True:
        origen = input("Ciudad de Origen: ")
        destino = input("Ciudad de Destino: ")

        if origen.lower() in ["s", "salir"] or destino.lower() in ["s", "salir"]:
            print("Saliendo del programa...")
            break

        origen_coord = obtener_coordenadas(origen)
        destino_coord = obtener_coordenadas(destino)

        if origen_coord == (None, None) or destino_coord == (None, None):
            print("No se pudo obtener las coordenadas de una o ambas ciudades. Por favor, verifica las ciudades e intenta nuevamente.")
            continue

        distance_km, time_seconds = calcular_viaje(origen_coord, destino_coord, api_key)

        if distance_km is not None and time_seconds is not None:
            horas, minutos, segundos = convertir_tiempo(time_seconds)
            mostrar_narrativa(origen, destino, distance_km, horas, minutos, segundos)
        else:
            print("No se pudo calcular la ruta. Por favor, verifica las ciudades e intenta nuevamente.")