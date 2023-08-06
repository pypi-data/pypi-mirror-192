# Sobre GamesDB

GamesDB é uma classe Python que permite a busca de informações sobre jogos eletrônicos em um site com o mesmo nome. A classe usa as bibliotecas BeautifulSoup, requests e fuzzywuzzy.

A classe tem um método eu busca um jogo pela identificação dele no site e um método busca por nome. Ambos retorna uma lista com um dicionário para cada jogo procurado. As seguintes informações do jogo são retornadas:

 -  id
-   game_title
-   overview
-   genres
-   esrb_rating
-   trailer
-   platform
-   region
-   developers
-   publishers
-   release_date
-   players
-   coop
-   cover
-   cover_thumb
-   fanarts
-   screenshots
-   clearlogos

## Como usar

    from games_db import GamesDB
    gdb = GamesDB()
    
### Busca de jogo por identificador:

    games = gbd.get_game_by_id('5')
Retorna uma lista com um dicionário com informações do jogo 

    lista = ['5','23','100']
    games = gbd.get_game_by_id(lista)
   Retorna uma lista com um dicionário para jogo pesquisado.


### Busca de jogo por nome:

    games = gbd.get_game_by_name('Super Mario Word', 'Super Nintendo (SNES)')
    ou
    games = gbd.get_game_by_name('Super Mario Word', 6)
Retorna uma lista com um dicionário com informações do jogo 

    lista = ['5','23','100']
    games = gbd.get_game_by_name(lista, 'Super Nintendo (SNES)')
    ou
    games = gbd.get_game_by_name(lista, 6')
   Retorna uma lista com um dicionário para jogo pesquisado.

### Nomes e códigos de consoles:

    for name, id in gbd.codigo_console.items():
	    print(f'{name}-{id}
