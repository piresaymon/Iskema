# -*- coding: utf-8 -*-
# Arquivo: iskema/util.py

# Importa a função search da biblioteca googlesearch-python
try:
    from googlesearch import search
    GOOGLESEARCH_AVAILABLE = True
except ImportError:
    print("Aviso: Biblioteca 'googlesearch-python' não encontrada. A busca não funcionará.")
    GOOGLESEARCH_AVAILABLE = False
except Exception as e:
    print(f"Aviso: Erro ao importar 'googlesearch-python': {e}. A busca não funcionará.")
    GOOGLESEARCH_AVAILABLE = False

import time # Para adicionar atrasos entre as requisições, se necessário

def doSearch(query, type_filter, lang="pt-BR", domain="com.br", num=30):
    """
    Realiza uma busca no Google por listagens de diretórios contendo o termo,
    utilizando a biblioteca googlesearch-python.

    Args:
        query (str): Termo de busca.
        type_filter (str): Tipo de arquivo (ex: 'mp3|wma', '.iso', etc.).
        lang (str, optional): Idioma da busca. Defaults to "pt-BR".
        domain (str, optional): Domínio do Google (não utilizado diretamente aqui devido a limitações da lib). Defaults to "com.br".
        num (int, optional): Número aproximado de resultados. Defaults to 30.

    Returns:
        list: Lista de URLs encontradas.
    """
    if not GOOGLESEARCH_AVAILABLE:
        print("Erro: A função de busca do Google não está disponível devido a problemas na biblioteca.")
        return []

    # Constrói a query de busca com os parâmetros específicos
    # Mantém o '?' inicial conforme a lógica original
    # Inclui o parâmetro de idioma diretamente na query, se relevante
    search_query = f"?intitle:index? {type_filter} {query} -html -wallywashis"
    # Nota: O parâmetro 'lang' pode não ser diretamente passado para o Google via esta lib.
    # A configuração do idioma da interface pode depender das configurações do agente ou do Google no lado deles.

    print(f"Buscando (via googlesearch-python): {search_query}")

    results = []
    try:
        # --- CORREÇÃO: Usando apenas os argumentos mais básicos e seguros ---
        # A função 'search' retorna um iterador (gerador)
        # stop=num tenta obter 'num' resultados
        # Adicionamos um pequeno atraso manual dentro do loop para ser gentil com o Google
        search_results = search(search_query, num_results=num) # Removidos lang e tld
        
        for i, url in enumerate(search_results):
            # --- CORREÇÃO: Adiciona pausa manual ---
            # Adiciona um pequeno atraso a cada 5-10 resultados
            if i > 0 and i % 5 == 0:
                 time.sleep(0.5) # Pausa de 0.5 segundo a cada 5 resultados
                 
            # Adiciona validações básicas
            if url and url.startswith(('http://', 'https://')):
                 # Filtra links óbvios do Google
                # Ampliando a lista de domínios do Google para filtrar
                google_domains = [
                    'google.com', 'support.google.com', 'accounts.google.com',
                    'policies.google.com', 'maps.google.com', 'mail.google.com',
                    'drive.google.com', 'docs.google.com', 'photos.google.com',
                    'youtube.com', 'play.google.com', 'news.google.com'
                ]
                is_google_link = any(gd in url for gd in google_domains)
                
                if not is_google_link:
                    if url not in results: # Evita duplicatas
                        results.append(url)
                        print(f"  URL encontrada: {url}") # Log opcional
            
            # Limita o número de resultados à quantidade solicitada
            if len(results) >= num:
                break
            
    except Exception as e:
        # Captura erros comuns como HTTP 429 (Too Many Requests), bloqueios, etc.
        print(f"Erro durante a busca no Google: {e}")
        # Dependendo do erro, pode ser útil retornar os resultados parciais encontrados até agora
        # return results 
        # Ou retornar uma lista vazia para indicar falha completa
        return []

    print(f"DEBUG: Número de resultados finais encontrados: {len(results)}")
    return results

# Fim do arquivo