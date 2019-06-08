from django.shortcuts import render
import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from caixa.scripts import run

def api(request, *args, **kwargs):
    try:
        with open('static/json/%s.json' % kwargs["contest"]) as json_file:
            data = json.load(json_file)
            print(data)
        return JsonResponse(data)
    except Exception as a:
        return JsonResponse("ERROR")

def home(request):
    return render(request, "home.html")

# Create your views here.
@api_view(['GET', 'POST'])
def process(request):
    if request.method == 'POST':
        result = run.run(request.data["contest"].lower())
        return render(request, "content.html", {
            "title"   : "Processo iniciado",
            "content" : result,
            "class"   : "success",
            "loteria" : request.data["contest"].lower()
            }
        )
