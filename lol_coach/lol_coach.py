import reflex as rx
import random

from .state import State
from . import style


def background_layer() -> rx.Component:
    return rx.box(
        rx.box(style=style.HEX_PATTERN_STYLE),
        rx.box(style=style.VIGNETTE_STYLE),
        rx.box(
            position="absolute",
            inset="0",
            background="radial-gradient(circle at 50% 30%, " + State.bg_glow_color + ", transparent 60%)",
            transition="background 0.8s ease",
            pointer_events="none",
        ),
        position="absolute",
        inset="0",
        z_index="-1",
    )


def floating_particles() -> rx.Component:
    particles = []
    for i in range(12):
        left = f"{random.randint(10, 90)}%"
        top = f"{random.randint(40, 90)}%"
        delay = f"{random.uniform(0, 4)}s"
        duration = f"{random.uniform(3, 7)}s"
        size = f"{random.randint(2, 6)}px"
        particles.append(
            rx.box(
                width=size,
                height=size,
                background=State.accent_color,
                border_radius="50%",
                position="absolute",
                left=left,
                top=top,
                opacity="0",
                box_shadow="0 0 10px " + State.accent_color,
                animation=f"float {duration} infinite {delay} ease-in",
                pointer_events="none",
            )
        )
    return rx.box(*particles, position="absolute", inset="0", overflow="hidden", z_index="0")


def settings_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("moon", stroke_width=2.5),
                variant="ghost",
                _hover={"color": style.GOLD, "transform": "rotate(90deg)"},
                transition="all 0.3s ease",
            )
        ),
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.icon("palette", color=style.GOLD, size=24),
                    rx.text("Personalización del Coach", font_weight="bold", font_size="1.2em", color=style.TEXT_MAIN),
                    align="center",
                    spacing="2",
                ),
                rx.text("Selecciona la sintonía de tu análisis:", color=style.TEXT_DIM, margin_y="1em"),
                rx.hstack(
                    rx.button(
                        "Hextech",
                        background="rgba(200, 200, 185, 0.15)",
                        border="1px solid #0AC8B9",
                        color="#0AC8B9",
                        on_click=State.set_theme("#0AC8B9", "rgba(10, 200, 185, 0.15)"),
                        _hover={"background": "#0AC8B9", "color": "#000"},
                    ),
                    rx.button(
                        "Infernal",
                        background="rgba(232, 64, 87, 0.15)",
                        border="1px solid #E84057",
                        color="#E84057",
                        on_click=State.set_theme("#E84057", "rgba(232, 64, 87, 0.15)"),
                        _hover={"background": "#E84057", "color": "#000"},
                    ),
                    rx.button(
                        "Vacío",
                        background="rgba(157, 78, 221, 0.15)",
                        border="1px solid #9D4EDD",
                        color="#9D4EDD",
                        on_click=State.set_theme("#9D4EDD", "rgba(157, 78, 221, 0.15)"),
                        _hover={"background": "#9D4EDD", "color": "#000"},
                    ),
                    spacing="4",
                    width="100%",
                    justify="center",
                ),
                rx.dialog.close(
                    rx.button("Guardar", style=style.GOLD_BUTTON_STYLE, margin_top="1.5em", width="100%")
                ),
                padding="1em",
            ),
            background=style.PANEL_BG,
            border=f"1px solid {style.PANEL_BORDER}",
            box_shadow="0 25px 50px rgba(0,0,0,0.5)",
            border_radius="16px",
            max_width="400px",
        )
    )


def search_bar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("swords", color=style.GOLD, size=30),
            rx.text(
                "LoL Coach AI",
                font_size="2em",
                font_weight="800",
                color=style.GOLD_BRIGHT,
                letter_spacing="1.5px",
            ),
            rx.icon("swords", color=style.GOLD, size=30),
            spacing="3",
            align="center",
            animation="pulseLogo 3s infinite ease-in-out",
        ),
        rx.text(
            "Tu analista personal",
            color=style.TEXT_DIM,
            font_size="1.1em",
            margin_bottom="1em",
        ),
        rx.hstack(
            rx.icon("search", color=style.TEXT_DIM, size=20, margin_left="1em"),
            rx.input(
                placeholder="Nombre de invocador",
                value=State.riot_name,
                on_change=State.set_riot_name,
                border="none",
                background="transparent",
                color=style.TEXT_MAIN,
                font_size="1.1em",
                _placeholder={"color": style.TEXT_DIM},
                _focus={"outline": "none", "box_shadow": "none"},
                width="100%",
            ),
            rx.text("#", color=style.GOLD, font_weight="700", font_size="1.3em"),
            rx.input(
                placeholder="TAG",
                value=State.riot_tag,
                on_change=State.set_riot_tag,
                on_key_down=State.procesar_tecla_chat,
                border="none",
                background="transparent",
                color=style.TEXT_MAIN,
                font_size="1.1em",
                _placeholder={"color": style.TEXT_DIM},
                _focus={"outline": "none", "box_shadow": "none"},
                width="35%",
            ),
            rx.button(
                rx.cond(
                    State.is_searching,
                    rx.spinner(size="3", color="#0A0F16"),
                    rx.hstack(rx.icon("search", size=18), rx.text("Analizar"), spacing="2"),
                ),
                on_click=State.buscar_invocador,
                style=style.GOLD_BUTTON_STYLE,
                border_radius="12px",
                padding_x="1.5em",
                padding_y="1.2em",
                font_size="1.1em",
                is_disabled=State.is_searching,
            ),
            width="100%",
            max_width="650px",
            padding="0.5em 0.5em 0.5em 0",
            border_radius="16px",
            style=
            {
                "background": "rgba(6, 10, 16, 0.75)",
                "border": f"1px solid {style.PANEL_BORDER}",
                "transition": "all 0.35s cubic-bezier(0.2, 0.8, 0.2, 1)",
                "box_shadow": "0 10px 30px rgba(0,0,0,0.5)",
                "_focus_within": 
                {
                    "background": "rgba(10, 15, 24, 0.9)",
                    "box_shadow": f"0 0 35px rgba(200, 170, 110, 0.25)",
                    "border": f"1px solid {style.GOLD}",
                    "transform": "translateY(-3px)",
                }
            },
            align="center",
        ),
        rx.cond(
            State.error != "",
            rx.text(
                State.error, 
                color=style.DANGER, 
                font_size="1em", 
                margin_top="0.8em",
                animation="fadeIn 0.4s ease-out forwards"
            ),
        ),
        width="100%",
        align="center",
        spacing="2",
        padding_y="1.5em 1.5em",
    )


def message_bubble(msg: rx.Var) -> rx.Component:
    is_user = msg["role"] == "user"
    return rx.cond(
        is_user,
        rx.box(
            rx.box(
                rx.markdown(msg["content"], color=style.TEXT_MAIN),
                background="rgba(200, 170, 110, 0.12)",
                border=f"1px solid rgba(200, 170, 110, 0.35)",
                border_radius="16px 16px 4px 16px",
                padding="0.8em 1.1em",
                max_width="70%",
                transition="all 0.3s ease",
                _hover={
                    "background": "rgba(200, 170, 110, 0.2)",
                    "box_shadow": "0 8px 25px rgba(200, 170, 110, 0.15)",
                },
            ),
            width="100%",
            display="flex",
            justify_content="flex-end",
            padding_y="0.35em",
            animation="slideInRight 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards",
        ),
        rx.box(
            rx.hstack(
                rx.box(
                    rx.icon("bot", size=18, color=style.TEXT_MAIN),
                    background=State.accent_color,
                    border_radius="50%",
                    padding="0.4em",
                    height="fit-content",
                    flex_shrink="0",
                    box_shadow="0 0 15px " + State.accent_color,
                    transition="background 0.5s ease",
                ),
                rx.box(
                    rx.markdown(msg["content"], color=style.TEXT_MAIN),
                    background="rgba(255, 255, 255, 0.03)",
                    border=f"1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="16px 16px 16px 4px",
                    padding="0.8em 1.1em",
                    max_width="70%",
                    transition="all 0.3s ease",
                    _hover={
                        "background": "rgba(255, 255, 255, 0.06)",
                        "box_shadow": "0 8px 25px " + State.bg_glow_color,
                        "border": f"1px solid rgba(255, 255, 255, 0.2)",
                    },
                ),
                align="start",
                width="100%",
            ),
            width="100%",
            padding_y="0.35em",
            animation="slideInLeft 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards",
        ),
    )


def mastery_card(mastery: rx.Var) -> rx.Component:
    return rx.dialog.close(
        rx.box(
            rx.vstack(
                rx.image(
                    src=mastery["image"],
                    width="75px",
                    height="75px",
                    border_radius="50%",
                    border="2px solid " + State.accent_color,
                    box_shadow="0 0 15px " + State.bg_glow_color,
                    transition="all 0.4s ease",
                ),
                rx.text(mastery["name"], color=style.TEXT_MAIN, font_weight="700", font_size="1.1em", margin_top="0.5em"),
                rx.text(mastery["points"] + " pts", color=style.GOLD, font_size="0.85em", font_weight="600"),
                align="center",
                spacing="0",
            ),
            padding="1.5em",
            background="rgba(18, 26, 38, 0.7)",
            border="1px solid " + style.PANEL_BORDER,
            border_radius="20px",
            cursor="pointer",
            position="relative",
            transition="all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1)",
            on_click=lambda: State.analizar_campeon(mastery["name"]),
            _hover={
                "background": "rgba(255, 255, 255, 0.05)",
                "transform": "translateY(-8px) scale(1.03)",
                "border_color": State.accent_color,
                "box_shadow": "0 15px 35px " + State.bg_glow_color,
            }
        )
    )

def mastery_modal() -> rx.Component:
    return rx.cond(
        State.top_masteries.length() > 0,
        rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    rx.hstack(rx.icon("sparkles", size=16), rx.text("Tus Mains")),
                    variant="ghost",
                    color=State.accent_color,
                    size="2",
                    transition="all 0.2s ease",
                    _hover={"transform": "scale(1.05)", "background": "rgba(255,255,255,0.05)"},
                )
            ),
            rx.dialog.content(
                rx.vstack(
                    rx.hstack(
                        rx.icon("sparkles", color=State.accent_color, size=24),
                        rx.text(
                            "Tus Mejores Campeones",
                            color=style.TEXT_MAIN,
                            font_size="1.4em",
                            font_weight="700",
                            text_transform="uppercase",
                            letter_spacing="1.5px"
                        ),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(
                        "Haz clic en el campeón para abrir un análisis detallado del campeón", 
                        color=style.TEXT_DIM, 
                        margin_bottom="1em"
                    ),
                    rx.hstack(
                        rx.foreach(State.top_masteries, mastery_card),
                        spacing="5",
                        justify="center",
                        width="100%",
                        flex_wrap="wrap",
                        padding_top="1em"
                    ),
                    rx.dialog.close(
                        rx.button("Cerrar Panel", style=style.GOLD_BUTTON_STYLE, margin_top="2em", width="100%")
                    ),
                    align="center",
                    width="100%",
                ),
                background=style.PANEL_BG,
                border="1px solid " + style.PANEL_BORDER,
                backdrop_filter="blur(12px)",
                box_shadow="0 25px 50px rgba(0,0,0,0.6)",
                border_radius="20px",
                max_width="900px",
                padding="2.5em",
            )
        ),
        rx.box()
    )


def skill_badge(skill: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.image(src=skill["image"], width="45px", height="45px", border_radius="10px", border=f"1px solid {style.PANEL_BORDER}"),
        rx.text(skill["name"], color=style.TEXT_DIM, font_size="0.8em", font_weight="600"),
        align="center",
        spacing="1"
    )

def item_badge(item: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.cond(
            item["image"] != "",
            rx.image(src=item["image"], width="60px", height="60px", border_radius="12px", border=f"1px solid {style.GOLD}"),
            rx.box(width="60px", height="60px", background="rgba(255,255,255,0.05)", border=f"1px solid {style.PANEL_BORDER}", border_radius="12px"),
        ),
        rx.text(item["name"], color=style.TEXT_MAIN, font_size="0.8em", text_align="center", max_width="90px", font_weight="600"),
        align="center",
        spacing="2"
    )

def counter_badge(champ: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.cond(
            champ["image"] != "",
            rx.image(src=champ["image"], width="60px", height="60px", border_radius="50%", border=f"2px solid {style.DANGER}"),
            rx.box(width="60px", height="60px", border_radius="50%", background="rgba(255,255,255,0.05)", border=f"2px solid {style.DANGER}"),
        ),
        rx.text(champ["name"], color=style.TEXT_MAIN, font_size="0.9em", font_weight="700"),
        align="center",
        spacing="2"
    )


def champ_analysis_screen() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.button(
                        rx.hstack(rx.icon("arrow-left", size=18), rx.text("Volver al Chat")),
                        on_click=State.cerrar_analisis,
                        variant="ghost",
                        color=style.TEXT_DIM,
                        _hover={"color": style.TEXT_MAIN, "background": "rgba(255,255,255,0.05)"}
                    ),
                    rx.spacer(),
                    rx.icon("swords", color=State.accent_color, size=24),
                    rx.text("Análisis OTP", color=style.TEXT_MAIN, font_weight="700", font_size="1.2em", letter_spacing="1px"),
                    width="100%",
                    padding="1.5em",
                    border_bottom=f"1px solid {style.PANEL_BORDER}",
                    background="rgba(10, 15, 24, 0.7)",
                    backdrop_filter="blur(10px)"
                ),
                width="100%"
            ),
            rx.cond(
                State.is_analyzing_champ,
                rx.center(
                    rx.vstack(
                        rx.box(
                            rx.box(
                                width="160px", height="160px",
                                border_radius="50%",
                                border=f"3px dashed {State.accent_color}",
                                position="absolute",
                                animation="spinRing 8s linear infinite",
                                opacity="0.6"
                            ),
                            rx.box(
                                width="130px", height="130px",
                                border_radius="50%",
                                border=f"2px solid {style.GOLD}",
                                border_style="dotted",
                                position="absolute",
                                animation="spinRingReverse 5s linear infinite",
                                opacity="0.8"
                            ),
                            rx.image(
                                src=State.champ_analysis_image,
                                width="100px", height="100px",
                                border_radius="50%",
                                border=f"3px solid {State.accent_color}",
                                animation="pulseAvatar 2s ease-in-out infinite",
                                box_shadow=f"0 0 20px {State.accent_color}",
                            ),
                            position="relative",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            width="170px", height="170px",
                            margin_bottom="1em"
                        ),
                        rx.text(
                            f"Evaluando a {State.champ_analysis_name}...",
                            color=style.GOLD_BRIGHT,
                            font_size="1.5em",
                            font_weight="700",
                            animation="textGlow 2s infinite",
                        ),
                        spacing="4",
                        align="center"
                    ),
                    height="70vh", width="100%"
                ),
                rx.box(
                    rx.vstack(
                        rx.box(
                            rx.hstack(
                                rx.image(
                                    src=State.champ_analysis_image,
                                    width="100px", height="100px",
                                    border_radius="16px",
                                    border=f"2px solid {State.accent_color}",
                                    box_shadow=f"0 10px 25px {State.bg_glow_color}"
                                ),
                                rx.vstack(
                                    rx.text(State.champ_analysis_name, font_size="2em", font_weight="800", color=style.TEXT_MAIN, line_height="1"),
                                    rx.text(State.champ_analysis_title, font_size="1.1em", color=style.GOLD_BRIGHT, font_style="italic"),
                                    rx.hstack(
                                        rx.foreach(State.champ_analysis_skills, skill_badge),
                                        spacing="3", margin_top="0.5em"
                                    ),
                                    spacing="1",
                                    align="start"
                                ),
                                spacing="5",
                                align="center"
                            ),
                            width="100%",
                            padding="2em",
                            background="rgba(255,255,255,0.03)",
                            border_radius="20px",
                            border=f"1px solid {style.PANEL_BORDER}",
                            margin_bottom="2em"
                        ),
                        rx.box(
                            rx.hstack(rx.icon("message-square", color=State.accent_color), rx.text("Veredicto del Coach", font_weight="700", font_size="1.2em", color=style.TEXT_MAIN), spacing="2", margin_bottom="1em"),
                            rx.text(State.champ_analysis_explanation, color=style.TEXT_MAIN, line_height="1.7", font_size="1.05em"),
                            width="100%",
                            padding="2em",
                            background="rgba(10, 200, 185, 0.05)",
                            border_left=f"4px solid {State.accent_color}",
                            border_radius="0 20px 20px 0",
                            margin_bottom="2em"
                        ),
                        rx.box(
                            rx.hstack(rx.icon("anvil", color=style.GOLD), rx.text("Build Recomendada", font_weight="700", font_size="1.2em", color=style.TEXT_MAIN), spacing="2", margin_bottom="1.5em"),
                            rx.hstack(
                                rx.foreach(State.champ_analysis_build, item_badge),
                                spacing="5",
                                flex_wrap="wrap"
                            ),
                            width="100%",
                            padding="2em",
                            background="rgba(200, 170, 110, 0.05)",
                            border=f"1px solid {style.PANEL_BORDER}",
                            border_radius="20px",
                            margin_bottom="2em"
                        ),
                        rx.box(
                            rx.hstack(rx.icon("skull", color=style.DANGER), rx.text("Counters Principales", font_weight="700", font_size="1.2em", color=style.TEXT_MAIN), spacing="2", margin_bottom="1.5em"),
                            rx.hstack(
                                rx.foreach(State.champ_analysis_counters, counter_badge),
                                spacing="6",
                                flex_wrap="wrap"
                            ),
                            width="100%",
                            padding="2em",
                            background="rgba(232, 64, 87, 0.05)",
                            border=f"1px solid rgba(232, 64, 87, 0.3)",
                            border_radius="20px",
                            margin_bottom="3em"
                        ),
                        width="100%",
                        max_width="860px",
                        margin="0 auto",
                        padding_y="2em"
                    ),
                    width="100%",
                    height="calc(100vh - 80px)",
                    overflow_y="auto",
                    padding_x="1.5em",
                    style={
                        "&::-webkit-scrollbar": {"width": "6px"},
                        "&::-webkit-scrollbar-thumb": {"background": style.PANEL_BORDER, "border_radius": "6px"},
                    }
                )
            )
        ),
        width="100%",
        height="100vh",
        background="rgba(5, 8, 13, 0.95)",
        backdrop_filter="blur(15px)",
        position="absolute",
        inset="0",
        z_index="20",
        animation="fadeIn 0.4s ease-out forwards"
    )


def chat_panel() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.hstack(
                rx.icon("shield", color=style.GOLD, size=20),
                rx.text(
                    State.display_name,
                    color=style.GOLD_BRIGHT,
                    font_weight="600",
                    font_size="1.1em",
                ),
                rx.spacer(),
                mastery_modal(),
                settings_modal(),
                rx.button(
                    rx.hstack(rx.icon("refresh-cw", size=16), rx.text("Salir")),
                    on_click=State.nueva_busqueda,
                    variant="ghost",
                    color=style.TEXT_DIM,
                    size="2",
                    transition="all 0.2s ease",
                    _hover={"color": style.DANGER, "transform": "scale(1.05)"},
                ),
                width="100%",
                align="center",
            ),
            width="100%",
            padding="1em 1.6em",
            background=style.PANEL_BG,
            backdrop_filter="blur(10px)",
            border_bottom=f"1px solid {style.PANEL_BORDER}",
            flex_shrink="0",
        ),
        rx.box(
            rx.vstack(
                rx.foreach(State.messages, message_bubble),
                rx.cond(
                    State.is_thinking,
                    rx.hstack(
                        rx.spinner(size="3", color=State.accent_color),
                        rx.text(
                            "Procesando la base de datos de Riot...",
                            color=style.TEXT_DIM,
                            font_size="0.95em",
                        ),
                        padding_y="1em",
                        animation="fadeIn 0.5s ease-out forwards",
                    ),
                ),
                width="100%",
                max_width="860px",
                margin="0 auto",
                spacing="2",
            ),
            width="100%",
            flex="1",
            min_height="0",
            overflow_y="auto",
            padding="1.6em",
        ),
        rx.box(
            rx.hstack(
                rx.icon(
                    "zap",
                    size=22,
                    color=State.accent_color,
                    cursor="pointer",
                    flex_shrink="0",
                    transition="all 0.2s ease",
                    _hover={"transform": "scale(1.1)", "filter": "brightness(1.3)"},
                ),
                rx.input(
                    placeholder="Escribe tu consulta sobre la partida...",
                    value=State.input_text,
                    on_change=State.set_input_text,
                    on_key_down=State.procesar_tecla_chat,
                    border="none",
                    background="transparent",
                    color=style.TEXT_MAIN,
                    font_size="1.05em",
                    _placeholder={"color": style.TEXT_DIM},
                    _focus={"outline": "none", "box_shadow": "none"},
                    width="100%",
                    is_disabled=State.is_thinking,
                ),
                rx.button(
                    rx.icon("send", size=18, color=style.BG_DARK),
                    on_click=State.enviar_mensaje,
                    is_disabled=State.is_thinking,
                    border_radius="50%",
                    width="2.8em",
                    height="2.8em",
                    padding="0",
                    flex_shrink="0",
                    style={
                        "background": f"linear-gradient(180deg, {style.GOLD_BRIGHT} 0%, {style.GOLD} 100%)",
                        "border": "none",
                        "transition": "all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1)",
                        "_hover": {
                            "transform": "translateY(-3px) scale(1.05)",
                            "box_shadow": "0 8px 20px rgba(200, 170, 110, 0.4)",
                        },
                        "_active": {"transform": "translateY(0) scale(0.95)"},
                        "_disabled": {"opacity": "0.4", "cursor": "not-allowed", "transform": "none", "box_shadow": "none"},
                    },
                ),
                width="100%",
                max_width="860px",
                margin="0 auto",
                align="center",
                spacing="4",
                padding="0.8em 1em 0.8em 1.5em",
                border_radius="32px",
                style={
                    "background": "rgba(14, 19, 27, 0.95)",
                    "border": f"1px solid {style.PANEL_BORDER}",
                    "box_shadow": "0 15px 35px rgba(0, 0, 0, 0.55)",
                    "transition": "all 0.35s cubic-bezier(0.2, 0.8, 0.2, 1)",
                    "_focus_within": {
                        "border": f"1px solid {style.GOLD}",
                        "box_shadow": "0 20px 45px rgba(200, 170, 110, 0.25)",
                        "transform": "translateY(-3px)",
                    }
                },
            ),
            width="100%",
            display="flex",
            justify_content="center",
            padding="0 1.6em 2em",
            flex_shrink="0",
        ),
        width="100%",
        height="100%",
        spacing="0",
    )


def empty_state() -> rx.Component:
    return rx.vstack(
        rx.icon("shield", size=48, color=State.accent_color, transition="color 0.5s ease"),
        rx.text(
            "Empieza tu análisis detallado",
            color=style.TEXT_MAIN,
            font_size="1.2em",
            font_weight="600",
        ),
        rx.hstack(
            rx.box(width="8px", height="8px", border_radius="50%", background=style.GOLD, opacity="0.5"),
            rx.box(width="8px", height="8px", border_radius="50%", background=style.GOLD, opacity="0.8"),
            rx.box(width="8px", height="8px", border_radius="50%", background=style.GOLD, opacity="0.5"),
            spacing="3",
            margin_top="1em"
        ),
        align="center",
        padding_y="4em",
        spacing="3",
    )


def top_bar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.spacer(),
            settings_modal(),
            width="100%",
            padding="1.5em 2em",
            position="absolute",
            top="0",
            right="0",
            z_index="10",
        )
    )


def search_screen() -> rx.Component:
    return rx.box(
        top_bar(),
        floating_particles(),
        rx.center(
            rx.vstack(
                rx.box(
                    search_bar(),
                    animation="fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards",
                    width="100%",
                ),
                rx.box(
                    empty_state(),
                    width="100%",
                    max_width="720px",
                    style=style.CARD_STYLE,
                    animation="fadeInUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards",
                ),
                width="100%",
                max_width="800px",
                padding="2em 1em",
                align="center",
                justify="center",
                z_index="5",
                position="relative",
            ),
            width="100%",
            min_height="100vh",
        )
    )


def chat_fullscreen() -> rx.Component:
    return rx.box(
        chat_panel(),
        width="100%",
        height="100vh",
        background="rgba(5, 8, 13, 0.65)",
        backdrop_filter="blur(4px)",
        position="relative",
        z_index="1",
        animation="fadeIn 0.6s ease-out forwards",
    )


def index() -> rx.Component:
    return rx.box(
        rx.html(style.ANIMATIONS_CSS),
        background_layer(),
        rx.cond(
            State.summoner_ready,
            rx.cond(
                State.show_champ_analysis,
                champ_analysis_screen(),
                chat_fullscreen(),
            ),
            search_screen(),
        ),
        style={
            "min_height": "100vh",
            "width": "100%",
            "background": f"linear-gradient(180deg, {style.BG_DARKER} 0%, {style.BG_DARK} 40%, #0a121c 75%, #060a10 100%)",
            "font_family": style.FONT,
            "position": "relative",
            "overflow_x": "hidden",
        },
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap",
    ],
)
app.add_page(index, title="LoL Coach AI")