import requests, logging, re, time, json, datetime, traceback
from typing import Dict, List, Union
from math import floor
from bot.constants import (
    level_constants,
    null_rank,
    CUMULATIVE_STARDUST,
    CUMULATIVE_CANDY,
)


def retrieve_flag(url: str):
    if url == "https://vanpokemap.com/query2.php":
        return "🇨🇦Vancouver, Canadá"
    elif url == "https://nycpokemap.com/query2.php":
        return "🇺🇸Nueva York, Estados Unidos"
    elif url == "https://londonpogomap.com/query2.php":
        return "🇬🇧Londres, Reino Unido"
    elif url == "https://sgpokemap.com/query2.php":
        return "🇸🇬Singapur, Singapur"
    elif url == "https://sydneypogomap.com/query2.php":
        return "🇦🇺Sydney, Australia"


def fetch_pokemon_data_by_iv(iv):
    """Obtains Pokemon data from multiple sources based on IV and returns a combined list of Pokemon."""
    total_data = []
    urls = [
        "https://vanpokemap.com/query2.php",
        "https://nycpokemap.com/query2.php",
        "https://londonpogomap.com/query2.php",
        "https://sgpokemap.com/query2.php",
        "https://sydneypogomap.com/query2.php",
    ]

    headers = {
        "https://vanpokemap.com/query2.php": {"Referer": "https://vanpokemap.com/"},
        "https://nycpokemap.com/query2.php": {"Referer": "https://nycpokemap.com/"},
        "https://londonpogomap.com/query2.php": {
            "Referer": "https://londonpogomap.com/"
        },
        "https://sgpokemap.com/query2.php": {"Referer": "https://sgpokemap.com/"},
        "https://sydneypogomap.com/query2.php": {
            "Referer": "https://sydneypogomap.com/"
        },
    }

    params = {
        "mons": ",".join(str(i) for i in range(999)),
        "minIV": str(iv),
        "time": int(time.time()),
        "since": 0,
    }

    for url in urls:
        headers_for_url = headers.get(url, {})
        try:
            logging.debug(f"Fetching data from URL: {url} with params: {params}")
            response = requests.get(url, params=params, headers=headers_for_url)
            response.raise_for_status()  # Si ocurre un error, lanzará una excepción
            data = response.json()
            for pokemon in data.get("pokemons", []):
                pokemon["flag"] = retrieve_flag(url)
                total_data.append(pokemon)
        except requests.exceptions.RequestException as e:
            logging.warning(f"Failed to fetch data from {url}: {e}")
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response from {url}: {e}")

    total_data.sort(key=lambda x: x["despawn"], reverse=True)
    return total_data


def retrieve_pokemon_name(pokemon_id):
    """Gets the name of a Pokémon based on its ID using the PokeAPI."""
    try:
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(pokeapi_url)
        response.raise_for_status()

        data = response.json()
        name = data.get("name").title()

        return name
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error fetching Pokémon name for ID {pokemon_id}: {e}")
    except ValueError as e:
        logging.error(f"Error decoding JSON response from PokeAPI: {e}")

    return None


def retrieve_pokemon_height(pokemon_id):
    """Gets the height of a Pokémon based on its ID using the PokeAPI."""
    try:
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(pokeapi_url)
        response.raise_for_status()

        data = response.json()
        height = data.get("height") / 10

        return str(height)
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error fetching Pokemon height for ID {pokemon_id}: {e}")
    except ValueError as e:
        logging.error(f"Error decoding JSON response from PokeAPI: {e}")

    return None


def retrieve_pokemon_weight(pokemon_id):
    """Gets the weight of a Pokémon based on its ID using the PokeAPI."""
    try:
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(pokeapi_url)
        response.raise_for_status()

        data = response.json()
        weight = data.get("weight") / 10

        return str(weight)
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error fetching Pokemon weight for ID {pokemon_id}: {e}")
    except ValueError as e:
        logging.error(f"Error decoding JSON response from PokeAPI: {e}")

    return None


def calculate_remaining_time(despawn, delay):
    """Obtains the despawn time and calculates the remaining time until then."""
    try:
        if despawn is None:
            return None
        else:
            end_time_24h = datetime.datetime.fromtimestamp(despawn)
            current_time = datetime.datetime.now()
            remaining_time = end_time_24h - current_time
            seconds = round(remaining_time.total_seconds() - delay)
            minutes, seconds = divmod(seconds, 60)
            if minutes < 0 or seconds < 0:
                return None
            formatted_dsp = f"{minutes}:{seconds:02}"
            return formatted_dsp
    except Exception as e:
        logging.error(f"Error calculating despawn time: {e}")

    return None


def retrieve_move_icon(move_type):
    """Returns an emoji representing the type of a Pokémon move."""
    if move_type == "Acero":
        return "⚙️"
    elif move_type == "Agua":
        return "💧"
    elif move_type == "Bicho":
        return "🐞"
    elif move_type == "Dragón":
        return "🐲"
    elif move_type == "Eléctrico":
        return "⚡"
    elif move_type == "Fantasma":
        return "👻"
    elif move_type == "Fuego":
        return "🔥"
    elif move_type == "Hielo":
        return "❄️"
    elif move_type == "Hada":
        return "🌸"
    elif move_type == "Lucha":
        return "🥊"
    elif move_type == "Normal":
        return "🔘"
    elif move_type == "Planta":
        return "🌿"
    elif move_type == "Psíquico":
        return "🔮"
    elif move_type == "Roca":
        return "🪨"
    elif move_type == "Siniestro":
        return "☯️"
    elif move_type == "Tierra":
        return "⛰️"
    elif move_type == "Veneno":
        return "☠️"
    elif move_type == "Volador":
        return "🪽"
    else:
        return ""


def retrieve_pokemon_move(pokemon_move_id, pokemon_name):
    """Gets the move name of a Pokemon based on the move ID using the PokeAPI."""

    with open("./data/moves.json", "r") as file:
        moves_data = json.load(file)
    move = moves_data.get(str(pokemon_move_id))
    if move:
        move_name = move.get("name")
        move_type = move.get("type")
        icon = retrieve_move_icon(move_type)
        return {"name": move_name, "icon": icon}
    else:
        print(f"Pokemon:{pokemon_name}, move_id:{pokemon_move_id}")
        return {"name": "", "icon": ""}


def coordinates_waiting_time(coordinates_list_size):
    """Obtains the excecution time of fetch_pokemon_data() function"""
    return 1.9967 * coordinates_list_size + 131.05


def escape_string(input_string):
    """Replaces characters '-' with '\-', and characters '.' with '\.'"""
    return re.sub(r"[-.]", lambda x: "\\" + x.group(), input_string)


def pokemon_is_galarian(pokemon_name: str, pokemon_move_1: str) -> bool:

    if pokemon_name == "Stunfisk" and (
        pokemon_move_1 == "Disparo Lodo" or pokemon_move_1 == "Garra Metal"
    ):
        return True
    if pokemon_name == "Meowth" and (
        pokemon_move_1 == "Arañazo" or pokemon_move_1 == "Garra Metal"
    ):
        return True
    if pokemon_name == "Ponyta" and (
        pokemon_move_1 == "Patada Baja" or pokemon_move_1 == "Psicocorte"
    ):
        return True
    if pokemon_name == "Rapidash" and (
        pokemon_move_1 == "Patada Baja"
        or pokemon_move_1 == "Psicocorte"
        or pokemon_move_1 == "Viento Feérico"
    ):
        return True
    if pokemon_name == "Slowpoke" and (
        pokemon_move_1 == "Confusión" or pokemon_move_1 == "Cola Férrea"
    ):
        return True
    if pokemon_name == "Slowbro" and (
        pokemon_move_1 == "Pistola Agua" or pokemon_move_1 == "Confusión"
    ):
        return True
    if pokemon_name == "Farfetch'd" and (
        pokemon_move_1 == "Corte Furia" or pokemon_move_1 == "Golpe Roca"
    ):
        return True
    if pokemon_name == "Weezing" and (
        pokemon_move_1 == "Placaje" or pokemon_move_1 == "Viento Feérico"
    ):
        return True
    if pokemon_name == "Mr-Mime" and (
        pokemon_move_1 == "Cabezazo Zen" or pokemon_move_1 == "Confusión"
    ):
        return True
    if pokemon_name == "Slowking" and (
        pokemon_move_1 == "Ácido"
        or pokemon_move_1 == "Confusión"
        or pokemon_move_1 == "Infortunio"
    ):
        return True
    if pokemon_name == "Zigzagoon" and (
        pokemon_move_1 == "Placaje" or pokemon_move_1 == "Derribo"
    ):
        return True
    if pokemon_name == "Linoone" and (
        pokemon_move_1 == "Lengüetazo" or pokemon_move_1 == "Alarido"
    ):
        return True
    if pokemon_name == "Darumaka" and (
        pokemon_move_1 == "Placaje" or pokemon_move_1 == "Colmillo Hielo"
    ):
        return True
    if pokemon_name == "Darmitan" and (
        pokemon_move_1 == "Placaje" or pokemon_move_1 == "Colmillo Hielo"
    ):
        return True
    if pokemon_name == "Yamask" and pokemon_move_1 == "Impresionar":
        return True
    if pokemon_name == "Stunfisk" and (
        pokemon_move_1 == "Disparo Lodo" or pokemon_move_1 == "Garra Metal"
    ):
        return True
    return False


def pokemon_is_alolan(pokemon_name: str, pokemon_move_1: str) -> bool:

    if pokemon_name == "Rattata" and (
        pokemon_move_1 == "Ataque Rápido" or pokemon_move_1 == "Placaje"
    ):
        return True
    if pokemon_name == "Raticate" and (
        pokemon_move_1 == "Mordisco" or pokemon_move_1 == "Ataque Rápido"
    ):
        return True
    if pokemon_name == "Raichu" and (
        pokemon_move_1 == "Impactrueno"
        or pokemon_move_1 == "Chispa"
        or pokemon_move_1 == "Voltiocambio"
    ):
        return True
    if pokemon_name == "Sandshrew" and (
        pokemon_move_1 == "Garra Metal" or pokemon_move_1 == "Nieve Polvo"
    ):
        return True
    if pokemon_name == "Sandslash" and (
        pokemon_move_1 == "Garra Metal"
        or pokemon_move_1 == "Nieve Polvo"
        or pokemon_move_1 == "Garra Umbría"
    ):
        return True
    if pokemon_name == "Vulpix" and (
        pokemon_move_1 == "Cabezazo Zen" or pokemon_move_1 == "Nieve Polvo"
    ):
        return True
    if pokemon_name == "Ninetales" and (
        pokemon_move_1 == "Finta"
        or pokemon_move_1 == "Nieve Polvo"
        or pokemon_move_1 == "Encanto"
    ):
        return True
    if pokemon_name == "Diglett" and (
        pokemon_move_1 == "Garra Metal"
        or pokemon_move_1 == "Bofetón Lodo"
        or pokemon_move_1 == "Ataque Arena"
    ):
        return True
    if pokemon_name == "Dugtrio" and (
        pokemon_move_1 == "Garra Metal"
        or pokemon_move_1 == "Bofetón Lodo"
        or pokemon_move_1 == "Ataque Arena"
    ):
        return True
    if pokemon_name == "Meowth" and (
        pokemon_move_1 == "Mordisco" or pokemon_move_1 == "Arañazo"
    ):
        return True
    if pokemon_name == "Persian" and (
        pokemon_move_1 == "Arañazo" or pokemon_move_1 == "Finta"
    ):
        return True
    if pokemon_name == "Geodude" and (
        pokemon_move_1 == "Lanzarrocas" or pokemon_move_1 == "Voltiocambio"
    ):
        return True
    if pokemon_name == "Graveler" and (
        pokemon_move_1 == "Disparo Lodo"
        or pokemon_move_1 == "Lanzarrocas"
        or pokemon_move_1 == "Bofetón Lodo"
    ):
        return True
    if pokemon_name == "Golem" and (
        pokemon_move_1 == "Disparo Lodo"
        or pokemon_move_1 == "Lanzarrocas"
        or pokemon_move_1 == "Bofetón Lodo"
    ):
        return True
    if pokemon_name == "Grimer" and (
        pokemon_move_1 == "Mordisco" or pokemon_move_1 == "Puya Nociva"
    ):
        return True
    if pokemon_name == "Muk" and (
        pokemon_move_1 == "Mordisco"
        or pokemon_move_1 == "Puya Nociva"
        or pokemon_move_1 == "Alarido"
    ):
        return True
    if pokemon_name == "Exeggutor" and (
        pokemon_move_1 == "Cola Dragón" or pokemon_move_1 == "Semilladora"
    ):
        return True
    if pokemon_name == "Marowak" and (
        pokemon_move_1 == "Golpe Roca"
        or pokemon_move_1 == "Infortunio"
        or pokemon_move_1 == "Giro Fuego"
    ):
        return True
    return False


def get_pokemon_by_name(pokedex, name):
    for pokemon in pokedex:
        if pokemon["name"].lower() == name.lower():
            return pokemon
    return None


def calculate_cost(start_lvl, end_lvl):
    stardust = CUMULATIVE_STARDUST[end_lvl] - CUMULATIVE_STARDUST[start_lvl]
    candy = CUMULATIVE_CANDY[end_lvl] - CUMULATIVE_CANDY[start_lvl]

    return {"stardust": stardust, "candy": candy}


def fetch_pvp_pokemon_data(max_cp: int):
    """Fetches PvP (Player versus Player) Pokemon data for the Great League (1500 CP cap)."""
    pvp_pokemon_list = []

    for iv in range(100, 70, -10):
        pokemons_list = fetch_pokemon_data_by_iv(iv)
        for pokemon in pokemons_list:
            pokemon_name = retrieve_pokemon_name(pokemon["pokemon_id"])
            dict_pokemon_move = retrieve_pokemon_move(pokemon["move1"], pokemon_name)
            if pokemon_is_alolan(pokemon_name, dict_pokemon_move["name"]):
                pokemon_name += " Alola"

            if pokemon_is_galarian(pokemon_name, dict_pokemon_move["name"]):
                pokemon_name += " Galar"

            with open(f"./data/dict_ranking_{max_cp}.json", "r") as file:
                rankings_data = json.load(file)
            first_rank = rankings_data.get(pokemon_name)
            if not first_rank:
                first_rank = null_rank
            if (
                pokemon["attack"] == first_rank["attackStat"]
                and pokemon["defence"] == first_rank["defenseStat"]
                and pokemon["stamina"] == first_rank["healthStat"]
            ):
                pokemon_dict = {
                    "pokemon": pokemon,
                    "ranking": first_rank,
                    "iv": iv,
                }
                pvp_pokemon_list.append(pokemon_dict)

    return pvp_pokemon_list


def league_signature(max_cp: int):
    if max_cp == 1500:
        return "🅶🅻"
    elif max_cp == 2500:
        return "🆄🅻"
    else:
        return "🅼🅻"


def generate_pvp_pokemon_messages(max_cp: int):
    """Retrieves Pokemon data, formats it into messages, and returns a list of formatted messages ready to be sent."""
    try:
        total_message = []
        total_data = fetch_pvp_pokemon_data(max_cp)
        if total_data != []:
            message_delay = 3 if len(total_data) > 18 else 2
            for data in total_data:
                delay = (
                    1
                    + coordinates_waiting_time(len(total_data))
                    + message_delay * total_data.index(data)
                )
                dsp = calculate_remaining_time(data["pokemon"]["despawn"], delay)
                if dsp:
                    pokemon_name = escape_string(
                        retrieve_pokemon_name(data["pokemon"]["pokemon_id"]).title()
                    )
                    iv_number = data["iv"]
                    cp = data["pokemon"]["cp"]
                    level = data["pokemon"]["level"]
                    shiny_icon = "✨" if data["pokemon"]["shiny"] == 0 else ""
                    latitude = data["pokemon"]["lat"]
                    longitude = data["pokemon"]["lng"]
                    flag = data["pokemon"]["flag"]
                    move1 = escape_string(
                        retrieve_pokemon_move(data["pokemon"]["move1"], pokemon_name)[
                            "name"
                        ]
                    )
                    move2 = escape_string(
                        retrieve_pokemon_move(data["pokemon"]["move2"], pokemon_name)[
                            "name"
                        ]
                    )
                    move1_icon = retrieve_pokemon_move(
                        data["pokemon"]["move1"], pokemon_name
                    )["icon"]
                    move2_icon = retrieve_pokemon_move(
                        data["pokemon"]["move2"], pokemon_name
                    )["icon"]
                    height = escape_string(
                        retrieve_pokemon_height(data["pokemon"]["pokemon_id"])
                    )
                    weight = escape_string(
                        retrieve_pokemon_weight(data["pokemon"]["pokemon_id"])
                    )
                    pokemon_id = data["pokemon"]["pokemon_id"]
                    cp_pvp_pokemon = data["ranking"]["cp"]
                    level_pvp_pokemon = escape_string(str(data["ranking"]["level"]))
                    gender_icon = "♂️" if data["pokemon"]["gender"] == 1 else "♀️"
                    candy = calculate_cost(
                        data["pokemon"]["level"], data["ranking"]["level"]
                    )["candy"]
                    stardust = calculate_cost(
                        data["pokemon"]["level"], data["ranking"]["level"]
                    )["stardust"]
                    league = league_signature(max_cp)
                    formatted_message = (
                        f"*{pokemon_name}* {gender_icon}{shiny_icon} ⌚\({dsp}\)\n"
                        f"IV:{iv_number} CP:{cp} LV:{level}\n"
                        f"⚖️{weight}kg 📏{height}m\n"
                        f"{move1_icon}{move1} \| {move2_icon}{move2}\n"
                        f"                     ▼\n"
                        f"\#0{pokemon_id} \- *{pokemon_name}* {league}\n"
                        f"🅡1 CP:{cp_pvp_pokemon} LV:{level_pvp_pokemon}\n"
                        f"⚗️{stardust} 🍬{candy}\n"
                        f"☄️🥊🄰🄴 ᴘᴠᴘ ᴛᴏᴘ ɢᴀʟᴀxʏ🏆🌀\n"
                        f"{flag}\n"
                        f"`{latitude},{longitude}`"
                    )
                    total_message.append(formatted_message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        logging.error(traceback.format_exc())
        return None
    return total_message


def calculate_cp(attack, defense, health, level_constant):
    try:
        value = attack * (defense * health) ** 0.5 * level_constant**2
        return 10 if value < 100 else int(value / 10)
    except Exception as e:
        # Handle the error appropriately
        print(f"An error occurred while calculating CP: {e}")
        return None


def calculate_products(
    pokedex_entry: Dict[str, int],
    attack_stat: int,
    defense_stat: int,
    health_stat: int,
    level_constant: int,
) -> Dict[str, int]:
    try:
        base_attack = pokedex_entry["baseAttack"]
        base_defense = pokedex_entry["baseDefense"]
        base_health = pokedex_entry["baseHealth"]

        attack_product = (base_attack + attack_stat) * level_constant
        defense_product = (base_defense + defense_stat) * level_constant
        health_product = floor((base_health + health_stat) * level_constant)
        product = attack_product * defense_product * health_product

        cp = calculate_cp(
            base_attack + attack_stat,
            base_defense + defense_stat,
            base_health + health_stat,
            level_constant,
        )

        return {
            "attackProduct": attack_product,
            "defenseProduct": defense_product,
            "healthProduct": health_product,
            "product": product,
            "cp": cp,
        }
    except KeyError as e:
        # Handle the KeyError (missing key in pokedex_entry)
        print(f"KeyError: {e} not found in pokedex_entry")
        return None
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred while calculating products: {e}")
        return None


def level_to_index(level_request: Dict[str, int]) -> int:
    return (level_request["level"] - 1) * 2


def index_to_level(index_request: Dict[str, int]) -> int:
    return index_request["index"] / 2 + 1


def build_rank(
    pokedex_entry: Dict[str, int], max_cp: int, max_level: int = 40, min_stat: int = 0
) -> List[Dict[str, int]]:
    try:
        rank_entries = []
        for attack_stat in range(15, min_stat - 1, -1):
            for defense_stat in range(15, min_stat - 1, -1):
                for health_stat in range(15, min_stat - 1, -1):
                    initial_index = level_to_index({"level": max_level})
                    for level_index in range(initial_index, -1, -1):
                        products = calculate_products(
                            pokedex_entry,
                            attack_stat,
                            defense_stat,
                            health_stat,
                            level_constants[level_index],
                        )
                        if products["cp"] <= max_cp:
                            rank_entries.append(
                                {
                                    "attackStat": attack_stat,
                                    "defenseStat": defense_stat,
                                    "healthStat": health_stat,
                                    "level": index_to_level({"index": level_index}),
                                    **products,
                                }
                            )
                            break

        rank_sorted = sorted(rank_entries, key=lambda x: x["product"], reverse=True)

        # return [{"rank": index + 1, **data} for index, data in enumerate(rank_sorted)]
        if rank_sorted:
            best_rank_entry = rank_sorted[0]
            best_rank_entry["rank"] = 1
            return best_rank_entry
        else:
            return {}
    except Exception as e:
        # Handle exceptions if any
        print(f"An error occurred while building rank: {e}")
        return {}


def calculate_rank(
    pokedex_entry: Dict[str, int],
    ref_attack_stat: int,
    ref_defense_stat: int,
    ref_health_stat: int,
    max_cp: int,
    max_level: int = 40,
    minimum_stat_value: int = 0,
) -> Dict[
    str,
    Union[List[Dict[str, int]], Dict[str, Union[Dict[str, int], List[Dict[str, int]]]]],
]:
    try:
        rank = build_rank(pokedex_entry, max_cp, max_level, minimum_stat_value)
        # occurence = next(
        #     (
        #         el
        #         for el in rank
        #         if el["attackStat"] == ref_attack_stat
        #         and el["defenseStat"] == ref_defense_stat
        #         and el["healthStat"] == ref_health_stat
        #     ),
        #     None,
        # )
        return {"rank": rank}
    except ValueError as ve:
        # Handle specific exceptions
        print(f"ValueError: {ve}")
        return {"rank": null_rank}
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred while calculating rank: {e}")
        return {"rank": null_rank}


def fetch_all_pvp_pokemon_data():
    """Fetches PvP (Player versus Player) Pokemon data for the Great League."""
    pvp_pokemon_list = []

    for iv in range(100, 70, -10):
        pokemons_list = fetch_pokemon_data_by_iv(iv)
        for pokemon in pokemons_list:
            pokemon_name = retrieve_pokemon_name(pokemon["pokemon_id"])
            dict_pokemon_move = retrieve_pokemon_move(pokemon["move1"], pokemon_name)
            if pokemon_is_alolan(pokemon_name, dict_pokemon_move["name"]):
                pokemon_name += " Alola"

            if pokemon_is_galarian(pokemon_name, dict_pokemon_move["name"]):
                pokemon_name += " Galar"

            with open(f"./data/dict_ranking_1500.json", "r") as file:
                rankings_1500_data = json.load(file)

            with open(f"./data/dict_ranking_2500.json", "r") as file:
                rankings_2500_data = json.load(file)

            with open(f"./data/dict_ranking_9999.json", "r") as file:
                rankings_master_data = json.load(file)

            first_rank_1500 = rankings_1500_data.get(pokemon_name)
            first_rank_2500 = rankings_2500_data.get(pokemon_name)
            first_rank_master = rankings_master_data.get(pokemon_name)

            if not first_rank_1500:
                first_rank_1500 = null_rank

            if not first_rank_2500:
                first_rank_2500 = null_rank

            if not first_rank_master:
                first_rank_master = null_rank

            if (
                pokemon["attack"] == first_rank_1500["attackStat"]
                and pokemon["defence"] == first_rank_1500["defenseStat"]
                and pokemon["stamina"] == first_rank_1500["healthStat"]
            ):
                pokemon_dict_1500 = {
                    "pokemon": pokemon,
                    "ranking": first_rank_1500,
                    "iv": iv,
                    "max_cp": 1500,
                }
                pvp_pokemon_list.append(pokemon_dict_1500)

            if (
                pokemon["attack"] == first_rank_2500["attackStat"]
                and pokemon["defence"] == first_rank_2500["defenseStat"]
                and pokemon["stamina"] == first_rank_2500["healthStat"]
            ):
                pokemon_dict_2500 = {
                    "pokemon": pokemon,
                    "ranking": first_rank_2500,
                    "iv": iv,
                    "max_cp": 2500,
                }
                pvp_pokemon_list.append(pokemon_dict_2500)

            if (
                pokemon["attack"] == first_rank_master["attackStat"]
                and pokemon["defence"] == first_rank_master["defenseStat"]
                and pokemon["stamina"] == first_rank_master["healthStat"]
            ):
                pokemon_dict_master = {
                    "pokemon": pokemon,
                    "ranking": first_rank_master,
                    "iv": iv,
                    "max_cp": 9999,
                }
                pvp_pokemon_list.append(pokemon_dict_master)

    return pvp_pokemon_list


def generate_all_pvp_pokemon_messages():
    """Retrieves Pokemon data, formats it into messages, and returns a list of formatted messages ready to be sent."""
    try:
        total_message = []
        total_data = fetch_all_pvp_pokemon_data()
        if total_data != []:
            message_delay = 3 if len(total_data) > 18 else 2
            for data in total_data:
                delay = (
                    1
                    + coordinates_waiting_time(len(total_data))
                    + message_delay * total_data.index(data)
                )
                dsp = calculate_remaining_time(data["pokemon"]["despawn"], delay)
                if dsp:
                    pokemon_name = escape_string(
                        retrieve_pokemon_name(data["pokemon"]["pokemon_id"]).title()
                    )
                    iv_number = data["iv"]
                    cp = data["pokemon"]["cp"]
                    level = data["pokemon"]["level"]
                    shiny_icon = "✨" if data["pokemon"]["shiny"] == 0 else ""
                    latitude = data["pokemon"]["lat"]
                    longitude = data["pokemon"]["lng"]
                    flag = data["pokemon"]["flag"]
                    move1 = escape_string(
                        retrieve_pokemon_move(data["pokemon"]["move1"], pokemon_name)[
                            "name"
                        ]
                    )
                    move2 = escape_string(
                        retrieve_pokemon_move(data["pokemon"]["move2"], pokemon_name)[
                            "name"
                        ]
                    )
                    move1_icon = retrieve_pokemon_move(
                        data["pokemon"]["move1"], pokemon_name
                    )["icon"]
                    move2_icon = retrieve_pokemon_move(
                        data["pokemon"]["move2"], pokemon_name
                    )["icon"]
                    height = escape_string(
                        retrieve_pokemon_height(data["pokemon"]["pokemon_id"])
                    )
                    weight = escape_string(
                        retrieve_pokemon_weight(data["pokemon"]["pokemon_id"])
                    )
                    pokemon_id = data["pokemon"]["pokemon_id"]
                    cp_pvp_pokemon = data["ranking"]["cp"]
                    level_pvp_pokemon = escape_string(str(data["ranking"]["level"]))
                    gender_icon = "♂️" if data["pokemon"]["gender"] == 1 else "♀️"
                    candy = calculate_cost(
                        data["pokemon"]["level"], data["ranking"]["level"]
                    )["candy"]
                    stardust = calculate_cost(
                        data["pokemon"]["level"], data["ranking"]["level"]
                    )["stardust"]
                    league = league_signature(data["max_cp"])
                    formatted_message = (
                        f"*{pokemon_name}* {gender_icon}{shiny_icon} ⌚\({dsp}\)\n"
                        f"IV:{iv_number} CP:{cp} LV:{level}\n"
                        f"⚖️{weight}kg 📏{height}m\n"
                        f"{move1_icon}{move1} \| {move2_icon}{move2}\n"
                        f"                     ▼\n"
                        f"\#0{pokemon_id} \- *{pokemon_name}* {league}\n"
                        f"🅡1 CP:{cp_pvp_pokemon} LV:{level_pvp_pokemon}\n"
                        f"⚗️{stardust} 🍬{candy}\n"
                        f"☄️🥊🄰🄴 ᴘᴠᴘ ᴛᴏᴘ ɢᴀʟᴀxʏ🏆🌀\n"
                        f"{flag}\n"
                        f"`{latitude},{longitude}`"
                    )
                    total_message.append(formatted_message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        logging.error(traceback.format_exc())
        return None
    return total_message