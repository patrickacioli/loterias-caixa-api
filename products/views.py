from django.shortcuts import render
import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from caixa.scripts import run
import os, time
from os import walk
from datetime import datetime
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from stat import *


@api_view(['GET', 'POST'])
def api(request):
    if request.method == 'GET':
        try: 
            nro     = request.query_params["nro"]
            contest = request.query_params["contest"]            
            if nro == "last":
                print(nro)
                # Buscar arquivos no diretório 
                f, dates = [], []
                for (dirpath, dirnames, filenames) in walk("static/api/%s" % contest):
                    f.extend(filenames)                    
                    break 
                for file_ in f:
                    dates.append(os.stat("static/api/%s/%s" % (contest, file_))[ST_CTIME])                
                last = max(dates)
                for file_ in f:
                    if os.stat("static/api/%s/%s" % (contest, file_))[ST_CTIME] == last:
                        with open("static/api/%s/%s" % (contest, file_), "r") as outfile:
                            data = json.load(outfile)        
            else:
                with open("static/api/%s/%s.json" % (contest, nro), "r") as outfile:
                    try:
                        data = json.load(outfile)
                    except Exception as a:
                        data = {"response":"500"}
                        print(json.load(outfile[0]))


            return JsonResponse(data)

        except Exception as a:
            return a

def home(request):
    return render(request, "home.html")

# Create your views here.
@api_view(['GET', 'POST'])
def process(request):
    if request.method == 'POST':        
        result = run.run(request.data["contest"].lower())        
        return render(request, "content.html", {
            "title"   : "Processo finalizado!",
            "content" : result,
            "class"   : "success",
            "loteria" : request.data["contest"].lower()
            }
        )
