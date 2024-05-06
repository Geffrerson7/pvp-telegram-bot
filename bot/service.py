import requests, logging, re, time, json, datetime


def retrieve_flag(url:str):
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
        
    with open("data/moves.json", "r") as file:
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
    return 1.0969 * coordinates_list_size + 4.0994


def escape_string(input_string):
    """Replaces characters '-' with '\-', and characters '.' with '\.'"""
    return re.sub(r"[-.]", lambda x: "\\" + x.group(), input_string)


def signature():
    """Return admin siganture"""
    return "✍🏻•´¯•. ☆ Jσʂé Lυιʂ ☆ .•´¯•✍🏻"


def get_pokemon_evolutions(pokemon_name):
    """Retrieves the evolution chain for a given Pokemon name."""
    for i in range(1, 542):
        evolution_chain_url = f"https://pokeapi.co/api/v2/evolution-chain/{i}"
        response = requests.get(evolution_chain_url)
        if response.status_code == 200:
            evolution_names = []
            evolution_data = response.json()
            chain = evolution_data.get("chain", {})
            species_name = chain.get("species", {}).get("name", "")
            if species_name == pokemon_name and len(chain["evolves_to"]) == 1:
                current_evolution = chain
                while current_evolution:
                    species_name = current_evolution["species"]["name"]
                    evolution_names.append(species_name)
                    current_evolution = current_evolution.get("evolves_to", [])
                    if current_evolution:
                        current_evolution = current_evolution[0]
                return evolution_names[1:]
            elif species_name == pokemon_name and len(chain["evolves_to"]) > 1:
                for evolution in chain["evolves_to"]:
                    species_name_2 = evolution["species"]["name"]
                    evolution_names.append(species_name_2)
                return evolution_names
    return None


def pokemon_is_galarian(pokemon_name: str, pokemon_move_1: str) -> bool:
    
    if pokemon_name == "Stunfisk" and (pokemon_move_1 == "Disparo Lodo" or pokemon_move_1 == "Garra Metal"):
        return True
    return False


def pokemon_is_alolan(pokemon_name: str, pokemon_move_1: str) -> bool:
    
    if pokemon_name == "Rattata" and (pokemon_move_1 == "Ataque Rápido" or pokemon_move_1 == "Placaje"):
        return True
    return False


def fetch_pvp_1500_pokemon_data():
    """Fetches PvP (Player versus Player) Pokemon data for the Great League (1500 CP cap)."""
    pvp_pokemon_list = []
    with open("data/pvp1500_data.json", "r") as file:
        data = json.load(file)
    for iv in range(100, 70, -10):
        pokemons_list = fetch_pokemon_data_by_iv(iv)
        for pokemon in pokemons_list:
            pokemon_name = retrieve_pokemon_name(pokemon["pokemon_id"])
            pokemon_evolution_names = get_pokemon_evolutions(pokemon_name.lower())
            pokemon_move_first = retrieve_pokemon_move(pokemon["move1"])
            for pvp_pokemon in data:
                iv = pvp_pokemon["IV"]
                attack, defence, stamina = iv.split("/")
                if (
                    (
                        pvp_pokemon["Name"] == pokemon_name
                        or (
                            len(pokemon_evolution_names) != 0
                            and pvp_pokemon["Name"] == pokemon_evolution_names[0]
                        )
                        or (
                            len(pokemon_evolution_names) > 1
                            and pvp_pokemon["Name"] == pokemon_evolution_names[1]
                        )
                        or (
                            len(pokemon_evolution_names) > 2
                            and pvp_pokemon["Name"] == pokemon_evolution_names[2]
                        )
                        or (
                            len(pokemon_evolution_names) > 3
                            and pvp_pokemon["Name"] == pokemon_evolution_names[3]
                        )
                        or (
                            len(pokemon_evolution_names) > 4
                            and pvp_pokemon["Name"] == pokemon_evolution_names[4]
                        )
                        or (
                            len(pokemon_evolution_names) > 5
                            and pvp_pokemon["Name"] == pokemon_evolution_names[5]
                        )
                        or (
                            len(pokemon_evolution_names) > 6
                            and pvp_pokemon["Name"] == pokemon_evolution_names[6]
                        )
                        or (
                            len(pokemon_evolution_names) > 7
                            and pvp_pokemon["Name"] == pokemon_evolution_names[7]
                        )
                    )
                    and attack == pokemon["attack"]
                    and defence == pokemon["defence"]
                    and stamina == pokemon["stamina"]
                    and pvp_pokemon["Galarian"] == pokemon_is_galarian(pokemon_name, pokemon_move_first)
                    and pvp_pokemon["Alolan"] == pokemon_is_alolan(pokemon_name, pokemon_move_first)
                ):
                    # Ahora puedes acceder a los valores de pvp_pokemon
                    pokemon_dict = {
                        "pokemon": pokemon,
                        "ranking": pvp_pokemon,
                        "iv": iv,
                    }
                    pvp_pokemon_list.append(pokemon_dict)
    return pvp_pokemon_list


def generate_pvp_1500_pokemon_messages():
    """Retrieves Pokemon data, formats it into messages, and returns a list of formatted messages ready to be sent."""
    try:
        total_message = []
        total_data = fetch_pvp_1500_pokemon_data()
        if total_data != []:
            message_delay = 3 if len(total_data) > 18 else 2
            for data in total_data:
                delay = (
                    1
                    + coordinates_waiting_time(len(total_data))
                    + message_delay * total_data.index(data)
                )
                dsp = calculate_remaining_time(data["pokemon"]["despawn"], delay)
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
                    retrieve_pokemon_move(data["pokemon"]["move1"])["name"]
                )
                move2 = escape_string(
                    retrieve_pokemon_move(data["pokemon"]["move2"])["name"]
                )
                move1_icon = retrieve_pokemon_move(data["pokemon"]["move1"])["icon"]
                move2_icon = retrieve_pokemon_move(data["pokemon"]["move2"])["icon"]
                height = escape_string(
                    retrieve_pokemon_height(data["pokemon"]["pokemon_id"])
                )
                weight = escape_string(
                    retrieve_pokemon_weight(data["pokemon"]["pokemon_id"])
                )
                ranking_pvp_pokemon = data["ranking"]["#"]
                name_pvp_pokemon = data["ranking"]["Name"]
                cp_pvp_pokemon = data["ranking"]["CP"]
                level_pvp_pokemon = escape_string(data["ranking"]["Level"])
                pvp_signature = escape_string(signature())
                gender_icon = "♂️" if data["pokemon"]["gender"] == 1 else "♀️"
                formatted_message = (
                    f"*{pokemon_name}* {gender_icon}{shiny_icon} ⌚\({dsp}\)\n"
                    f"IV:{iv_number} CP:{cp} LV:{level}\n"
                    f"⚖️{weight}kg 📏{height}m\n"
                    f"{move1_icon}{move1} \| {move2_icon}{move2}\n"
                    f"                     ▼\n"
                    f"\#0{ranking_pvp_pokemon} \- *{name_pvp_pokemon}* 🅶🅻\n"
                    f"🅡1 CP:{cp_pvp_pokemon} LV:{level_pvp_pokemon}\n"
                    f"🌀🏅🄰🄴 ᴇʟᴇᴍᴇɴᴛs ᴘᴠᴘ ᴛᴏᴘ ɢᴀʟᴀxʏ🏆🌀\n"
                    f"      ˢⁿⁱᵖᵉʳ 🄰🄴 ᵉˡᵉᵐᵉⁿᵗˢ\n"
                    f" {pvp_signature}\n"
                    f"{flag}\n"
                    f"`{latitude},{longitude}`"
                )
                total_message.append(formatted_message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        return None
    return total_message
