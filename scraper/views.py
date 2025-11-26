from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from django.contrib.auth.decorators import login_required

@login_required
def buscar(request):
    query = request.GET.get('q', '')
    resultados = []
    error = None
    
    if query:
        try:
            search_url = f"https://es.wikipedia.org/w/index.php?search={quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check if we got a direct article match
            if '/wiki/' in response.url and 'search=' not in response.url:
                # Direct article page
                title_element = soup.find('h1', class_='firstHeading')
                content = soup.find('div', class_='mw-parser-output')
                
                if title_element and content:
                    # Get first paragraph
                    paragraphs = content.find_all('p', recursive=False)
                    snippet = ''
                    for p in paragraphs:
                        text = p.get_text().strip()
                        if text and len(text) > 50:
                            snippet = text[:300] + '...' if len(text) > 300 else text
                            break
                    
                    resultados.append({
                        'titulo': title_element.get_text(),
                        'snippet': snippet,
                        'url': response.url
                    })
            else:
                # Search results page
                search_results = soup.find_all('div', class_='mw-search-result-heading')
                
                for result in search_results[:10]:
                    link = result.find('a')
                    if link:
                        titulo = link.get_text()
                        url = 'https://es.wikipedia.org' + link.get('href')
                        
                        # Get snippet
                        result_div = result.find_parent('li')
                        snippet_div = result_div.find('div', class_='searchresult') if result_div else None
                        snippet = snippet_div.get_text().strip() if snippet_div else 'Sin descripción disponible'
                        
                        resultados.append({
                            'titulo': titulo,
                            'snippet': snippet,
                            'url': url
                        })
                
                if not resultados:
                    error = 'No se encontraron resultados para tu búsqueda.'
        
        except requests.exceptions.Timeout:
            error = 'La búsqueda tardó demasiado tiempo. Por favor, intenta de nuevo.'
        except requests.exceptions.ConnectionError:
            error = 'Error de conexión. Verifica tu conexión a internet.'
        except requests.exceptions.HTTPError as e:
            error = f'Error HTTP: {e.response.status_code}'
        except Exception as e:
            error = f'Error inesperado: {str(e)}'
    
    context = {
        'query': query,
        'resultados': resultados,
        'error': error
    }
    
    return render(request, 'buscar.html', context)