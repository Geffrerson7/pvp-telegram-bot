import requests, logging, re, time
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_pokemon_data():
    try:

        url = "https://moonani.com/PokeList/pvp.php"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"id": "customers"})
            data_list = []

            if table:
                for row in table.find_all("tr")[1:]:
                    cells = row.find_all("td")
                    if len(cells) > 0:
                        data = {
                            "Name": cells[1].text.strip(),
                            "CP": cells[4].text.strip(),
                            "Level": cells[5].text.strip(),
                            "Shiny": cells[11].text.strip(),
                            "Start Time": cells[13].text.strip(),
                            "End Time": cells[14].text.strip(),
                            "Coords": cells[3].text.strip(),
                        }
                        data_list.append(data)

                # Ordenar los datos por "End Time" en orden descendente
                data_list.sort(key=lambda x: x["End Time"], reverse=True)
            else:
                print("Error: No se encontró la tabla de datos en la página web.")
        else:
            print(f"Error: Respuesta inesperada del servidor ({response.status_code})")

        return data_list

    except Exception as e:
        print(f"Error: {e}")
        return []


def calculate_time(time):
    new_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return new_time


def coordinates_waiting_time(coordinates_list_size):
    """Obtains the excecution time of fetch_pokemon_data() function"""
    return 1.0969 * coordinates_list_size + 4.0994


def escape_string(input_string):
    """Replaces characters '-' with '\-', and characters '.' with '\.' """
    return re.sub(r"[-.]", lambda x: "\\" + x.group(), input_string)


def generate_pokemon_messages():
    try:
        total_message = []
        total_data = fetch_pokemon_data()
        if total_data != []:
            for data in total_data:
                name = escape_string(data['Name'])
                start_time = calculate_time(data["Start Time"])
                end_time = calculate_time(data["End Time"])
                shiny_icon = "✨" if data["Shiny"].lower() == "yes" else ""
                formatted_message = (
                    f"🅐 {name}{shiny_icon}\n"
                    f"🅔🛡L{data['Level']} CP {data['CP']}\n"
                    f"🌀🏅🄰🄴 ᴘᴠᴘ ᴛᴏᴘ ɢᴀʟᴀxʏ🥊🌀\n"
                    f"⌚sᴛᴀʀᴛ ᴛɪᴍᴇ\n"
                    f"`{start_time}`\n"
                    f"⌚ᴇɴᴅ ᴛɪᴍᴇ\n"
                    f"`{end_time}`\n"
                    f"`{data['Coords']}`"
                )
                total_message.append(formatted_message)
        else:
            logging.error("Pokemons not found")
    except Exception as e:
        logging.error(f"Error sending Pokemon data: {e}")
        return None
    return total_message


def test_generate_pokemon_messages():
    start_time = time.time()  
    generate_pokemon_messages()  
    end_time = time.time()  

    execution_time = end_time - start_time 
    return execution_time
