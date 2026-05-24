import requests
from django.conf import settings


BASE_URL = getattr(settings, "OPEN5E_BASE_URL", "https://api.open5e.com")


def buscar_criaturas(nombre="", tipo=""):
    #Busca criaturas en la API de Open5e.
    #Si se pasa un nombre, filtra por él.
    #Devuelve una lista de criaturas o una lista vacía si falla.
    
    try:
        params = {"limit": 20, "format": "json"}
        if nombre:
            params["name__icontains"] = nombre
        if tipo:
            params["type"] = tipo.lower()

        response = requests.get(
            f"{BASE_URL}/v2/creatures/",
            params=params,
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("results", []), None

    except requests.exceptions.ConnectionError:
        return [], "No se ha podido conectar con el bestiario externo. Comprueba tu conexión."
    except requests.exceptions.Timeout:
        return [], "El bestiario externo ha tardado demasiado en responder. Inténtalo de nuevo."
    except requests.exceptions.HTTPError as e:
        return [], f"El bestiario externo ha devuelto un error: {e}"
    except Exception:
        return [], "Ha ocurrido un error inesperado al consultar el bestiario externo."


def obtener_criatura(key):
    #Obtiene el detalle de una criatura por su slug.
    #Devuelve la criatura o None si falla.
    
    try:
        response = requests.get(
            f"{BASE_URL}/v2/creatures/{key}/",
            params={"format": "json"},
            timeout=5,
        )
        response.raise_for_status()
        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "No se ha podido conectar con el bestiario externo."
    except requests.exceptions.Timeout:
        return None, "El bestiario externo ha tardado demasiado en responder."
    except requests.exceptions.HTTPError:
        return None, "No se ha encontrado la criatura solicitada."
    except Exception:
        return None, "Ha ocurrido un error inesperado al consultar el bestiario externo."
