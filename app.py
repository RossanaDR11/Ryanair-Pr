import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importar configuración y utilidades
from config import (
    PAGE_CONFIG, CSS_STYLES, SERVICE_ASPECTS, COLORS,
    NAVIGATION_OPTIONS, FIGURE_SIZES,
    TOP_N_COUNTRIES, TOP_N_ROUTES, MIN_REVIEWS_FOR_ROUTE_ANALYSIS
)
from utils import (
    load_data, calculate_recommendation_rate, calculate_nps,
    create_metric_card, display_story, apply_filters
)

# Configuración de la página
st.set_page_config(**PAGE_CONFIG)

# Estilo CSS personalizado
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Funciones load_data, create_metric_card y display_story ahora están en utils.py


def show_executive_summary(df):
    """Resumen Ejecutivo para CEO"""
    st.title("Resumen Ejecutivo: Análisis de Satisfacción del Cliente Ryanair")
    st.markdown("### Informe para la Dirección Ejecutiva")
    display_story('Resumen Ejecutivo')
    st.markdown("---")
    
    # KPIs principales
    st.markdown("## Indicadores Clave de Rendimiento")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_rating = df['Overall Rating'].mean()
        st.markdown(create_metric_card(
            "Calificación Promedio",
            f"{avg_rating:.1f}/10"
        ), unsafe_allow_html=True)
    
    with col2:
        rec_rate = calculate_recommendation_rate(df)
        st.markdown(create_metric_card(
            "Tasa de Recomendación",
            f"{rec_rate:.1f}%"
        ), unsafe_allow_html=True)
    
    with col3:
        total_reviews = len(df)
        st.markdown(create_metric_card(
            "Total de Reseñas",
            f"{total_reviews:,}"
        ), unsafe_allow_html=True)
    
    with col4:
        verified_pct = (df['Trip_verified_clean'] == 'Verified').sum() / len(df) * 100
        st.markdown(create_metric_card(
            "Reseñas Verificadas",
            f"{verified_pct:.1f}%"
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Análisis de sentimiento general
    st.markdown("## Distribución de Satisfacción")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de distribución
        fig, ax = plt.subplots(figsize=(10, 5))
        rating_dist = df['Rating_Category'].value_counts()
        colors = {'Positivo (8-10)': COLORS['positive'], 'Neutral (4-7)': COLORS['neutral'], 'Negativo (1-3)': COLORS['negative']}
        rating_dist.plot(kind='bar', color=[colors.get(x, '#6c757d') for x in rating_dist.index], ax=ax)
        ax.set_title('Distribución de Calificaciones por Categoría', fontsize=14, fontweight='bold', color='black')
        ax.set_xlabel('Categoría de Calificación', fontsize=11, color='black')
        ax.set_ylabel('Número de Reseñas', fontsize=11, color='black')
        ax.tick_params(colors='black')
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### Distribución Porcentual")
        for category in ['Positivo (8-10)', 'Neutral (4-7)', 'Negativo (1-3)']:
            count = (df['Rating_Category'] == category).sum()
            pct = (count / len(df)) * 100
            st.markdown(f"**{category}**")
            st.progress(pct / 100)
            st.markdown(f"{pct:.1f}% ({count:,} reseñas)")
            st.markdown("")
    
    st.markdown("---")
    
    # Aspectos del servicio
    st.markdown("## Evaluación por Aspectos del Servicio")
    
    service_aspects = SERVICE_ASPECTS
    aspect_means = df[service_aspects].mean().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.RdYlGn(aspect_means.values / 5)
    bars = ax.barh(aspect_means.index, aspect_means.values, color=colors)
    ax.set_title('Calificación Promedio por Aspecto del Servicio (Escala 1-5)', 
                 fontsize=14, fontweight='bold', color='black')
    ax.set_xlabel('Calificación Promedio', fontsize=11, color='black')
    ax.set_ylabel('Aspecto del Servicio', fontsize=11, color='black')
    ax.tick_params(colors='black')
    ax.axvline(x=3, color='gray', linestyle='--', alpha=0.5, label='Punto Medio (3.0)')
    ax.grid(axis='x', alpha=0.3)
    ax.legend()
    
    # Agregar valores en las barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', ha='left', va='center', fontsize=10, color='black')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.markdown("---")
    
    # Hallazgos clave
    st.markdown("## Hallazgos Clave")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### Puntos Fuertes")
        best_aspect = aspect_means.idxmax()
        best_score = aspect_means.max()
        st.markdown(f"""
        - **{best_aspect}** lidera con {best_score:.2f}/5.0
        - {rec_rate:.1f}% de los clientes recomiendan el servicio
        - {verified_pct:.1f}% de reseñas están verificadas, indicando credibilidad
        - La calificación promedio general es {avg_rating:.1f}/10
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("### Áreas de Mejora")
        worst_aspect = aspect_means.idxmin()
        worst_score = aspect_means.min()
        negative_pct = ((df['Rating_Category'] == 'Negativo (1-3)').sum() / len(df)) * 100
        st.markdown(f"""
        - **{worst_aspect}** tiene la calificación más baja: {worst_score:.2f}/5.0
        - {negative_pct:.1f}% de las reseñas son negativas (1-3)
        - {100-rec_rate:.1f}% de clientes NO recomiendan el servicio
        - Oportunidad significativa de mejora en experiencia del cliente
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Conclusión ejecutiva
    st.markdown("## Conclusión Ejecutiva")
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown(f"""
    El análisis de {len(df):,} reseñas de clientes revela un **panorama mixto** en la satisfacción del cliente de Ryanair:
    
    **Situación Actual:**
    - La calificación promedio de **{avg_rating:.1f}/10** sugiere una experiencia de cliente por debajo de lo óptimo
    - Con una tasa de recomendación del **{rec_rate:.1f}%**, existe una oportunidad significativa de mejora
    - El aspecto mejor valorado es **{aspect_means.idxmax()}** ({aspect_means.max():.2f}/5.0)
    - El aspecto que requiere atención urgente es **{aspect_means.idxmin()}** ({aspect_means.min():.2f}/5.0)
    
    **Implicaciones Estratégicas:**
    - Existe potencial para convertir clientes neutrales/negativos en promotores
    - La mejora en aspectos críticos del servicio puede incrementar significativamente la lealtad
    - Se recomienda priorizar inversiones en las áreas de menor puntuación
    
    **Recomendación Principal:**
    Implementar un plan de acción integral centrado en mejorar {worst_aspect.lower()} y la experiencia general del cliente, 
    con el objetivo de aumentar la tasa de recomendación al 50% en los próximos 12 meses.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def show_eda(df):
    """Análisis Exploratorio de Datos"""
    st.title("Análisis Exploratorio de Datos (EDA)")
    st.markdown("### Exploración Detallada del Dataset")
    display_story('Análisis Exploratorio')
    st.markdown("---")
    
    # Información general
    st.markdown("## Información General del Dataset")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Registros", f"{len(df):,}")
    with col2:
        st.metric("Columnas", f"{df.shape[1]}")
    with col3:
        st.metric("Período", f"{df['Date Published'].min().strftime('%Y-%m')} a {df['Date Published'].max().strftime('%Y-%m')}")
    
    st.markdown("---")
    
    # Distribución de calificaciones
    st.markdown("## Distribución de Calificaciones Generales")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        rating_counts = df['Overall Rating'].value_counts().sort_index()
        bars = ax.bar(rating_counts.index, rating_counts.values, color='steelblue', edgecolor='black')
        ax.set_title('Distribución de Calificaciones Generales (1-10)', 
                     fontsize=14, fontweight='bold', color='black')
        ax.set_xlabel('Calificación', fontsize=11, color='black')
        ax.set_ylabel('Número de Reseñas', fontsize=11, color='black')
        ax.tick_params(colors='black')
        ax.grid(axis='y', alpha=0.3)
        
        # Agregar valores en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9, color='black')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### Estadísticas")
        st.markdown(f"**Media:** {df['Overall Rating'].mean():.2f}")
        st.markdown(f"**Mediana:** {df['Overall Rating'].median():.2f}")
        st.markdown(f"**Moda:** {df['Overall Rating'].mode()[0]:.0f}")
        st.markdown(f"**Desv. Estándar:** {df['Overall Rating'].std():.2f}")
        st.markdown(f"**Mínimo:** {df['Overall Rating'].min():.0f}")
        st.markdown(f"**Máximo:** {df['Overall Rating'].max():.0f}")
        
        st.markdown("### Percentiles")
        st.markdown(f"**25%:** {df['Overall Rating'].quantile(0.25):.1f}")
        st.markdown(f"**50%:** {df['Overall Rating'].quantile(0.50):.1f}")
        st.markdown(f"**75%:** {df['Overall Rating'].quantile(0.75):.1f}")

    # Valores resumidos e interpretación (según notebook)
    avg_overall = df['Overall Rating'].mean()
    rec_rate_approx = calculate_recommendation_rate(df)
    st.markdown('**Valores resumidos:**')
    st.markdown(f'- **Calificación promedio (Overall Rating):** {avg_overall:.2f} / 10')
    st.markdown(f'- **Tasa de recomendación (approx.):** {rec_rate_approx:.1f}%')
    st.markdown('**Interpretación concreta:** La calificación media y la tasa de recomendación indican si una parte significativa de clientes recomendaría la aerolínea. Si la calificación y la recomendación están por debajo de niveles aceptables, prioriza intervenciones.')
    
    st.markdown("---")
    
    # Tipos de viajero
    st.markdown("## Análisis por Tipo de Viajero")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        traveller_counts = df['Type Of Traveller'].value_counts()
        colors_palette = plt.cm.Set3(range(len(traveller_counts)))
        ax.pie(traveller_counts.values, labels=traveller_counts.index, autopct='%1.1f%%',
               startangle=90, colors=colors_palette, textprops={'color': 'black'})
        ax.set_title('Distribución por Tipo de Viajero', fontsize=14, fontweight='bold', color='black')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**Interpretación - Distribución por tipo de viajero**")
        st.markdown(
            "- **Resultado observado:** muestra qué porcentaje de reseñas proviene de cada tipo de viajero.\n"
            "- **Qué buscar:** segmentos con baja satisfacción relativa (cruzar con `Overall Rating`).\n"
            "- **Significado:** si 'Viajeros Familiares' presentan menor nota, puede indicar necesidades no cubiertas (equipaje, espacio).\n"
            "- **Acción práctica:** priorizar comunicaciones y mejoras para los segmentos con peor experiencia."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Calificación promedio por tipo de viajero
        traveller_rating = df.groupby('Type Of Traveller')['Overall Rating'].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(traveller_rating.index, traveller_rating.values, color='coral')
        ax.set_title('Calificación Promedio por Tipo de Viajero', 
                     fontsize=14, fontweight='bold', color='black')
        ax.set_xlabel('Calificación Promedio', fontsize=11, color='black')
        ax.tick_params(colors='black')
        ax.grid(axis='x', alpha=0.3)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{width:.2f}', ha='left', va='center', fontsize=10, color='black')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**Interpretación - Calificación promedio por tipo de viajero**")
        st.markdown(
            "- **Resultado observado:** calificación media por tipo de viajero.\n"
            "- **Qué buscar:** tipos con promedio significativamente inferior a la media global.\n"
            "- **Significado:** un gap importante sugiere la necesidad de ajustar producto/servicio para ese segmento.\n"
            "- **Acción práctica:** diseñar acciones dirigidas (p. ej. políticas de equipaje para familias) y monitorizar su efecto."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recomendación vs Calificación
    st.markdown("## Relación entre Calificación y Recomendación")
    
    rec_by_rating = df.groupby('Overall Rating')['Recommended_bool'].agg(['sum', 'count'])
    rec_by_rating['percentage'] = (rec_by_rating['sum'] / rec_by_rating['count'] * 100)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(rec_by_rating.index, rec_by_rating['percentage'], marker='o', 
            linewidth=2, markersize=8, color='darkblue')
    ax.set_title('Porcentaje de Recomendación según Calificación General', 
                 fontsize=14, fontweight='bold', color='black')
    ax.set_xlabel('Calificación General (1-10)', fontsize=11, color='black')
    ax.set_ylabel('% que Recomienda', fontsize=11, color='black')
    ax.tick_params(colors='black')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50%')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
    **Insight:** Existe una clara correlación positiva entre la calificación general y la probabilidad de recomendación. 
    Las calificaciones superiores a 7 muestran tasas de recomendación significativamente más altas.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Matriz de correlación
    st.markdown("## Correlación entre Aspectos del Servicio")
    
    service_aspects = ['Overall Rating', 'Seat Comfort', 'Cabin Staff Service', 
                       'Food & Beverages', 'Ground Service', 'Value For Money']
    correlation_matrix = df[service_aspects].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    
    # Configurar etiquetas
    ax.set_xticks(np.arange(len(service_aspects)))
    ax.set_yticks(np.arange(len(service_aspects)))
    ax.set_xticklabels(service_aspects, rotation=45, ha='right')
    ax.set_yticklabels(service_aspects)
    ax.tick_params(colors='black')
    
    # Agregar valores de correlación
    for i in range(len(service_aspects)):
        for j in range(len(service_aspects)):
            text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                         ha="center", va="center", color="black", fontsize=10)
    
    ax.set_title('Matriz de Correlación - Aspectos del Servicio', 
                 fontsize=14, fontweight='bold', color='black', pad=20)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.tick_params(colors='black')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
    **Insight:** La correlación más fuerte con la calificación general se observa en aspectos específicos del servicio. 
    Esto indica qué factores tienen mayor impacto en la satisfacción global del cliente.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def show_temporal_analysis(df):
    """Análisis Temporal"""
    st.title("Análisis Temporal de Reseñas")
    st.markdown("### Evolución de la Satisfacción del Cliente")
    display_story('Análisis Temporal')
    st.markdown("---")
    
    # Volumen de reseñas por mes
    st.markdown("## Volumen de Reseñas a lo Largo del Tiempo")
    
    monthly_reviews = df.groupby('Month_Published').size()
    monthly_reviews.index = monthly_reviews.index.astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(range(len(monthly_reviews)), monthly_reviews.values, color='steelblue', edgecolor='black')
    ax.set_title('Número de Reseñas por Mes', fontsize=14, fontweight='bold', color='black')
    ax.set_xlabel('Mes', fontsize=11, color='black')
    ax.set_ylabel('Número de Reseñas', fontsize=11, color='black')
    ax.set_xticks(range(len(monthly_reviews)))
    ax.set_xticklabels(monthly_reviews.index, rotation=45, ha='right')
    ax.tick_params(colors='black')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.markdown("---")
    
    # Tendencia de calificaciones
    st.markdown("## Evolución de la Calificación Promedio")
    
    monthly_avg = df.groupby('Month_Published').agg({
        'Overall Rating': 'mean',
        'Recommended_bool': lambda x: (x.sum() / x.notna().sum() * 100) if x.notna().sum() > 0 else 0
    })
    monthly_avg.index = monthly_avg.index.astype(str)
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    color1 = 'darkblue'
    ax1.set_xlabel('Mes', fontsize=11, color='black')
    ax1.set_ylabel('Calificación Promedio (1-10)', fontsize=11, color=color1)
    line1 = ax1.plot(range(len(monthly_avg)), monthly_avg['Overall Rating'], 
                     color=color1, marker='o', linewidth=2, label='Calificación Promedio')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.tick_params(axis='x', colors='black')
    ax1.set_xticks(range(len(monthly_avg)))
    ax1.set_xticklabels(monthly_avg.index, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)
    
    # Segundo eje Y para tasa de recomendación
    ax2 = ax1.twinx()
    color2 = 'darkgreen'
    ax2.set_ylabel('% Recomendación', fontsize=11, color=color2)
    line2 = ax2.plot(range(len(monthly_avg)), monthly_avg['Recommended_bool'], 
                     color=color2, marker='s', linewidth=2, linestyle='--', 
                     label='% Recomendación')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Leyenda combinada
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='best')
    
    ax1.set_title('Tendencia Temporal: Calificación y Recomendación', 
                  fontsize=14, fontweight='bold', color='black')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    # Explicación sencilla después del volumen mensual
    st.markdown("**¿Qué significa esto?**")
    st.markdown(
        "La primera gráfica muestra cuántas reseñas recibimos cada mes. Un pico indica mayor actividad (por ejemplo temporada alta). "
        "Si en meses con mucho volumen la satisfacción baja, puede ser una señal de capacidad o servicio insuficiente en picos."
    )

    # Lectura de la tendencia (mover aquí desde la sección de calificaciones)
    st.markdown("**Lectura de la tendencia:**")
    st.markdown(
        "La línea azul muestra la calificación promedio mensual y la línea verde la tasa de recomendación. "
        "Si ambas suben, la experiencia mejora; si la recomendación cae mientras la nota se mantiene, puede haber problemas no capturados por la nota (por ejemplo, cargos inesperados)."
    )
    # Estadísticas agregadas globales (temporal)
    avg_rating_overall = df['Overall Rating'].mean()
    try:
        rec_rate_overall = (df['Recommended_bool'].sum() / df['Recommended_bool'].notna().sum()) * 100
    except Exception:
        rec_rate_overall = 0
    st.markdown(f"**Resumen global:** Calificación promedio **{avg_rating_overall:.2f}/10**, Tasa de recomendación **{rec_rate_overall:.1f}%**")
    
    st.markdown("---")
    
    # Análisis por año
    st.markdown("## Comparativa Anual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        yearly_avg = df.groupby('Year_Published')['Overall Rating'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(yearly_avg.index.astype(str), yearly_avg.values, 
                      color='coral', edgecolor='black')
        ax.set_title('Calificación Promedio por Año', fontsize=14, fontweight='bold', color='black')
        ax.set_xlabel('Año', fontsize=11, color='black')
        ax.set_ylabel('Calificación Promedio', fontsize=11, color='black')
        ax.tick_params(colors='black')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, 10)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col2:
        yearly_rec = df.groupby('Year_Published')['Recommended_bool'].apply(
            lambda x: (x.sum() / x.notna().sum() * 100) if x.notna().sum() > 0 else 0
        )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(yearly_rec.index.astype(str), yearly_rec.values, 
                      color='lightseagreen', edgecolor='black')
        ax.set_title('Tasa de Recomendación por Año', fontsize=14, fontweight='bold', color='black')
        ax.set_xlabel('Año', fontsize=11, color='black')
        ax.set_ylabel('% Recomendación', fontsize=11, color='black')
        ax.tick_params(colors='black')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, 100)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    st.markdown("---")
    
    # Insights temporales
    st.markdown("## Insights Temporales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("### Tendencias Identificadas")
        
        # Calcular tendencia
        recent_avg = monthly_avg['Overall Rating'].tail(3).mean()
        older_avg = monthly_avg['Overall Rating'].head(3).mean()
        trend = "al alza" if recent_avg > older_avg else "a la baja"
        
        st.markdown(f"""
        - La tendencia general de calificaciones está **{trend}**
        - Promedio últimos 3 meses: **{recent_avg:.2f}**
        - Promedio primeros 3 meses: **{older_avg:.2f}**
        - Cambio: **{((recent_avg - older_avg) / older_avg * 100):+.1f}%**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("### Puntos de Atención")
        
        # Mes con menor calificación
        worst_month = monthly_avg['Overall Rating'].idxmin()
        worst_score = monthly_avg['Overall Rating'].min()
        
        # Mes con mayor volumen
        peak_month = monthly_reviews.idxmax()
        peak_count = monthly_reviews.max()
        
        st.markdown(f"""
        - Mes con menor calificación: **{worst_month}** ({worst_score:.2f})
        - Mayor volumen de reseñas: **{peak_month}** ({peak_count} reseñas)
        - Volatilidad en calificaciones mensual: **{monthly_avg['Overall Rating'].std():.2f}**
        """)
        st.markdown('</div>', unsafe_allow_html=True)

def show_rating_analysis(df):
    """Análisis Detallado de Calificaciones"""
    st.title("Análisis Detallado de Calificaciones")
    st.markdown("### Evaluación Profunda de la Satisfacción")
    st.markdown("---")
    
    # Aspectos del servicio
    service_aspects = SERVICE_ASPECTS
    
    st.markdown("## Calificaciones por Aspecto del Servicio")
    
    # Boxplot comparativo
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Preparar datos para boxplot
    data_to_plot = [df[aspect].dropna() for aspect in service_aspects]
    
    bp = ax.boxplot(data_to_plot, labels=service_aspects, patch_artist=True,
                    showmeans=True, meanline=True)
    
    # Colorear boxes
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'plum']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')
    
    # Configurar líneas
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color='black')
    
    ax.set_title('Distribución de Calificaciones por Aspecto del Servicio (Boxplot)', 
                 fontsize=14, fontweight='bold', color='black')
    ax.set_ylabel('Calificación (1-5)', fontsize=11, color='black')
    ax.tick_params(colors='black')
    ax.grid(axis='y', alpha=0.3)
    ax.set_xticklabels(service_aspects, rotation=45, ha='right')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Explicación del boxplot (colocada en la sección correcta)
    st.markdown("**¿Qué nos indica el boxplot?**")
    st.markdown(
        "La caja (boxplot) muestra la distribución de las calificaciones por aspecto. "
        "La línea interna es la mediana y los 'bigotes' muestran la variabilidad. "
        "Si la mediana está alta y la caja es pequeña, la mayoría de clientes están satisfechos en ese aspecto."
    )
    # Valores numéricos relevantes para lectura inmediata
    total_reviews = len(df)
    avg_rating = df['Overall Rating'].mean()
    recommendation_rate = calculate_recommendation_rate(df)
    nps = calculate_nps(df)
    st.markdown(f"**KPIs rápidos:** Total: **{total_reviews:,}**, Promedio: **{avg_rating:.2f}/10**, Recomendación: **{recommendation_rate:.1f}%**, NPS aprox.: **{nps:.1f}**")
    
    st.markdown("---")
    
    # Comparación de aspectos
    st.markdown("## Comparación Detallada por Aspecto")
    
    aspect_stats = pd.DataFrame({
        'Promedio': df[service_aspects].mean(),
        'Mediana': df[service_aspects].median(),
        'Desv. Est.': df[service_aspects].std(),
        'Mínimo': df[service_aspects].min(),
        'Máximo': df[service_aspects].max()
    }).round(2)
    
    st.dataframe(aspect_stats.style.background_gradient(cmap='RdYlGn', subset=['Promedio']), 
                 use_container_width=True)
    st.markdown("**Interpretación rápida:**")
    st.markdown(
        "La tabla muestra promedios y dispersiones por aspecto. Prioriza los aspectos con menor promedio y mayor número de reseñas para mejorar impacto."
    )
    
    st.markdown("---")
    
    # Análisis por categoría de rating
    st.markdown("## Distribución de Aspectos según Categoría de Satisfacción")
    
    for category in ['Positivo (8-10)', 'Neutral (4-7)', 'Negativo (1-3)']:
        if category in df['Rating_Category'].unique():
            st.markdown(f"### {category}")
            
            df_cat = df[df['Rating_Category'] == category]
            aspect_means_cat = df_cat[service_aspects].mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(12, 5))
            
            # Determinar color según categoría
            if 'Positivo' in category:
                color = 'forestgreen'
            elif 'Neutral' in category:
                color = 'goldenrod'
            else:
                color = 'crimson'
            
            bars = ax.bar(aspect_means_cat.index, aspect_means_cat.values, 
                         color=color, alpha=0.7, edgecolor='black')
            ax.set_title(f'Calificación Promedio de Aspectos - {category}', 
                        fontsize=13, fontweight='bold', color='black')
            ax.set_ylabel('Calificación Promedio', fontsize=11, color='black')
            ax.tick_params(colors='black')
            ax.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=10, color='black')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            # Explicación por categoría
            st.markdown("**¿Qué indica este gráfico?**")
            st.markdown(
                f"Este gráfico muestra las calificaciones promedio de los aspectos para la categoría **{category}**. "
                "Si una barra es significativamente más baja que las demás, enfoca mejoras allí para ese grupo de clientes."
            )
    
    st.markdown("---")
    
    # Correlación con recomendación
    st.markdown("## Impacto de Cada Aspecto en la Recomendación")
    
    correlations = []
    for aspect in service_aspects:
        valid_data = df[[aspect, 'Recommended_bool']].dropna()
        if len(valid_data) > 0:
            corr = valid_data[aspect].corr(valid_data['Recommended_bool'])
            correlations.append(corr)
        else:
            correlations.append(0)
    
    corr_df = pd.DataFrame({
        'Aspecto': service_aspects,
        'Correlación con Recomendación': correlations
    }).sort_values('Correlación con Recomendación', ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors_corr = ['green' if x > 0 else 'red' for x in corr_df['Correlación con Recomendación']]
    bars = ax.barh(corr_df['Aspecto'], corr_df['Correlación con Recomendación'], color=colors_corr)
    ax.set_title('Correlación de Aspectos del Servicio con Recomendación', 
                 fontsize=14, fontweight='bold', color='black')
    ax.set_xlabel('Coeficiente de Correlación', fontsize=11, color='black')
    ax.tick_params(colors='black')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.grid(axis='x', alpha=0.3)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.01 if width > 0 else width - 0.01, 
               bar.get_y() + bar.get_height()/2,
               f'{width:.3f}',
               ha='left' if width > 0 else 'right', 
               va='center', fontsize=10, color='black')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown(f"""
    **Insight Clave:** El aspecto **{corr_df.iloc[0]['Aspecto']}** muestra la correlación más fuerte 
    con la probabilidad de recomendación ({corr_df.iloc[0]['Correlación con Recomendación']:.3f}), 
    indicando que mejoras en este área tendrían el mayor impacto en la lealtad del cliente.
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def show_geographic_analysis(df):
    """Análisis Geográfico: países, rutas y calificaciones por ubicación."""
    st.title("Análisis Geográfico")
    st.markdown("### Distribución Geográfica de Reseñas")
    st.markdown("---")

    # Top países por número de reseñas
    st.markdown("## Top Países por Número de Reseñas")
    top_countries = df['Passenger Country'].value_counts().head(TOP_N_COUNTRIES)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(top_countries.index, top_countries.values, color='steelblue')
    ax.set_title('Top 15 Países con Más Reseñas', fontsize=14, fontweight='bold')
    ax.set_xlabel('Número de Reseñas')
    ax.set_ylabel('País')
    ax.grid(axis='x', alpha=0.3)
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, f' {int(width)}', ha='left', va='center', fontsize=9)
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    # Listado top-5 dinámico y explicación (según notebook)
    top5_countries = top_countries.head(5)
    st.markdown("**Top países (5 principales) por volumen de reseñas:**")
    if not top5_countries.empty:
        for country, cnt in top5_countries.items():
            st.markdown(f"- **{country}**: {int(cnt):,} reseñas")
    else:
        st.markdown("- No hay datos de país disponibles en este dataset.")

    st.markdown("**Interpretación:**")
    st.markdown(
        "El Reino Unido y otros mercados clave concentran gran parte del volumen; prioriza pilotos y acciones en esos mercados para obtener impacto rápido. "
        "Revisa también la satisfacción relativa por país para detectar focos problemáticos locales."
    )
    st.markdown('---')

    # Calificación promedio por país (top 15 por volumen)
    st.markdown("## Calificación Promedio por País (Top 15 por Volumen)")
    country_ratings = df.groupby('Passenger Country').agg({
        'Overall Rating': 'mean',
        'Passenger Country': 'count'
    }).rename(columns={'Passenger Country': 'Count'}).sort_values('Count', ascending=False).head(TOP_N_COUNTRIES)
    country_ratings = country_ratings.sort_values('Overall Rating', ascending=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(country_ratings.index, country_ratings['Overall Rating'], color=plt.cm.RdYlGn(country_ratings['Overall Rating']/10))
    ax.set_title('Calificación Promedio por País (Top 15)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Calificación Promedio')
    ax.set_xlim(0, 10)
    ax.grid(axis='x', alpha=0.3)
    for i, (idx, row) in enumerate(country_ratings.iterrows()):
        ax.text(row['Overall Rating'], i, f" {row['Overall Rating']:.2f}", va='center', ha='left', fontsize=9, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('---')

    # Rutas más populares
    st.markdown("## Rutas Más Populares")
    # La columna 'Route' ya se crea en load_data
    top_routes = df['Route'].value_counts().head(TOP_N_ROUTES)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(top_routes.index, top_routes.values, color='royalblue')
    ax.set_title('Top 15 Rutas Más Comentadas', fontsize=14, fontweight='bold')
    ax.set_xlabel('Número de Reseñas')
    ax.invert_yaxis()
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, f' {int(width)}', ha='left', va='center', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    # Resumen numérico - top rutas
    top5_routes = top_routes.head(5)
    st.markdown("**Top rutas (5 principales) por número de reseñas:**")
    for route, cnt in top5_routes.items():
        st.markdown(f"- **{route}**: {int(cnt):,} reseñas")

    st.markdown('---')

    # Calificación promedio por ruta (con al menos MIN_REVIEWS_FOR_ROUTE_ANALYSIS reseñas)
    st.markdown(f"## Calificación Promedio por Ruta (mínimo {MIN_REVIEWS_FOR_ROUTE_ANALYSIS} reseñas)")
    route_ratings = df.groupby('Route').agg({
        'Overall Rating': 'mean',
        'Route': 'count'
    }).rename(columns={'Route': 'Count'})
    route_ratings = route_ratings[route_ratings['Count'] >= MIN_REVIEWS_FOR_ROUTE_ANALYSIS].sort_values('Overall Rating', ascending=True).head(TOP_N_ROUTES)
    if not route_ratings.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(route_ratings.index, route_ratings['Overall Rating'], color=plt.cm.RdYlGn(route_ratings['Overall Rating']/10))
        ax.set_title('Peores Rutas por Calificación (mínimo 5 reseñas)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Calificación Promedio')
        ax.set_xlim(0, 10)
        for i, (idx, row) in enumerate(route_ratings.iterrows()):
            ax.text(row['Overall Rating'], i, f" {row['Overall Rating']:.2f}", va='center', ha='left', fontsize=9, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # (Explicación anual ya ubicada en Análisis Temporal) -- no repetir aquí
    else:
        st.info('No hay rutas con al menos 5 reseñas para mostrar.')

def show_recommendations(df):
    """Recomendaciones Estratégicas (texto adaptado desde el notebook)"""
    st.title("Recomendaciones Estratégicas")
    st.markdown("### Plan de Acción y Recomendaciones")
    st.markdown("---")

    # Métricas clave
    total_reviews = len(df)
    avg_rating = df['Overall Rating'].mean()
    recommendation_rate = calculate_recommendation_rate(df)
    nps = calculate_nps(df)
    positive_rate = (df['Sentiment'] == 'Positivo').sum() / total_reviews * 100 if total_reviews > 0 else 0
    negative_rate = (df['Sentiment'] == 'Negativo').sum() / total_reviews * 100 if total_reviews > 0 else 0

    st.markdown("### ✅ Resumen de KPIs")
    st.markdown(f"- **Total de Reseñas:** {total_reviews:,}")
    st.markdown(f"- **Calificación Promedio:** {avg_rating:.2f} / 10")
    st.markdown(f"- **Tasa de Recomendación:** {recommendation_rate:.1f}%")
    st.markdown(f"- **Reseñas Positivas:** {positive_rate:.1f}%")
    st.markdown(f"- **Reseñas Negativas:** {negative_rate:.1f}%")
    st.markdown(f"- **NPS aproximado:** {nps:.1f}")

    st.markdown('---')

    st.markdown('#### 📌 Áreas Críticas de Mejora')
    st.markdown("- **Servicio en Tierra (Ground Service):** Es típicamente el aspecto peor valorado — acción: mejorar capacitación y procesos de check-in.")
    st.markdown("- **Transparencia de Precios:** Muchas quejas sobre cargos ocultos — acción: clarificar tarifas en el proceso de reserva.")
    st.markdown("- **Gestión de Equipaje:** Problemas y cobros frecuentes — acción: revisar políticas y comunicación.")
    st.markdown("- **Comunicación con Pasajeros:** Falta de información en retrasos/incidencias — acción: implementar comunicación proactiva.")

    st.markdown('---')

    st.markdown('#### ✅ Fortalezas a Mantener')
    st.markdown('- **Value for Money:** Muchos pasajeros reconocen buen valor por precio.')
    st.markdown('- **Puntualidad:** Cuando ocurre, es destacada positivamente.')
    st.markdown('- **Personal de Cabina:** Generalmente bien valorado.')
    st.markdown('- **Cobertura de Rutas:** Red extensa apreciada por clientes.')

    st.markdown('---')

    st.markdown('#### 🎯 Segmentos Prioritarios')
    st.markdown('- **Viajeros Familiares:** Tienden a tener experiencias más negativas; priorizar mejoras en sus rutas y servicios.')
    st.markdown('- **Mercados Clave:** Foco en UK, España, Italia, Irlanda por volumen.')
    st.markdown('- **Rutas Problemáticas:** Identificar rutas con peores calificaciones para intervenciones puntuales.')

    st.markdown('---')

    st.markdown('#### 📊 Métricas a Monitorear')
    st.markdown('- **NPS (Net Promoter Score):** Mensual')
    st.markdown('- **Tasa de Recomendación:** Sumar seguimiento mensual')
    st.markdown('- **Calificación de Ground Service:** Métrica prioritaria')
    st.markdown('- **Volumen de Quejas por Categoría:** Detectar patrones emergentes')
    st.markdown('- **Satisfacción por Tipo de Viajero:** Medir y cerrar brechas')

    st.markdown('---')

    # Cronograma simplificado (mantener tabla ligera)
    timeline_data = {
        'Fase': ['Fase 1', 'Fase 2', 'Fase 3', 'Fase 4'],
        'Período': ['Meses 1-3', 'Meses 4-6', 'Meses 7-9', 'Meses 10-12'],
        'Acciones Clave': [
            'Auditoría completa, Formación de equipos, Quick wins',
            'Implementación mejoras prioritarias, Lanzamiento programa fidelización',
            'Optimización continua, Expansión a todos los segmentos',
            'Evaluación resultados, Ajustes finales, Planificación año 2'
        ],
        'Meta de Satisfacción': [f'{avg_rating + 0.5:.1f}', f'{avg_rating + 1.0:.1f}', f'{avg_rating + 1.5:.1f}', f'{avg_rating + 2.0:.1f}']
    }
    timeline_df = pd.DataFrame(timeline_data)
    st.markdown('## Cronograma de Implementación Sugerido')
    st.table(timeline_df)

    st.markdown('---')

    # Conclusión final (texto tomado del notebook)
    st.markdown('## Conclusión y Próximos Pasos')
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown(f"""
    ### Resumen Ejecutivo

    El análisis de {total_reviews:,} reseñas ha identificado oportunidades significativas de mejora en la experiencia del cliente de Ryanair. Con una calificación promedio actual de **{avg_rating:.1f}/10** y una tasa de recomendación del **{recommendation_rate:.1f}%**, existe un margen considerable para aumentar la satisfacción y lealtad del cliente.

    ### Impacto Potencial

    La implementación de las recomendaciones propuestas podría resultar en:
    - **Aumento de 2-3 puntos** en la calificación promedio general
    - **Incremento del 15-20%** en la tasa de recomendación
    - **Reducción del 30%** en reseñas negativas
    - **Mejora del 25%** en satisfacción de aspectos críticos

    ### Recomendación Final

    Se recomienda priorizar la mejora en los aspectos críticos identificados (por ejemplo, Ground Service) como punto de partida, estableciendo un equipo multifuncional dedicado con autoridad para implementar cambios rápidos. El monitoreo continuo mediante los KPIs establecidos permitirá ajustar la estrategia en tiempo real y maximizar el retorno de inversión.

    **La inversión en experiencia del cliente no es un gasto, es una inversión estratégica que generará retornos sostenibles a largo plazo.**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Cargar datos: permitir uploader en sidebar si no hay CSV disponible
    uploaded_file = st.sidebar.file_uploader('Upload reviews CSV', type=['csv'])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        df = load_data()

    # Botón para recargar datos sin reiniciar el servidor
    if st.sidebar.button('Recargar datos'):
        try:
            st.cache_data.clear()
        except Exception:
            try:
                load_data.clear()
            except Exception:
                pass

        if uploaded_file is not None:
            new_df = load_data(uploaded_file)
        else:
            new_df = load_data()

        if new_df is None:
            st.sidebar.error('No se encontró ningún CSV para recargar.')
        else:
            st.session_state['df'] = new_df
            st.sidebar.success('Datos recargados correctamente.')
            st.rerun()

    if df is None:
        st.sidebar.warning('No se encontró el archivo de datos. Por favor sube `ryanair_reviews.csv` o coloca el archivo en el directorio del proyecto.')
        st.info('Sube el CSV usando el uploader en la barra lateral para continuar.')
        return

    # Guardar en session_state para uso interactivo
    st.session_state['df'] = df

    # Sidebar - Índice destacado (si no existe antes)
    st.sidebar.markdown(
        """
        <div class='sidebar-index' style='background-color:#ffffff;padding:10px;border-radius:8px;text-align:left;margin-bottom:12px;border-left:6px solid #073590;'>
            <h2 style='color:#073590;margin:0;font-size:18px;margin-left:6px;'>Índice</h2>
            <div style='color:#334155;font-size:13px;margin-top:6px;margin-left:6px;'>Navegación rápida</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Present radio options with icons but map to canonical page keys
    selected = st.sidebar.radio('Secciones', list(NAVIGATION_OPTIONS.keys()), index=0, label_visibility='hidden')
    page = NAVIGATION_OPTIONS[selected]

    st.sidebar.markdown('---')
    st.sidebar.markdown("### Filtros de Datos")

    # Filtro de fecha
    min_date = df['Date Published'].min()
    max_date = df['Date Published'].max()
    date_range = st.sidebar.date_input(
        "Rango de fechas:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filtro de verificación
    verification_filter = st.sidebar.multiselect(
        "Verificación de viaje:",
        options=df['Trip_verified_clean'].unique(),
        default=df['Trip_verified_clean'].unique()
    )

    # Filtro por tipo de viajero
    traveller_types = st.sidebar.multiselect(
        "Tipo de viajero:",
        options=sorted(df['Type Of Traveller'].dropna().unique()),
        default=sorted(df['Type Of Traveller'].dropna().unique())
    )

    # Filtro por país
    all_countries = sorted(df['Passenger Country'].dropna().unique())
    country_filter = st.sidebar.multiselect(
        "País del pasajero:",
        options=['Todos'] + all_countries,
        default=['Todos']
    )

    # Filtro por rango de calificación
    rating_range = st.sidebar.slider(
        "Rango de calificación (1-10):",
        min_value=1,
        max_value=10,
        value=(1, 10)
    )

    # Aplicar filtros básicos
    df_filtered = apply_filters(df, date_range, verification_filter)

    # Aplicar filtros adicionales
    if traveller_types:
        df_filtered = df_filtered[df_filtered['Type Of Traveller'].isin(traveller_types)]

    if 'Todos' not in country_filter and country_filter:
        df_filtered = df_filtered[df_filtered['Passenger Country'].isin(country_filter)]

    df_filtered = df_filtered[
        (df_filtered['Overall Rating'] >= rating_range[0]) &
        (df_filtered['Overall Rating'] <= rating_range[1])
    ]

    st.sidebar.markdown(f"**Reseñas seleccionadas:** {len(df_filtered):,} de {len(df):,}")

    # Botón para exportar datos filtrados
    if st.sidebar.button('📥 Exportar datos filtrados'):
        csv = df_filtered.to_csv(index=False)
        st.sidebar.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=f"ryanair_filtrado_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    # Contenido principal según la página seleccionada
    if page == "Resumen Ejecutivo":
        show_executive_summary(df_filtered)
    elif page == "Análisis Exploratorio":
        show_eda(df_filtered)
    elif page == "Análisis Temporal":
        show_temporal_analysis(df_filtered)
    elif page == "Análisis de Calificaciones":
        show_rating_analysis(df_filtered)
    elif page == "Recomendaciones Estratégicas":
        show_recommendations(df_filtered)
    elif page == "Análisis Geográfico":
        show_geographic_analysis(df_filtered)


if __name__ == "__main__":
    main()
