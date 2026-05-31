from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import buscar_criaturas, obtener_criatura


@login_required
def bestiario(request):
    
    #Página principal del bestiario con un buscador usando la API de Open5e
    nombre = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    criaturas, error = buscar_criaturas(nombre, tipo)

    return render(request, "api_client/bestiario.html", {
        "criaturas": criaturas,
        "error": error,
        "query": nombre,
        "tipo": tipo,
    })


@login_required
def detalle_criatura(request, slug):
    #Página de detalle de una criatura externa.
    criatura, error = obtener_criatura(slug)

    return render(request, "api_client/detalle_criatura.html", {
        "criatura": criatura,
        "error": error,
    })
