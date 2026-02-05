"""
Funciones utilitarias para el análisis de satisfacción de Ryanair.
"""
import pandas as pd
import os
import streamlit as st
from config import (
    DATA_PATHS, RATING_THRESHOLDS, RATING_CATEGORIES,
    SENTIMENT_CATEGORIES, VERIFICATION_MAPPING
)


@st.cache_data
def load_data(path=None):
    """
    Cargar y procesar datos desde `path` o desde ubicaciones alternativas.

    Args:
        path: Ruta del archivo CSV o objeto file-like. Si es None, busca en rutas predefinidas.

    Returns:
        DataFrame procesado o None si no se encuentra ningún archivo.

    Raises:
        FileNotFoundError: Si no se encuentra ningún archivo CSV válido.
        pd.errors.EmptyDataError: Si el archivo CSV está vacío.
    """
    possible_paths = []
    if path:
        possible_paths.append(path)
    possible_paths.extend(DATA_PATHS)

    csv_path = None
    for p in possible_paths:
        try:
            if p is None:
                continue
            if hasattr(p, 'read'):
                csv_path = p
                break
            if os.path.exists(p):
                csv_path = p
                break
        except (OSError, TypeError):
            continue

    if csv_path is None:
        return None

    # Read CSV (handle file-like objects or paths)
    try:
        if hasattr(csv_path, 'read'):
            df = pd.read_csv(csv_path)
        else:
            df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        st.error("El archivo CSV está vacío.")
        return None
    except Exception as e:
        st.error(f"Error al leer el archivo CSV: {str(e)}")
        return None

    # Validar columnas necesarias
    required_columns = ['Date Published', 'Overall Rating']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Faltan columnas requeridas: {', '.join(missing_columns)}")
        return None

    # Convertir fechas
    df['Date Published'] = pd.to_datetime(df.get('Date Published', pd.NaT), errors='coerce')
    df['Date Flown'] = pd.to_datetime(df.get('Date Flown', pd.NaT), errors='coerce')

    # Crear variables temporales
    df['Year_Published'] = df['Date Published'].dt.year
    df['Month_Published'] = df['Date Published'].dt.to_period('M').astype(str)
    df['Year_Flown'] = df['Date Flown'].dt.year

    # Procesar recomendaciones: normalizar a minúsculas y mapear a 1/0
    df['Recommended'] = df.get('Recommended', pd.Series()).fillna('').astype(str).str.strip().str.lower()
    df['Recommended_bool'] = df['Recommended'].map({'yes': 1, 'no': 0})

    # Clasificar por rating
    df['Rating_Category'] = df['Overall Rating'].apply(classify_rating)

    # Limpiar verificación
    df['Trip_verified_clean'] = df.get('Trip_verified', pd.Series()).fillna('Unknown')
    df['Trip_verified_clean'] = df['Trip_verified_clean'].replace(VERIFICATION_MAPPING)

    # Crear columna 'Sentiment'
    df['Sentiment'] = df['Overall Rating'].apply(sentiment_from_rating)

    # Crear columna 'Route' (Origin → Destination)
    if 'Origin' in df.columns and 'Destination' in df.columns:
        df['Route'] = df['Origin'].fillna('Unknown') + ' → ' + df['Destination'].fillna('Unknown')

    return df


def classify_rating(rating):
    """
    Clasificar una calificación en categorías (Positivo, Neutral, Negativo).

    Args:
        rating: Calificación numérica (1-10).

    Returns:
        str: Categoría de la calificación.
    """
    if pd.isna(rating):
        return RATING_CATEGORIES['unrated']

    try:
        r = float(rating)
    except (ValueError, TypeError):
        return RATING_CATEGORIES['unrated']

    if r <= RATING_THRESHOLDS['negative_max']:
        return RATING_CATEGORIES['negative']
    elif r <= RATING_THRESHOLDS['neutral_max']:
        return RATING_CATEGORIES['neutral']
    else:
        return RATING_CATEGORIES['positive']


def sentiment_from_rating(rating):
    """
    Obtener sentimiento desde una calificación.

    Args:
        rating: Calificación numérica (1-10).

    Returns:
        str: Sentimiento (Positivo, Neutral, Negativo, Desconocido).
    """
    if pd.isna(rating):
        return SENTIMENT_CATEGORIES['unknown']

    try:
        r = float(rating)
    except (ValueError, TypeError):
        return SENTIMENT_CATEGORIES['unknown']

    if r <= RATING_THRESHOLDS['negative_max']:
        return SENTIMENT_CATEGORIES['negative']
    elif r <= RATING_THRESHOLDS['neutral_max']:
        return SENTIMENT_CATEGORIES['neutral']
    else:
        return SENTIMENT_CATEGORIES['positive']


def calculate_recommendation_rate(df):
    """
    Calcular tasa de recomendación.

    Args:
        df: DataFrame con columna 'Recommended_bool'.

    Returns:
        float: Tasa de recomendación en porcentaje.
    """
    if 'Recommended_bool' not in df.columns:
        return 0.0

    valid_count = df['Recommended_bool'].notna().sum()
    if valid_count == 0:
        return 0.0

    return (df['Recommended_bool'].sum() / valid_count) * 100


def calculate_nps(df):
    """
    Calcular Net Promoter Score (NPS) aproximado.

    Args:
        df: DataFrame con columna 'Sentiment'.

    Returns:
        float: NPS aproximado.
    """
    if 'Sentiment' not in df.columns or len(df) == 0:
        return 0.0

    n_positive = (df['Sentiment'] == SENTIMENT_CATEGORIES['positive']).sum()
    n_negative = (df['Sentiment'] == SENTIMENT_CATEGORIES['negative']).sum()

    return ((n_positive - n_negative) / len(df)) * 100


def create_metric_card(label, value, delta=None):
    """
    Crear tarjeta de métrica personalizada (HTML).

    Args:
        label: Etiqueta de la métrica.
        value: Valor de la métrica.
        delta: Cambio porcentual (opcional).

    Returns:
        str: HTML para la tarjeta de métrica.
    """
    if delta is not None:
        change_color = 'green' if delta > 0 else 'red'
        delta_html = f"<div style='color:{change_color}; font-size:14px;'>{delta:+.1f}%</div>"
    else:
        delta_html = ""

    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def display_story(page_key: str):
    """
    Muestra un texto de storytelling para una página.

    Args:
        page_key: Clave de la página.
    """
    from config import STORY_TEXTS
    text = STORY_TEXTS.get(page_key)
    if text:
        st.info(text)


def apply_filters(df, date_range, verification_filter):
    """
    Aplicar filtros al DataFrame.

    Args:
        df: DataFrame original.
        date_range: Tupla con rango de fechas.
        verification_filter: Lista con valores de verificación a incluir.

    Returns:
        DataFrame filtrado.
    """
    if len(date_range) == 2:
        mask = (
            (df['Date Published'] >= pd.to_datetime(date_range[0])) &
            (df['Date Published'] <= pd.to_datetime(date_range[1])) &
            (df['Trip_verified_clean'].isin(verification_filter))
        )
        return df[mask]
    else:
        return df[df['Trip_verified_clean'].isin(verification_filter)]


def format_large_number(num):
    """
    Formatear números grandes con separadores de miles.

    Args:
        num: Número a formatear.

    Returns:
        str: Número formateado.
    """
    try:
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return str(num)
