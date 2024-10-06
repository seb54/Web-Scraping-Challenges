# Web Scraping Challenges

Ce repository contient une série de scripts Python utilisant Selenium pour effectuer diverses tâches de web scraping. Chaque script est conçu pour automatiser la collecte d'informations spécifiques sur des pages web, principalement des citations du site [Quotes to Scrape](https://quotes.toscrape.com/).

## Prérequis

Pour exécuter ces scripts, vous devez disposer de :

- Python 3.x
- Selenium
- Un WebDriver compatible (par exemple, ChromeDriver)

### Installation des dépendances

1. Installez Selenium via pip :

```sh
pip install selenium
```

2. Téléchargez ChromeDriver depuis [le site officiel](https://sites.google.com/chromium.org/driver/) et assurez-vous que son chemin est correctement configuré.

## Scripts disponibles

### 1. `get_first_quote.py`

Ce script ouvre une page avec des citations retardées par JavaScript et extrait la première citation visible.

**Usage :**

```sh
python get_first_quote.py
```

### 2. `get_fifth_quote_with_delay.py`

Ce script est conçu pour naviguer vers une page de citations avec un délai de chargement, attendre que toutes les citations soient visibles, et extraire la cinquième citation.

**Usage :**

```sh
python get_fifth_quote_with_delay.py
```

### 3. `get_einstein_music_quote.py`

Ce script permet de rechercher une citation spécifique sur le site en sélectionnant un auteur et un tag, puis de soumettre le formulaire de recherche.

**Usage :**

```sh
python get_einstein_music_quote.py
```

### 4. `find_most_repeated_tag.py`

Ce script scrute une page de tableau de citations et compte les occurrences des différents tags.

**Usage :**

```sh
python find_most_repeated_tag.py
```

### 5. books_scraper.py

Ce script scrape les catégories de livres sur le site "Books to Scrape" et calcule le nombre de livres et le prix moyen par catégorie.

**Usage :**

```sh
python books_scrapper.py
```
### 6. bot_connect_count_pages.py

Ce script permet de se connecter à un site en simulant une saisie humaine, puis de naviguer à travers la pagination pour collecter des informations.

**Usage :**

```sh
python bot_connect_count_pages.py
```

### 7. count_quotes.py

Ce script fait défiler une page avec des citations jusqu'à ce qu'il n'y ait plus de nouvelles citations à charger, puis extrait toutes les citations valides.

**Usage :**

```sh
python count_quotes.py
```


## Configuration du WebDriver

Pour chaque script, vous devez spécifier le chemin vers votre ChromeDriver. Cela est fait dans la fonction `configure_driver()` en modifiant la ligne suivante :

```python
driver = configure_driver("..\\drivers\\chromedriver.exe")
```

Assurez-vous de remplacer le chemin par celui où est situé votre ChromeDriver.

