# POKEDEX com DJANGO e POKEAPI

Este é um projeto de aplicação web para introduzir o framework Django e conexões com API. Para exemplo, utilizamos a POKEAPI https://pokeapi.co/

## Configuração do ambiente

- No console windows:
```bash
python -m venv env
python.exe -m pip install --upgrade pip
. env/Scripts/activate
django-admin startproject core .
python manage.py startapp pokedex
pip install pillow
pip install requests
```
- Caso algum comando retorne erro de permissão:
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Configurações da aplicação
- Em *core/settings.py*
```python
import os

...

"DIRS": [BASE_DIR / "templates"],

...

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
```

## Configurando Urls e Views
- Em *core/urls.py*
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pokedex.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
- Em *pokedex/urls.py*
```python
from django.urls import path
from . import views

urlpatterns = [
    path('/', views.index, name='index')
]
```
- Em *pokedex/views.py*
```python
from django.shortcuts import render

# Create your views here.
def index(request):
    ctx = {}
    return render(request, 'index.html', ctx=ctx)
```
- Em *templates/index.html*
```html
<h1>Hello, world!</h1>
```
- Testar a aplicação
```bash
python manage.py runserver
```

## Template

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokedex</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>

<body>
    <!-- <div class="pokemon-info">
        <div class="pokemon-main">
            <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png" alt="Imagem do Ditto">
            <h5>Ditto</h5>
            <button><a>Voltar</a></button>
        </div>
        <div class="pokemon-stats">
            <p>HP <span>48</span></p>
            <p>ATTACK <span>48</span></p>
            <p>DEFENSE <span>48</span></p>
            <p>SPECIAL DEF <span>48</span></p>
            <p>SPECIAL ATK <span>48</span></p>
            <p>SPEED <span>48</span></p>
        </div>
    </div>-->

    <form method="POST">
        {% csrf_token %}
        <img width="150px" src="{% static 'assets/img/logo.png' %}" alt="Logo Pokemon">
        <input type="text" placeholder="Digite o nome do pokemon" name="pokemon">
        <button type="submit">Buscar</button>
    </form>

</body>
</html>
```

## Estilos
```css
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

body {
  background: rgb(27,27,27);
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

form {
  background: rgb(12,12,12);
  padding: 128px 128px;
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
}

form button {
  padding: 8px 32px;
  background: rgb(245,245,245);
  color: rgb(12,12,12);
  margin-top: 8px;
  cursor: pointer;
}

form input {
  height: 32px;
  width: 220px;
  text-align: center;
}

.pokemon-info {
  background: rgb(12,12,12);
  padding: 128px 128px;
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
}

.pokemon-info .pokemon-main {
  background: rgb(222,222,222);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  flex-direction: column;
  padding: 32px 64px;
  border-radius: 32px;
}

.pokemon-info .pokemon-main img {
  border-radius: 50%;
  border: 1px solid #aeaeae;
  box-shadow: 1px 1px 2px 4px rgba(0,0,0,0.1);
}

.pokemon-info .pokemon-main button {
  padding: 8px 32px;
  background: rgb(245,245,245);
  color: rgb(12,12,12);
  margin-top: 8px;
  cursor: pointer;  
}

.pokemon-info .pokemon-main button a {
  text-decoration: none;
  outline: rgba(0,0,0,0.2);
  border: none;
  color: #000;
  transition: 200ms;
}

.pokemon-info .pokemon-main button:hover {
  box-shadow: 1px 1px 2px 2px rgba(0,0,0,0.1);
}

.pokemon-info .pokemon-stats {
  background: rgb(222,222,222);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  flex-direction: column;
  padding: 32px 64px;
  border-radius: 32px;
}

.pokemon-info .pokemon-stats span {
  font-size: 24px;
  margin-left: 8px;
  border: 1px solid #aeaeae;
  box-shadow: 1px 1px 2px 4px rgba(0,0,0,0.1);
  padding: 4px 4px;
}
```
### Views

```python
from django.shortcuts import render
import requests

def get_pokemon_info(name):
    url = f'http://pokeapi.co/api/v1/pokemon/{name}/'
    headers = {"Content-Type": "application/json"} 
    response = requests.get(url, headers=headers) 
    pokemon_info = response.json() 

    pokemon_info_dict = {'name': name.upper()}
    pokemon_info_dict['image_url'] = pokemon_info['sprites']['front_default']

    for stat in pokemon_info['stats']:
        stat_name = stat['stat']['name'].replace('-', '_')
        pokemon_info_dict[stat_name] = stat['base_stat']

    return pokemon_info_dict

# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get("pokemon")
        name = name.lower()
        if not name:
            ctx = {'data': False}
            return render(request, 'index.html', context=ctx)            
        
        try:
            ctx = get_pokemon_info(name)
            ctx['data'] = True
        except:
            ctx = {'data': False}
            return render(request, 'index.html', context=ctx)              

        return render(request, 'index.html', context=ctx)
    else:
        ctx = {'data': False}
        return render(request, 'index.html', context=ctx)
```

### Referências

- https://github.com/WillAngelis/Pokedex
- https://web-pokedex.vercel.app/