
from typing import List, Optional
from src.personaje import Personaje
import requests
import random


def generar_personaje_aleatorio(numero: int) -> Optional[Personaje]:
        path = 'https://swapi.dev/api/people/'
        full_path = path + str(numero)
        try:
            response = requests.get(full_path)
            if response.status_code == 200: 
                diccionario = response.json()
                personaje = Personaje(**diccionario)
                return personaje
            return None
        except Exception as error:
            print("No se pudo encontrar el personaje #"+str(numero)+": ", error)
            

def encontrar_personaje(personaje_buscado : str, personajes: List[Personaje]):
    personaje_encontrado = None
    for personaje in personajes:
            if personaje.name == personaje_buscado:
                personaje_encontrado = personaje
                break
    return personaje_encontrado
        