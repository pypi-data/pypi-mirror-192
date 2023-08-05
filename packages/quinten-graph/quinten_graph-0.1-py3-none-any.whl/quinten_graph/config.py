# Here you should define all your constant variable that are parameters of your whole project
# like paths to data, list of expected files for checks, information to connect to mail server etc.
# please see wiki here https://confluence.par.quinten.io/pages/viewpage.action?pageId=43102811


import logging

# ===================================================
# LOGS
# ===================================================
PATH_LOG_FILE = "../logs"
LOG_LEVEL = logging.INFO

PATH_PROJECT = "C:/Users/vvincentelli/projets/Quinten graph/quinten_graph"

PATH_DATASETCHURN = "../data/datasetchurn.csv"

# palettes of entities
dic_quinten_colors = {
    "finance": [
        "#2C3347",  # bleu-gris fonce
        "#4D5B86",  # bleu-gris moyen
        "#8D99BE",  # bleu-gris clair
        "#455B60",  # vert_gris fonce
        "#7A9FA9",  # vert_gris moyen
        "#CBE2E3",  # vert-gris clair
        "#BDAA70",  # marron moyen
        "#E5DDC6",  # marron clair
        "#C9584A",  # rouge moyen
        "#FF9691",  # rouge clair
        "#B0B0B0",  # gris moyen
        "#D7D7D7",  # gris clair
    ],
    "health": None,
    "academy": None,
    "holding": None,
}

dic_quinten_linear_colors = {
    "finance": [
        "#D7D7D7",  # gris clair (valeur basse)
        "#2C3347",  # bleu-gris fonce (valeur haute)
    ],
    "health": None,
    "academy": None,
    "holding": None,
}

dic_rc_params = dict(
    figsize=(10, 6),
    axes_titlesize=25,
    axes_labelsize=20,
    lines_linewidth=3,
    lines_markersize=150,
    xtick_labelsize=15,
    ytick_labelsize=15,
    font_family="Arial",
)
