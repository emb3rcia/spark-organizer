#reused from my spark-builder project

import json
import os
import sys
from PyQt6.QtWidgets import QMessageBox, QApplication

default_themes = {
    "dark": {
        "main_backgrounds": {
            "window_background": "#222222",
            "popup_background": "#2B2B2B",
            "panel_background": "#363636",
            "tooltip_background": "#444444"
        },

        "text": {
            "text_primary": "#FFFFFF",
            "text_secondary": "#E6E6E6",
            "text_disabled": "#A1A1A1",
            "text_inverted": "#000000",
            "text_tooltip": "#FFFFFF"
        },

        "button": {
            "button_background": "#494949",
            "button_text": "#FFFFFF",
            "button_hover": "#616161",
            "button_border": "#6D6D6D",
            "button_pressed": "#525252",
            "button_disabled": "#3D3D3D"
        },

        "input": {
            "input_background": "#919191",
            "input_text": "#FFFFFF",
            "input_border": "#6D6D6D",
            "input_placeholder": "#707070",
            "input_disabled": "#3D3D3D"
        },

        "table": {
            "table_background": "#363636",
            "table_alternate_row": "#525252",
            "table_text": "#FFFFFF",
            "table_header_background": "#363636",
            "table_header_text": "#FFFFFF",
            "table_grid": "#5A5A5A"
        },

        "highlight": {
            "highlight": "#747474",
            "highlight_text": "#FFFFFF",
            "focus_outline": "#818181"
        },
        
        "combo-box": {
            "combo-box_background": "#494949",
            "combo-box_text": "#FFFFFF",
            "combo-box_border": "#6D6D6D",
            "combo-box_hover": "#616161",
            "combo-box_dropdown_background": "#494949",
            "combo-box_disabled": "#3D3D3D"
        },

        "accent": {
            "accent_primary": "#474747",
            "accent_secondary": "#696969",
            "error": "#FF0000",
            "success": "#00FF00",
            "warning": "#FFEE00",
            "info": "#0000FF"
        },
        
        "extra": {
            "scrollbar_background": "#313131",
            "scrollbar_handle": "#505050",
            "link": "#6E6791",
            "link_hover": "#615897"
        }
    },
    "amoled": {
        "main_backgrounds": {
            "window_background": "#000000",
            "popup_background": "#000000",
            "panel_background": "#000000",
            "tooltip_background": "#000000"
        },

        "text": {
            "text_primary": "#A1A1A1",
            "text_secondary": "#DADADA",
            "text_disabled": "#838383",
            "text_inverted": "#000000",
            "text_tooltip": "#A1A1A1"
        },

        "button": {
            "button_background": "#000000",
            "button_text": "#A1A1A1",
            "button_hover": "#292929",
            "button_border": "#CACACA",
            "button_pressed": "#252525",
            "button_disabled": "#707070"
        },

        "input": {
            "input_background": "#000000",
            "input_text": "#A1A1A1",
            "input_border": "#CACACA",
            "input_placeholder": "#727272",
            "input_disabled": "#707070"
        },

        "table": {
            "table_background": "#000000",
            "table_alternate_row": "#1B1B1B",
            "table_text": "#A1A1A1",
            "table_header_background": "#000000",
            "table_header_text": "#A1A1A1",
            "table_grid": "#2E2E2E"
        },

        "highlight": {
            "highlight": "#505050",
            "highlight_text": "#FFFFFF",
            "focus_outline": "#272727"
        },
        
        "combo-box": {
            "combo-box_background": "#000000",
            "combo-box_text": "#A1A1A1",
            "combo-box_border": "#CACACA",
            "combo-box_hover": "#616161",
            "combo-box_dropdown_background": "#000000",
            "combo-box_disabled": "#707070"
        },
        
        "accent": {
            "accent_primary": "#686868",
            "accent_secondary": "#8D8D8D",
            "error": "#FF0000",
            "success": "#00FF00",
            "warning": "#FFEE00",
            "info": "#0000FF"
        },
        
        "extra": {
            "scrollbar_background": "#000000",
            "scrollbar_handle": "#303030",
            "link": "#ADADAD",
            "link_hover": "#C4C4C4"
        }
    },
    "light": {
        "main_backgrounds": {
            "window_background": "#FFFFFF",
            "popup_background": "#CCCCCC",
            "panel_background": "#CCCCCC",
            "tooltip_background": "#A7A7A7"
        },

        "text": {
            "text_primary": "#000000",
            "text_secondary": "#222222",
            "text_disabled": "#4B4B4B",
            "text_inverted": "#FFFFFF",
            "text_tooltip": "#000000"
        },

        "button": {
            "button_background": "#B6B6B6",
            "button_text": "#000000",
            "button_hover": "#919191",
            "button_border": "#6D6D6D",
            "button_pressed": "#7E7E7E",
            "button_disabled": "#C0C0C0"
        },

        "input": {
            "input_background": "#B6B6B6",
            "input_text": "#000000",
            "input_border": "#6D6D6D",
            "input_placeholder": "#5A5A5A",
            "input_disabled": "#C0C0C0"
        },

        "table": {
            "table_background": "#ACACAC",
            "table_alternate_row": "#949494",
            "table_text": "#000000",
            "table_header_background": "#949494",
            "table_header_text": "#000000",
            "table_grid": "#999999"
        },

        "highlight": {
            "highlight": "#A3A3A3",
            "highlight_text": "#000000",
            "focus_outline": "#696969"
        },
        
        "combo-box": {
            "combo-box_background": "#B6B6B6",
            "combo-box_text": "#000000",
            "combo-box_border": "#6D6D6D",
            "combo-box_hover": "#919191",
            "combo-box_dropdown_background": "#B6B6B6",
            "combo-box_disabled": "#C0C0C0"
        },
        
        "accent": {
            "accent_primary": "#686868",
            "accent_secondary": "#8D8D8D",
            "error": "#FF0000",
            "success": "#00FF00",
            "warning": "#FFEE00",
            "info": "#0000FF"
        },
        
        "extra": {
            "scrollbar_background": "#B6B6B6",
            "scrollbar_handle": "#808080",
            "link": "#403C55",
            "link_hover": "#2E2949"
        }
    }
}

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
themes_file = os.path.join(config_path, "themes.json")

def get_themes():
    if os.path.exists(themes_file):
        try:
            with open(themes_file, "r") as f:
                themes_data = json.load(f)
                return themes_data
        except json.JSONDecodeError:
            return 1
    else:
        tmp_file = themes_file + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(default_themes, f, indent=4)
        os.replace(tmp_file, themes_file)
        return default_themes.copy()

def overwrite_themes():
    tmp_file = themes_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(default_themes, f, indent=4)
    os.replace(tmp_file, themes_file)

def listThemes():
    try:
        with open(themes_file, "r") as f:
            themes_json = json.load(f)
            return list(themes_json.keys())
    except json.JSONDecodeError:
        return 1