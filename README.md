# 📊 Dashboard de Análisis de Satisfacción del Cliente - Ryanair

Dashboard interactivo construido con Streamlit para analizar la satisfacción del cliente de Ryanair mediante reseñas y calificaciones.

![Ryanair Analysis](https://img.shields.io/badge/Ryanair-Analysis-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)

## 📑 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura de Datos](#estructura-de-datos)
- [Secciones del Dashboard](#secciones-del-dashboard)
- [Configuración](#configuración)
- [Contribución](#contribución)

## ✨ Características

### Análisis Completo
- **Resumen Ejecutivo**: KPIs principales y hallazgos clave para la dirección ejecutiva
- **Análisis Exploratorio**: Distribución de calificaciones, tipos de viajero y correlaciones
- **Análisis Temporal**: Evolución de la satisfacción a lo largo del tiempo
- **Análisis Geográfico**: Distribución por países y rutas más populares
- **Análisis de Calificaciones**: Evaluación detallada por aspectos del servicio
- **Recomendaciones Estratégicas**: Plan de acción basado en datos

### Filtros Interactivos
- Rango de fechas personalizado
- Filtro por verificación de viaje
- Filtro por tipo de viajero
- Filtro por país del pasajero
- Rango de calificación (1-10)

### Funcionalidades Adicionales
- Exportación de datos filtrados a CSV
- Visualizaciones interactivas y detalladas
- Cálculo automático de KPIs (NPS, tasa de recomendación, etc.)
- Interfaz intuitiva y responsiva

## 📁 Estructura del Proyecto

```
Ryanair Pr/
│
├── src/                        # Código fuente
│   ├── app.py                  # Aplicación principal de Streamlit
│   ├── config.py               # Configuración y constantes
│   └── utils.py                # Funciones utilitarias
│
├── data/                       # Datos del proyecto
│   └── ryanair_reviews (1).csv # Dataset de reseñas
│
├── notebooks/                  # Jupyter notebooks para análisis
│   └── ryanair_analysis (1).ipynb
│
├── docs/                       # Documentación
│   ├── README.md               # Documentación detallada
│   ├── guia_presentacion_ryanair.docx
│   └── ryanair_storytelling.pptx
│
├── archive/                    # Versiones antiguas
│   ├── app copy.py
│   └── streamlit_app.py
│
├── .gitignore                  # Archivos ignorados por Git
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "Ryanair Pr"
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv

   # En Windows:
   venv\Scripts\activate

   # En Mac/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Preparar los datos**
   - Coloca tu archivo CSV de reseñas en el directorio del proyecto
   - El archivo debe llamarse `ryanair_reviews.csv` o `ryanair_reviews (1).csv`
   - Alternativamente, puedes usar el uploader en la aplicación

## 💻 Uso

### Iniciar la Aplicación

```bash
streamlit run src/app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Cargar Datos

Hay dos formas de cargar datos:

1. **Automática**: Coloca el archivo CSV en el directorio del proyecto con el nombre correcto
2. **Manual**: Usa el uploader en la barra lateral de la aplicación

### Navegación

1. Usa el menú lateral para navegar entre secciones
2. Aplica filtros en la barra lateral según tus necesidades
3. Exporta datos filtrados cuando lo necesites

## 📊 Estructura de Datos

El archivo CSV debe contener las siguientes columnas:

### Columnas Requeridas
- `Date Published`: Fecha de publicación de la reseña
- `Overall Rating`: Calificación general (1-10)

### Columnas Opcionales (Recomendadas)
- `Date Flown`: Fecha del vuelo
- `Recommended`: Si recomienda o no (yes/no)
- `Trip_verified`: Verificación del viaje
- `Type Of Traveller`: Tipo de viajero
- `Passenger Country`: País del pasajero
- `Origin`: Origen del vuelo
- `Destination`: Destino del vuelo
- `Seat Comfort`: Calificación de comodidad del asiento (1-5)
- `Cabin Staff Service`: Calificación del servicio de cabina (1-5)
- `Food & Beverages`: Calificación de comida y bebidas (1-5)
- `Ground Service`: Calificación del servicio en tierra (1-5)
- `Value For Money`: Calificación de relación calidad-precio (1-5)

## 🎯 Secciones del Dashboard

### 1. Resumen Ejecutivo
- **KPIs Principales**: Calificación promedio, tasa de recomendación, total de reseñas
- **Distribución de Satisfacción**: Categorización en Positivo, Neutral y Negativo
- **Evaluación por Aspectos**: Calificación promedio de cada aspecto del servicio
- **Hallazgos Clave**: Puntos fuertes y áreas de mejora
- **Conclusión Ejecutiva**: Resumen para la dirección

### 2. Análisis Exploratorio (EDA)
- **Información General**: Estadísticas básicas del dataset
- **Distribución de Calificaciones**: Histograma completo de ratings
- **Análisis por Tipo de Viajero**: Distribución y calificaciones promedio
- **Relación Calificación-Recomendación**: Correlación entre variables
- **Matriz de Correlación**: Relaciones entre aspectos del servicio

### 3. Análisis Temporal
- **Volumen de Reseñas**: Tendencia mensual de reseñas recibidas
- **Evolución de Calificaciones**: Tendencia de satisfacción en el tiempo
- **Comparativa Anual**: Análisis año a año
- **Insights Temporales**: Identificación de tendencias y puntos de atención

### 4. Análisis Geográfico
- **Top Países**: Países con más reseñas
- **Calificación por País**: Satisfacción promedio por ubicación
- **Rutas Populares**: Rutas más comentadas
- **Rutas Problemáticas**: Rutas con peores calificaciones

### 5. Análisis de Calificaciones
- **Boxplots por Aspecto**: Distribución detallada de calificaciones
- **Comparación de Aspectos**: Estadísticas descriptivas completas
- **Análisis por Categoría**: Desglose Positivo/Neutral/Negativo
- **Correlación con Recomendación**: Impacto de cada aspecto en la lealtad

### 6. Recomendaciones Estratégicas
- **Resumen de KPIs**: Métricas clave consolidadas
- **Áreas Críticas de Mejora**: Prioridades de acción
- **Fortalezas a Mantener**: Aspectos positivos a preservar
- **Segmentos Prioritarios**: Grupos de clientes clave
- **Métricas a Monitorear**: KPIs de seguimiento
- **Cronograma de Implementación**: Plan de acción por fases

## ⚙️ Configuración

### Personalizar Constantes

Edita el archivo `config.py` para personalizar:

```python
# Cambiar número de elementos en visualizaciones
TOP_N_COUNTRIES = 15  # Top países a mostrar
TOP_N_ROUTES = 15     # Top rutas a mostrar

# Cambiar umbrales de categorización
RATING_THRESHOLDS = {
    'negative_max': 3,   # Máximo para categoría negativa
    'neutral_max': 7,    # Máximo para categoría neutral
    'positive_min': 8    # Mínimo para categoría positiva
}

# Personalizar colores
COLORS = {
    'positive': '#28a745',
    'neutral': '#ffc107',
    'negative': '#dc3545'
}
```

### Agregar Rutas de Datos

Para agregar nuevas rutas de búsqueda de archivos, modifica `config.py`:

```python
DATA_PATHS = [
    'tu/ruta/personalizada/data.csv',
    os.path.join(os.getcwd(), 'ryanair_reviews.csv'),
    # ... más rutas
]
```

## 🛠️ Arquitectura Técnica

### Módulos

- **app.py**: Interfaz principal y lógica de visualización
- **config.py**: Configuración centralizada y constantes
- **utils.py**: Funciones utilitarias y procesamiento de datos

### Tecnologías Utilizadas

- **Streamlit**: Framework de aplicación web
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Operaciones numéricas
- **Matplotlib**: Visualizaciones estáticas
- **Seaborn**: Visualizaciones estadísticas

### Optimizaciones

- **Caché de datos**: `@st.cache_data` para carga eficiente
- **Funciones helper**: Código DRY y reutilizable
- **Constantes centralizadas**: Fácil mantenimiento
- **Manejo de errores**: Excepciones específicas y mensajes claros

## 📈 Métricas Calculadas

### KPIs Principales
- **Calificación Promedio**: Media de Overall Rating
- **Tasa de Recomendación**: % de usuarios que recomiendan
- **NPS (Net Promoter Score)**: (Promotores - Detractores) / Total × 100
- **Distribución de Sentimiento**: % Positivo, Neutral, Negativo

### Categorización
- **Negativo**: Calificación 1-3
- **Neutral**: Calificación 4-7
- **Positivo**: Calificación 8-10

## 🤝 Contribución

### Mejoras Futuras Sugeridas

1. **Análisis de Texto (NLP)**
   - Análisis de sentimiento en comentarios
   - Word clouds de términos frecuentes
   - Extracción de temas principales

2. **Visualizaciones Avanzadas**
   - Migración a Plotly para interactividad
   - Mapas geográficos interactivos
   - Dashboards personalizables

3. **Predicciones**
   - Forecasting de tendencias
   - Clasificación automática de sentimiento
   - Detección de anomalías

4. **Integraciones**
   - Conexión a bases de datos
   - APIs para actualización automática
   - Exportación a múltiples formatos

## 📝 Notas de Versión

### Versión 2.0 (Actual)
- ✅ Refactorización completa del código
- ✅ Separación en módulos (app, config, utils)
- ✅ Mejora en manejo de errores
- ✅ Filtros adicionales interactivos
- ✅ Exportación de datos filtrados
- ✅ Uso de constantes centralizadas
- ✅ Documentación completa

### Versión 1.0
- Versión inicial con análisis básico
- Visualizaciones estáticas
- Filtros limitados

## 📄 Licencia

Este proyecto es de uso interno y educativo.

## 👤 Autor

Análisis de Satisfacción del Cliente - Ryanair Dashboard

---

**¿Preguntas o sugerencias?** Abre un issue o contacta al equipo de desarrollo.
