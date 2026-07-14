import os
import json
import time
import requests
import reflex as rx
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()

RIOT_API_KEY = os.environ.get("RIOT_API_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
RIOT_HEADERS = {"X-Riot-Token": RIOT_API_KEY}
CONTINENTE = "europe"
REGION = "euw1"


def format_puntos(pts: int) -> str:
    if pts >= 1000000:
        return f"{pts / 1000000:.1f}M"
    if pts >= 1000:
        return f"{pts / 1000:.1f}K"
    return str(pts)


class State(rx.State):
    riot_name: str = ""
    riot_tag: str = ""
    display_name: str = ""
    input_text: str = ""
    messages: list[dict[str, str]] = []
    is_searching: bool = False
    is_thinking: bool = False
    summoner_ready: bool = False
    error: str = ""
    champ_analysis_skill_order: str = ""
    
    accent_color: str
    bg_glow_color: str

    historial_mensajes: list[str] = []
    indice_historial: int = 0
    top_masteries: list[dict[str, str]] = []

    show_champ_analysis: bool = False
    is_analyzing_champ: bool = False
    champ_analysis_name: str = ""
    champ_analysis_title: str = ""
    champ_analysis_image: str = ""
    champ_analysis_skills: list[dict[str, str]] = []
    champ_analysis_explanation: str = ""
    champ_analysis_build: list[dict[str, str]] = []
    champ_analysis_counters: list[dict[str, str]] = []

    _puuid: str = ""
    _match_json: str = "[]"
    _system_prompt: str = ""

    def set_theme(self, hex_color: str, glow_color: str):
        self.accent_color = hex_color
        self.bg_glow_color = glow_color

    def set_riot_name(self, value: str):
        self.riot_name = value

    def set_riot_tag(self, value: str):
        self.riot_tag = value

    def set_input_text(self, value: str):
        self.input_text = value

    def flecha_arriba(self):
        if not self.historial_mensajes:
            return
        if self.indice_historial > 0:
            self.indice_historial -= 1
            self.input_text = self.historial_mensajes[self.indice_historial]

    def flecha_abajo(self):
        if not self.historial_mensajes:
            return
        if self.indice_historial < len(self.historial_mensajes) - 1:
            self.indice_historial += 1
            self.input_text = self.historial_mensajes[self.indice_historial]
        elif self.indice_historial == len(self.historial_mensajes) - 1:
            self.indice_historial = len(self.historial_mensajes)
            self.input_text = ""

    def procesar_tecla_chat(self, key: str):
        if key == "Enter":
            yield from self.enviar_mensaje()
        elif key == "ArrowUp":
            self.flecha_arriba()
        elif key == "ArrowDown":
            self.flecha_abajo()

    def cerrar_analisis(self):
        self.show_champ_analysis = False

    def analizar_campeon(self, name: str):
        self.champ_analysis_name = name
        self.show_champ_analysis = True
        self.is_analyzing_champ = True
        self.champ_analysis_skills = []
        self.champ_analysis_explanation = ""
        self.champ_analysis_build = []
        self.champ_analysis_counters = []
        self.champ_analysis_skill_order = "" 

        try:
            resp_v = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
            version = resp_v.json()[0]
        except Exception:
            version = "14.15.1" 
            
        self.champ_analysis_image = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{name}.png"
        
        yield 

        try:
            url_champ = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{name}.json"
            resp_champ = requests.get(url_champ)
            champ_data = resp_champ.json()["data"][name]
            champ_key = champ_data["key"]

            champions = requests.get(
                f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
            ).json()["data"]

            resp_items = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json").json()
            items_data = resp_items["data"]

            mis_builds_exitosas = []
            url_match_ids = f"https://{CONTINENTE}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self._puuid}/ids?champion={champ_key}&start=0&count=10"
            resp_match_ids = requests.get(url_match_ids, headers=RIOT_HEADERS)
            
            estadisticas_champ = []
            if resp_match_ids.status_code == 200:
                match_ids = resp_match_ids.json()
                for match_id in match_ids:
                    url_match = f"https://{CONTINENTE}.api.riotgames.com/lol/match/v5/matches/{match_id}"
                    rm = requests.get(url_match, headers=RIOT_HEADERS)
                    if rm.status_code == 200:
                        datos_partida = rm.json()
                        for participante in datos_partida["info"]["participants"]:
                            if participante["puuid"] == self._puuid:
                                estadisticas_champ.append(participante)
                                if participante.get("win", False):
                                    items = [participante.get(f"item{i}", 0) for i in range(6)]
                                    valid_items = [item for item in items if item > 0]
                                    if len(valid_items) >= 4:
                                        build_traducida = []
                                        for item_id in valid_items:
                                            str_id = str(item_id)
                                            item_name = items_data[str_id]["name"] if str_id in items_data else "Unknown"
                                            build_traducida.append({"id": item_id, "name": item_name})
                                        mis_builds_exitosas.append(build_traducida)
                                break
            
            json_stats = json.dumps(estadisticas_champ) if estadisticas_champ else "[]"
            builds_str = json.dumps(mis_builds_exitosas, ensure_ascii=False)

            prompt_json = (
                f"Actúa como un Coach Challenger de {name}. Analiza mis estadísticas recientes sobre este campeón, prohibido hablar de otro, únicamente analiza este. Si es un mago no le pongas objetos AD por ejemplo, debe llevar AP\n"
                f"Tengo estas builds que YA me han funcionado en partidas ganadas: {builds_str}.\n"
                "Instrucciones:\n"
                "- NO inventes objetos. Prioriza items de mi lista de éxito.\n"
                "- Devuelve un JSON estricto con el siguiente formato exacto:\n"
                "{\n"
                '  "explicacion": "análisis táctico basado en mis partidas",\n'
                '  "runas": ["Conqueror", "Triumph", "Legend: Alacrity", "Coup de Grace", "Nimbus Cloak"],\n'
                '  "objetos": [3153, 3006, 3078, 3053, 6333, 3026],\n'
                '  "counters": ["LeeSin", "Kindred", "Nidalee"],\n'
                '  "skill_order": "Q > E > W (R siempre que esté disponible)"\n'
                "}\n"
                "- Devuelve los objetos ÚNICAMENTE como IDs numéricos oficiales de Riot.\n"
                "- Devuelve los counters usando el IDENTIFICADOR OFICIAL de Riot (LeeSin, MissFortune, MonkeyKing, TwistedFate, etc.), nunca el nombre mostrado al jugador.\n"
                "- Si un objeto no está en mi lista de éxito, solo añádelo si es totalmente imprescindible."
            )

            cliente = genai.Client(api_key=GOOGLE_API_KEY)
            respuesta = cliente.models.generate_content(
                model="gemini-3.5-flash", 
                contents=[types.Content(role="user", parts=[types.Part(text=f"Datos: {json_stats}\n{prompt_json}")])],
                config=types.GenerateContentConfig(
                    system_instruction=self._system_prompt,
                    response_mime_type="application/json",
                ),
            )
            
            datos = json.loads(respuesta.text)
            
            self.champ_analysis_explanation = datos.get("explicacion", "")
            self.champ_analysis_skill_order = datos.get("skill_order", "")

            counters = []
            for champ_id in datos.get("counters", []):
                if champ_id in champions:
                    counters.append({
                        "name": champions[champ_id]["name"],
                        "image": f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champ_id}.png"
                    })
            self.champ_analysis_counters = counters

            build_final = []
            for item in datos.get("objetos", []):
                item_id = str(item)
                if item_id in items_data:
                    build_final.append({
                        "name": items_data[item_id]["name"],
                        "image": f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{item_id}.png"
                    })
            self.champ_analysis_build = build_final

            skills_list = []
            
            if "passive" in champ_data:
                p_data = champ_data["passive"]
                p_img = p_data.get("image", {}).get("full", "")
                skills_list.append({
                    "key": "P",
                    "name": p_data.get("name", "Pasiva"),
                    "description": p_data.get("description", ""),
                    "image": f"https://ddragon.leagueoflegends.com/cdn/{version}/img/passive/{p_img}" if p_img else ""
                })
                
            teclas = ["Q", "W", "E", "R"]
            spells_data = champ_data.get("spells", [])
            for i, spell in enumerate(spells_data):
                if i < len(teclas):
                    s_img = spell.get("image", {}).get("full", "")
                    skills_list.append({
                        "key": teclas[i],
                        "name": spell.get("name", ""),
                        "description": spell.get("description", ""),
                        "image": f"https://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{s_img}" if s_img else ""
                    })
            
            self.champ_analysis_skills = skills_list

        except Exception as e:
            print(f"Error analizando campeón: {e}")
        finally:
            self.is_analyzing_champ = False
    def buscar_invocador(self):
        name = self.riot_name.strip()
        tag = self.riot_tag.strip().lstrip("#")

        if not name or not tag:
            self.error = "Introduce nombre de invocador y un tag"
            return

        self.is_searching = True
        self.error = ""
        self.summoner_ready = False
        self.show_champ_analysis = False
        self.messages = []
        self.top_masteries = []
        yield

        try:
            url_cuenta = (
                f"https://{CONTINENTE}.api.riotgames.com/riot/account/v1/"
                f"accounts/by-riot-id/{name}/{tag}"
            )
            resp_cuenta = requests.get(url_cuenta, headers=RIOT_HEADERS)

            if resp_cuenta.status_code != 200:
                self.error = (
                    f"No se encontró a {name}#{tag} "
                    f"(código {resp_cuenta.status_code})."
                )
                self.is_searching = False
                return

            puuid = resp_cuenta.json()["puuid"]

            resp_v = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
            version = resp_v.json()[0]
            
            resp_champs = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_ES/champion.json")
            champs_data = resp_champs.json()["data"]
            id_to_champ = {str(v["key"]): v["id"] for k, v in champs_data.items()}

            url_mastery = f"https://{REGION}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
            resp_mastery = requests.get(url_mastery, headers=RIOT_HEADERS)
            
            lista_m = []
            if resp_mastery.status_code == 200:
                masteries = resp_mastery.json()[:5]
                for m in masteries:
                    c_id = str(m["championId"])
                    c_name = id_to_champ.get(c_id, "Desconocido")
                    pts = format_puntos(m["championPoints"])
                    img = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{c_name}.png"
                    lista_m.append({"name": c_name, "points": pts, "image": img})
            
            self.top_masteries = lista_m

            url_partidas = (
                f"https://{CONTINENTE}.api.riotgames.com/lol/match/v5/matches/"
                f"by-puuid/{puuid}/ids?start=0&count=100&queue=420"
            )
            resp_partidas = requests.get(url_partidas, headers=RIOT_HEADERS)
            partidas = resp_partidas.json()

            if not isinstance(partidas, list):
                self.error = "No se pudieron obtener las partidas del invocador."
                self.is_searching = False
                return

            datos_json = []
            for match_id in partidas:
                url_info = f"https://{CONTINENTE}.api.riotgames.com/lol/match/v5/matches/{match_id}"
                for intento in range(4):
                    resp_match = requests.get(url_info, headers=RIOT_HEADERS)
                    if resp_match.status_code == 429:
                        espera = float(resp_match.headers.get("Retry-After", 1))
                        time.sleep(espera + 0.2)
                        continue
                    break

                datos_partida = resp_match.json()
                if "info" in datos_partida and datos_partida["info"].get("queueId") == 420:
                    datos_json.append(datos_partida)
                if len(datos_json) >= 10:
                    break

            info_maestrias = ", ".join([f"{m['name']} ({m['points']} pts)" for m in lista_m])

            system_prompt = f"""Actúa como un Coach Analista de élite de League of Legends.
                                El invocador es "{name}" (puuid: "{puuid}"). Sus mains: {info_maestrias}.
                                Busca su puuid en los 'participants' de cada partida y analiza SOLO sus datos.
                                Tono: profesional y constructivo."""

            self._puuid = puuid
            self._match_json = json.dumps(datos_json)
            self._system_prompt = system_prompt
            self.display_name = f"{name}#{tag}"
            self.summoner_ready = True
            self.is_searching = False
            self.messages = [
                {
                    "role": "assistant",
                    "content": (
                        f"Listo! Ya tengo tus rankeds analizadas y he revisado tu maestría"
                        f", {name}. Pregúntame lo que quieras."
                    ),
                }
            ]

        except Exception as e:
            self.error = f"Error al obtener datos de Riot: {e}"
            self.is_searching = False

    def enviar_mensaje(self):
        pregunta = self.input_text.strip()
        if not pregunta or not self.summoner_ready or self.is_thinking:
            return

        if not self.historial_mensajes or self.historial_mensajes[-1] != pregunta:
            self.historial_mensajes.append(pregunta)
        self.indice_historial = len(self.historial_mensajes)

        self.messages.append({"role": "user", "content": pregunta})
        self.input_text = ""
        self.is_thinking = True
        yield

        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=f"JSON de partidas generales:\n{self._match_json}")]
            ),
            types.Content(
                role="model",
                parts=[types.Part(text="Entendido.")]
            ),
        ]
        for m in self.messages:
            rol = "user" if m["role"] == "user" else "model"
            contents.append(types.Content(role=rol, parts=[types.Part(text=m["content"])]))

        try:
            cliente = genai.Client(api_key=GOOGLE_API_KEY)
            respuesta = cliente.models.generate_content(
                model="gemini-3.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self._system_prompt,
                ),
            )
            texto = respuesta.text
        except Exception:
            texto = f"Espera un momento antes de continuar con el análisis. Disculpa las molestias, nuestros servidores están experimentando una alta carga de trabajo."

        self.messages.append({"role": "assistant", "content": texto})
        self.is_thinking = False

    def nueva_busqueda(self):
        self.summoner_ready = False
        self.show_champ_analysis = False
        self.messages = []
        self.top_masteries = []
        self.error = ""
        self.riot_name = ""
        self.riot_tag = ""