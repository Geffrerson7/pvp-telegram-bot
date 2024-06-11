import json
from bot.service import get_pokemon_by_name, calculate_rank
from bot.constants import pokedex

dict_ranking = {}
for pokemon in pokedex:
    pokedex_entry = get_pokemon_by_name(pokedex, pokemon["name"])
    ranking_data = calculate_rank(
        pokedex_entry,
        2,
        2,
        2,
        1500,
    )
    first_rank = ranking_data["rank"]
    first_rank["number"] = pokemon["number"]
    dict_ranking[pokemon["name"]] = first_rank
# Guardar el diccionario en un archivo JSON
with open('dict_ranking_1500.json', 'w') as json_file:
    json.dump(dict_ranking, json_file, indent=4)

