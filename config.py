"""Настройки проекта"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "databases", "db_variant_16.db")
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

COMPANY_NAME = "Ал.Недвижимость"
APP_TITLE = f"Система заказа — {COMPANY_NAME}"

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700


FONT_FAMILY = "Calibri"


COLOR_MAIN_BG = "#FFFFFF"        
COLOR_SECONDARY_BG = "#D2F6E7"   
COLOR_ACCENT = "#70B2AF"         
COLOR_HIGHLIGHT = "#ff8080"      

HIGHLIGHT_THRESHOLD = 3         
INDICATOR_THRESHOLD = 5          
DISCOUNT_AREA_THRESHOLD = 100    
DISCOUNT_PERCENT = 5      