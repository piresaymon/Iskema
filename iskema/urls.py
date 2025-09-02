# Arquivo: iskema/urls.py

from django.contrib import admin # Se você descomentou o admin em settings.py
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Importe suas views específicas
from core.views import index, find, construction

# Se você tiver uma view personalizada para erro 500, pode configurá-la assim:
# from django.views.defaults import server_error
# handler500 = 'iskema.views.custom_server_error' # Ou uma view sua
# Ou, se quiser manter a padrão, não precisa definir handler500

urlpatterns = [
    # path('admin/', admin.site.urls), # Descomente se estiver usando o admin
    path('', find, name='home'), # Mapeia a raiz para a view 'find'
    path('index/', index, name='index'),
    path('construction/', construction, name='construction'),
    # Adicione outras URLs aqui
    # Exemplo: path('outra_app/', include('outra_app.urls')),
]

# Adiciona URLs para servir arquivos estáticos durante o desenvolvimento
urlpatterns += staticfiles_urlpatterns()
