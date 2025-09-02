# Arquivo: iskema/core/views.py
# -*- coding: utf-8 -*-
from django.shortcuts import render  # <-- Import correto
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.utils.encoding import smart_str # <-- Import correto para Django 4+
# Se você estiver usando Django 4.2+, smart_str está em django.utils.encoding
# Se tiver problemas, pode tentar from django.utils.encoding import force_str

from .forms import SearchForm  # Import relativo é preferido
# from .google import search # Esta linha está comentada no original e não é usada
from .util import doSearch      # Import relativo é preferido
# from urllib import unquote # Não usado no código atual, e urllib.unquote é py2
import urllib.parse # Para Python 3

@csrf_exempt
def index(request):
    # return render_to_response("core/construction.html") # <-- ANTIGO
    return render(request, "core/construction.html") # <-- NOVO

@csrf_exempt
def find(request):
    if request.method == 'POST':
        form = SearchForm(request.POST, auto_id=False)
        if form.is_valid():
            # Usar .cleaned_data é mais seguro
            q = form.cleaned_data.get('q', '')
            # Codificar para bytes e depois decodificar para string ascii, ignorando erros
            # ou simplesmente usar o valor limpo diretamente, que já é string.
            # A lógica original com smart_str parece confusa.
            # Vamos simplificar: pegar o valor limpo diretamente.
            # q = smart_str(request.POST['q'], encoding='ascii', errors='ignore')
            
            # Pegando o tipo do POST (verifique se o nome do campo está correto no form)
            # O form só tem 'q'. O 'typeGroup' vem do HTML manualmente.
            # Vamos pegar diretamente do POST como antes, mas com segurança.
            type_group = request.POST.get('typeGroup', '') # Use .get() para evitar KeyError
            
            print(f"Q: {q} , type: {type_group}") # Log atualizado
            
            # Passar os parâmetros corretamente para doSearch
            # Assumindo que doSearch(query, type_filter, ...)
            results = doSearch(query=q, type_filter=type_group)
            
            # Passar contexto explicitamente é melhor que 'locals()'
            context = {
                'form': form,
                'results': results,
                'STATIC_URL': settings.STATIC_URL # Se necessário no template
            }
            # return render_to_response("core/index.html", locals(), context_instance=RequestContext(request)) # <-- ANTIGO
            return render(request, "core/index.html", context) # <-- NOVO

    # Se for GET ou se o POST não for válido
    # elif request.method == 'GET': # O 'else' cobre o GET e casos de POST inválido
    form = SearchForm(auto_id=False)
    context = {
        'form': form,
        'STATIC_URL': settings.STATIC_URL # Se necessário no template
    }
    # context = RequestContext(request, {'form': form,'STATIC_URL' :settings.STATIC_URL}) # <-- ANTIGO
    # return render_to_response("core/index.html", context) # <-- ANTIGO
    return render(request, "core/index.html", context) # <-- NOVO

def construction(request):
    # return render_to_response("core/construction.html") # <-- ANTIGO
    return render(request, "core/construction.html") # <-- NOVO
