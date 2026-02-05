"""
Configuración y constantes para la aplicación de análisis de satisfacción de Ryanair.
"""
import os

# ==================== RUTAS DE ARCHIVOS ====================
# Obtener el directorio raíz del proyecto (un nivel arriba de src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

DATA_PATHS = [
    os.path.join(DATA_DIR, 'ryanair_reviews (1).csv'),
    os.path.join(DATA_DIR, 'ryanair_reviews.csv'),
    os.path.join(os.getcwd(), 'ryanair_reviews (1).csv'),  # Fallback a directorio actual
    os.path.join(os.getcwd(), 'ryanair_reviews.csv'),
    '/mnt/user-data/uploads/ryanair_reviews__1_.csv'
]

# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
PAGE_CONFIG = {
    'page_title': 'Análisis de Satisfacción - Ryanair',
    'page_icon': '✈️',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# ==================== ASPECTOS DEL SERVICIO ====================
SERVICE_ASPECTS = [
    'Seat Comfort',
    'Cabin Staff Service',
    'Food & Beverages',
    'Ground Service',
    'Value For Money'
]

# ==================== CATEGORÍAS DE RATING ====================
RATING_THRESHOLDS = {
    'negative_max': 3,
    'neutral_max': 7,
    'positive_min': 8
}

RATING_CATEGORIES = {
    'negative': 'Negativo (1-3)',
    'neutral': 'Neutral (4-7)',
    'positive': 'Positivo (8-10)',
    'unrated': 'Sin Calificar'
}

SENTIMENT_CATEGORIES = {
    'positive': 'Positivo',
    'neutral': 'Neutral',
    'negative': 'Negativo',
    'unknown': 'Desconocido'
}

# ==================== COLORES ====================
COLORS = {
    'positive': '#28a745',
    'neutral': '#ffc107',
    'negative': '#dc3545',
    'default': '#6c757d',

    # Colores para gráficos
    'primary': 'steelblue',
    'secondary': 'coral',
    'accent': 'lightseagreen',

    # Colores para boxplot
    'boxplot': ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'plum']
}

# ==================== TEXTOS DE STORYTELLING ====================
STORY_TEXTS = {
    'Resumen Ejecutivo': (
        "Somos business intelligence: analizamos si a la gente le gusta volar con Ryanair. "
        "Aquí resumimos lo más importante: cuánta gente opinó, qué tan contentos están y qué partes del servicio necesitan arreglos."
    ),
    'Análisis Exploratorio': (
        "Miramos los datos como si fueran pistas: cuántas reseñas hay, qué notas ponen y quiénes son los que escriben."
    ),
    'Análisis Temporal': (
        "Observamos cómo cambian las opiniones con el tiempo, mes a mes y año a año. Es como ver un álbum de fotos."
    ),
    'Análisis de Calificaciones': (
        "Vemos las notas específicas y agrupamos en positivo, neutral y negativo para entender el sentimiento general."
    ),
    'Recomendaciones Estratégicas': (
        "Sugerimos acciones claras y priorizadas para aumentar la satisfacción y la recomendación de clientes."
    )
}

# ==================== MAPEO DE VERIFICACIÓN ====================
VERIFICATION_MAPPING = {
    'Trip Verified': 'Verified',
    'Verified Review': 'Verified',
    'Not Verified': 'Not Verified',
    'NotVerified': 'Not Verified',
    'Unverified': 'Not Verified'
}

# ==================== OPCIONES DE NAVEGACIÓN ====================
NAVIGATION_OPTIONS = {
    '📊 Resumen Ejecutivo': 'Resumen Ejecutivo',
    '🔎 Análisis Exploratorio': 'Análisis Exploratorio',
    '📅 Análisis Temporal': 'Análisis Temporal',
    '🌍 Análisis Geográfico': 'Análisis Geográfico',
    '⭐ Análisis de Calificaciones': 'Análisis de Calificaciones',
    '💡 Recomendaciones Estratégicas': 'Recomendaciones Estratégicas'
}

# ==================== TAMAÑOS DE FIGURAS ====================
FIGURE_SIZES = {
    'small': (10, 5),
    'medium': (12, 6),
    'large': (14, 7),
    'extra_large': (14, 6),
    'square': (10, 8)
}

# ==================== LÍMITES DE VISUALIZACIÓN ====================
TOP_N_COUNTRIES = 15
TOP_N_ROUTES = 15
MIN_REVIEWS_FOR_ROUTE_ANALYSIS = 5

# ==================== ESTILOS CSS ====================
CSS_STYLES = """
    <style>
    .main {
        background-color: white;
    }
    .stApp {
        background-color: white;
    }
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: black !important;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 14px;
        color: #6c757d;
        margin-bottom: 5px;
    }
    .insight-box {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 15px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 15px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 15px 0;
    }
    </style>
"""
