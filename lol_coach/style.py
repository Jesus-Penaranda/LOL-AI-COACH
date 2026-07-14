BG_DARK = "#0A0F16"
BG_DARKER = "#060A0F"
PANEL_BG = "rgba(18, 26, 38, 0.72)"
PANEL_BORDER = "rgba(200, 170, 110, 0.35)"
GOLD = "#C8AA6E"
GOLD_BRIGHT = "#F0E6D2"
TEXT_MAIN = "#E7E3DA"
TEXT_DIM = "#A0A8B4"
DANGER = "#E84057"

FONT = "'Poppins', 'Segoe UI', sans-serif"

ANIMATIONS_CSS = """
<style>
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(35px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
@keyframes slideInRight {
    0% { opacity: 0; transform: translateX(35px); }
    100% { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    0% { opacity: 0; transform: translateX(-35px); }
    100% { opacity: 1; transform: translateX(0); }
}
@keyframes hexPulse {
    0% { opacity: 0.08; transform: scale(1); }
    50% { opacity: 0.16; transform: scale(1.03); }
    100% { opacity: 0.08; transform: scale(1); }
}
@keyframes goldGlow {
    0% { box-shadow: 0 0 5px rgba(200, 170, 110, 0.1); }
    50% { box-shadow: 0 0 25px rgba(200, 170, 110, 0.4); }
    100% { box-shadow: 0 0 5px rgba(200, 170, 110, 0.1); }
}
@keyframes float {
    0% { transform: translateY(0px) translateX(0px) rotate(0deg); opacity: 0; }
    20% { opacity: 0.8; }
    80% { opacity: 0.8; }
    100% { transform: translateY(-100px) translateX(20px) rotate(45deg); opacity: 0; }
}
@keyframes pulseLogo {
    0% { filter: drop-shadow(0 0 10px rgba(200, 170, 110, 0.3)); transform: scale(1); }
    50% { filter: drop-shadow(0 0 30px rgba(200, 170, 110, 0.7)); transform: scale(1.02); }
    100% { filter: drop-shadow(0 0 10px rgba(200, 170, 110, 0.3)); transform: scale(1); }
}
@keyframes pulseAvatar {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(10, 200, 185, 0.4); }
    50% { transform: scale(1.08); box-shadow: 0 0 40px rgba(10, 200, 185, 0.8); }
    100% { transform: scale(1); box-shadow: 0 0 15px rgba(10, 200, 185, 0.4); }
}
@keyframes spinRing {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@keyframes spinRingReverse {
    0% { transform: rotate(360deg); }
    100% { transform: rotate(0deg); }
}
@keyframes textGlow {
    0% { opacity: 0.7; }
    50% { opacity: 1; text-shadow: 0 0 12px rgba(200, 170, 110, 0.6); }
    100% { opacity: 0.7; }
}
</style>
"""

_HEX_SVG = (
    "data:image/svg+xml;utf8,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100' viewBox='0 0 56 100'%3E"
    "%3Cpath d='M28 0 L56 16 L56 50 L28 66 L0 50 L0 16 Z' fill='none' "
    "stroke='%23C8AA6E' stroke-width='0.7'/%3E"
    "%3Cpath d='M28 66 L56 82 L56 100 L28 100 L0 100 L0 82 Z' fill='none' "
    "stroke='%23C8AA6E' stroke-width='0.7'/%3E"
    "%3C/svg%3E"
)

HEX_PATTERN_STYLE = {
    "position": "absolute",
    "inset": "0",
    "opacity": "0.10",
    "background_image": f"url(\"{_HEX_SVG}\")",
    "background_size": "112px 200px",
    "mask_image": "radial-gradient(ellipse 80% 70% at 50% 30%, black 40%, transparent 90%)",
    "pointer_events": "none",
    "animation": "hexPulse 8s infinite ease-in-out",
    "transform_origin": "center",
}

VIGNETTE_STYLE = {
    "position": "absolute",
    "inset": "0",
    "background": "radial-gradient(ellipse 80% 60% at 50% 40%, transparent 55%, rgba(2, 4, 8, 0.65) 100%)",
    "pointer_events": "none",
}

CARD_STYLE = {
    "background": PANEL_BG,
    "border": f"1px solid {PANEL_BORDER}",
    "border_radius": "18px",
    "backdrop_filter": "blur(12px)",
    "box_shadow": "0 15px 50px rgba(0, 0, 0, 0.6)",
    "transition": "all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)",
    "_hover": {
        "transform": "translateY(-4px)",
        "box_shadow": "0 25px 60px rgba(200, 170, 110, 0.15)",
        "border": f"1px solid rgba(200, 170, 110, 0.55)",
    }
}

GOLD_BUTTON_STYLE = {
    "background": f"linear-gradient(180deg, {GOLD} 0%, #A17F3F 100%)",
    "color": "#0A0F16",
    "font_weight": "600",
    "border": "1px solid rgba(240, 230, 210, 0.4)",
    "animation": "goldGlow 4s infinite ease-in-out",
    "_hover": {
        "background": f"linear-gradient(180deg, {GOLD_BRIGHT} 0%, {GOLD} 100%)",
        "transform": "translateY(-3px) scale(1.03)",
        "box_shadow": "0 8px 25px rgba(200, 170, 110, 0.45)",
    },
    "_active": {
        "transform": "translateY(1px) scale(0.98)",
    },
    "transition": "all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1)",
}