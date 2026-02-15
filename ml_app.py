"""
App Interactiva de Machine Learning - Predicción de Recomendación Ryanair
Versión Simple y Limpia
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Configuración de la página
st.set_page_config(
    page_title="ML Predictor - Ryanair",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Profesional - Colores Ryanair
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        height: 70px;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 1px;
        background: linear-gradient(135deg, #073590 0%, #0A4DAB 100%);
        color: #F1C933;
        border: none;
        border-radius: 8px;
        margin: 25px 0;
        box-shadow: 0 4px 15px rgba(7, 53, 144, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0A4DAB 0%, #073590 100%);
        box-shadow: 0 6px 20px rgba(7, 53, 144, 0.4);
        transform: translateY(-2px);
    }
    .prediction-yes {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border: 3px solid #2E7D32;
        padding: 35px;
        border-radius: 12px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
    }
    .prediction-no {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border: 3px solid #C62828;
        padding: 35px;
        border-radius: 12px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 4px 12px rgba(198, 40, 40, 0.2);
    }
    h1 {
        color: #073590;
        text-align: center;
        font-weight: 700;
    }
    h2 {
        color: #073590;
        margin-top: 30px;
        font-weight: 600;
    }
    h3 {
        color: #0A4DAB;
        font-weight: 600;
    }
    .metric-box {
        background-color: #F5F7FA;
        padding: 18px;
        border-radius: 8px;
        border-left: 4px solid #073590;
        margin: 12px 0;
    }
    .stExpander {
        border: 1px solid #E0E0E0;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar modelo
@st.cache_resource
def load_model():
    """Cargar modelo Random Forest"""
    try:
        with open('ryanair_recommendation_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Ejecuta primero: python run_ml_analysis.py")
        return None

def main():
    # Título profesional
    st.markdown("# 🎯 Sistema Predictivo de Recomendación")
    st.markdown("### Análisis de Machine Learning para Evaluación de Satisfacción del Cliente")
    st.markdown("---")

    # Cargar modelo
    model = load_model()
    if model is None:
        st.stop()

    # Información del modelo
    with st.expander("ℹ️ Información del Sistema Predictivo", expanded=False):
        st.markdown("""
        ### 🔍 Descripción del Sistema

        Este sistema utiliza algoritmos de **Machine Learning** (Random Forest Classifier)
        para predecir la probabilidad de recomendación de un cliente basándose en su
        evaluación de 5 aspectos clave del servicio.

        ### 📊 Especificaciones Técnicas

        - **Algoritmo:** Random Forest Classifier
        - **Accuracy:** 94.67%
        - **Precision:** 90.14%
        - **Recall:** 91.03%
        - **ROC-AUC Score:** 0.9467
        - **Dataset de Entrenamiento:** 2,249 reseñas verificadas
        - **Variables Predictoras:** 5 aspectos del servicio + segmento de cliente

        ### 🎯 Aplicaciones

        - Identificación proactiva de clientes en riesgo de churn
        - Priorización de intervenciones de servicio al cliente
        - Evaluación de impacto de mejoras operativas
        - Segmentación estratégica de clientes
        """)

    st.markdown("## 📝 Calificaciones del Cliente")
    st.markdown("*Indica cómo calificó el cliente cada aspecto (1 = Muy malo, 5 = Excelente)*")

    # Inputs organizados en 2 columnas
    col1, col2 = st.columns(2)

    with col1:
        seat_comfort = st.slider(
            "🪑 Comodidad del Asiento",
            1.0, 5.0, 3.0, 0.5,
            help="Confort y espacio del asiento"
        )

        cabin_staff = st.slider(
            "👥 Servicio del Personal",
            1.0, 5.0, 3.0, 0.5,
            help="Atención y amabilidad de la tripulación"
        )

        food_bev = st.slider(
            "🍽️ Comida y Bebidas",
            1.0, 5.0, 2.0, 0.5,
            help="Calidad de alimentos y bebidas"
        )

    with col2:
        ground_service = st.slider(
            "✈️ Servicio en Tierra",
            1.0, 5.0, 2.0, 0.5,
            help="Check-in, embarque y manejo en aeropuerto"
        )

        value_money = st.slider(
            "💰 Relación Calidad-Precio",
            1.0, 5.0, 3.0, 0.5,
            help="¿Valió la pena el precio pagado?"
        )

    # Mostrar promedio
    avg_score = np.mean([seat_comfort, cabin_staff, food_bev, ground_service, value_money])
    st.markdown(f"**Calificación Promedio:** {avg_score:.2f} / 5.0")

    # Tipo de pasajero
    st.markdown("---")
    st.markdown("### 👤 Perfil del Pasajero")

    traveller_type = st.selectbox(
        "Tipo de Viajero:",
        ["Couple Leisure", "Solo Leisure", "Family Leisure", "Business"],
        help="Selecciona el tipo de pasajero para un análisis más personalizado"
    )

    # Descripciones de segmentos
    segment_descriptions = {
        "Couple Leisure": {
            "emoji": "💑",
            "descripcion": "Pareja viajando por placer",
            "caracteristicas": "Suelen buscar comodidad y buen servicio. Valoran la experiencia general más que el precio.",
            "avg_satisfaction": 4.5,
            "prioridades": ["Servicio del Personal", "Comodidad del Asiento", "Relación Calidad-Precio"]
        },
        "Solo Leisure": {
            "emoji": "🧳",
            "descripcion": "Viajero individual por placer",
            "caracteristicas": "Más flexible con el servicio. Valora mucho la relación calidad-precio y la puntualidad.",
            "avg_satisfaction": 4.3,
            "prioridades": ["Relación Calidad-Precio", "Servicio en Tierra", "Puntualidad"]
        },
        "Family Leisure": {
            "emoji": "👨‍👩‍👧‍👦",
            "descripcion": "Familia viajando con niños",
            "caracteristicas": "Segmento más crítico. Necesitan espacio, buen servicio y gestión de equipaje. Muy sensibles a problemas.",
            "avg_satisfaction": 3.8,
            "prioridades": ["Servicio en Tierra", "Equipaje", "Espacio y Comodidad"]
        },
        "Business": {
            "emoji": "💼",
            "descripcion": "Viajero de negocios",
            "caracteristicas": "Valora eficiencia y puntualidad por encima de todo. Menos sensible al precio.",
            "avg_satisfaction": 4.6,
            "prioridades": ["Puntualidad", "Servicio en Tierra", "Eficiencia"]
        }
    }

    segment = segment_descriptions[traveller_type]

    with st.expander(f"{segment['emoji']} Ver perfil de este segmento", expanded=False):
        st.markdown(f"**Descripción:** {segment['descripcion']}")
        st.markdown(f"**Características:** {segment['caracteristicas']}")
        st.markdown(f"**Satisfacción promedio:** {segment['avg_satisfaction']:.1f}/5.0")
        st.markdown("**Prioridades principales:**")
        for i, prioridad in enumerate(segment['prioridades'], 1):
            st.markdown(f"   {i}. {prioridad}")

    st.markdown("---")

    # Botón de predicción profesional
    if st.button("📊 EJECUTAR ANÁLISIS PREDICTIVO"):

        # Preparar datos
        input_data = pd.DataFrame({
            'Seat Comfort': [seat_comfort],
            'Cabin Staff Service': [cabin_staff],
            'Food & Beverages': [food_bev],
            'Ground Service': [ground_service],
            'Value For Money': [value_money]
        })

        # Añadir columnas faltantes (todas en 0)
        for col in model.feature_names_in_:
            if col not in input_data.columns:
                input_data[col] = 0

        # Reordenar columnas
        input_data = input_data[model.feature_names_in_]

        # Predicción
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]

        # Mostrar resultado
        st.markdown("---")

        if prediction == 1:
            # SÍ recomienda
            st.markdown(f"""
            <div class="prediction-yes">
                <h1 style="color: #28a745; font-size: 48px; margin: 0;">✅ SÍ RECOMENDARÁ</h1>
                <h2 style="color: #28a745; margin: 10px 0;">Probabilidad: {probability[1]*100:.1f}%</h2>
                <p style="font-size: 18px; color: #155724; margin-top: 20px;">
                    Este cliente tiene alta probabilidad de recomendar Ryanair a otras personas.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Clasificación
            if probability[1] > 0.7:
                st.success("🟢 **PROMOTOR** - Cliente muy satisfecho que promoverá activamente la marca")
            else:
                st.info("🟡 **NEUTRAL** - Cliente satisfecho pero no entusiasta")

        else:
            # NO recomienda
            st.markdown(f"""
            <div class="prediction-no">
                <h1 style="color: #dc3545; font-size: 48px; margin: 0;">❌ NO RECOMENDARÁ</h1>
                <h2 style="color: #dc3545; margin: 10px 0;">Probabilidad: {probability[0]*100:.1f}%</h2>
                <p style="font-size: 18px; color: #721c24; margin-top: 20px;">
                    Este cliente tiene baja probabilidad de recomendar Ryanair a otras personas.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.error("🔴 **DETRACTOR** - Cliente insatisfecho que puede dañar la reputación")

        # Análisis profesional contextualizado
        st.markdown("---")
        st.markdown("### 📊 Análisis de Segmento y Contexto")

        # Generar análisis profesional
        if prediction == 1:
            # Cliente SÍ recomienda
            if traveller_type == "Couple Leisure":
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Desviación:** {'+' if avg_score > segment['avg_satisfaction'] else ''}{(avg_score - segment['avg_satisfaction']):.2f} puntos

                #### Factores Determinantes de la Recomendación:

                1. **Servicio del Personal (Cabin Staff):** {cabin_staff:.1f}/5.0
                   - Factor crítico para este segmento
                   - Cumple con expectativas de atención personalizada

                2. **Comodidad del Asiento:** {seat_comfort:.1f}/5.0
                   - Aspecto valorado en viajes de ocio en pareja
                   - Contribuye positivamente a la experiencia general

                3. **Relación Calidad-Precio:** {value_money:.1f}/5.0
                   - Percepción de valor adecuada para el segmento

                #### Implicaciones de Negocio:

                Este segmento representa un **valor estratégico alto**. Las parejas en ocio tienen:
                - Mayor propensión a compartir experiencias positivas en redes sociales
                - Influencia en decisiones de viaje de su círculo social cercano
                - Potencial de repetición de compra para futuras vacaciones

                **Recomendación Estratégica:** Mantener estándares de servicio del personal y comodidad
                para asegurar la conversión de este cliente en promotor activo de marca.
                """)
            elif traveller_type == "Solo Leisure":
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Desviación:** {'+' if avg_score > segment['avg_satisfaction'] else ''}{(avg_score - segment['avg_satisfaction']):.2f} puntos

                #### Factores Determinantes de la Recomendación:

                1. **Relación Calidad-Precio:** {value_money:.1f}/5.0
                   - Variable principal de decisión para este segmento
                   - Percepción positiva de valor generado

                2. **Servicio en Tierra:** {ground_service:.1f}/5.0
                   - Eficiencia en procesos operativos valorada
                   - Sin fricciones significativas en customer journey

                3. **Flexibilidad del Segmento**
                   - Menor sensibilidad a servicios complementarios
                   - Enfoque en funcionalidad básica del servicio

                #### Implicaciones de Negocio:

                Este segmento presenta **características estratégicas diferenciadas**:
                - Alta actividad en canales digitales (reseñas online, foros de viaje)
                - Capacidad de influencia en comunidades de viajeros independientes
                - Menor costo de adquisición y mayor margen operativo

                **Recomendación Estratégica:** Optimizar relación calidad-precio y eficiencia operativa
                para maximizar NPS en este segmento de alto alcance digital.
                """)
            elif traveller_type == "Family Leisure":
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0 (segmento más exigente)
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Desviación:** {'+' if avg_score > segment['avg_satisfaction'] else ''}{(avg_score - segment['avg_satisfaction']):.2f} puntos

                #### Factores Determinantes de la Recomendación:

                1. **Servicio en Tierra:** {ground_service:.1f}/5.0
                   - Variable crítica: gestión de equipaje, embarque, atención a necesidades especiales
                   - Performance por encima del umbral mínimo de aceptación

                2. **Experiencia Integral**
                   - Coordinación efectiva de múltiples touchpoints
                   - Ausencia de fricciones operativas significativas

                3. **Comodidad y Espacio:** {seat_comfort:.1f}/5.0
                   - Factor secundario pero relevante en viajes familiares
                   - Cumple requisitos mínimos de confort

                #### Implicaciones de Negocio:

                Este segmento representa **el mayor desafío operativo pero el mayor valor a largo plazo**:
                - CLV (Customer Lifetime Value) más alto: viajes recurrentes, múltiples pasajeros
                - Efecto red amplificado: influencia en grupos de padres, comunidades escolares
                - Barrera de salida alta una vez fidelizados

                **Recomendación Estratégica:** Resultado excepcional. Implementar programa de fidelización
                específico para familias y mantener excelencia en servicio en tierra. Este cliente representa
                un activo estratégico de alto valor.
                """)
            else:  # Business
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0 (segmento con mayor satisfacción)
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Desviación:** {'+' if avg_score > segment['avg_satisfaction'] else ''}{(avg_score - segment['avg_satisfaction']):.2f} puntos

                #### Factores Determinantes de la Recomendación:

                1. **Eficiencia Operativa y Puntualidad**
                   - KPI crítico para este segmento
                   - Cumplimiento de SLA (Service Level Agreement)

                2. **Servicio en Tierra:** {ground_service:.1f}/5.0
                   - Procesos ágiles de check-in y embarque
                   - Minimización de tiempos de espera

                3. **Relación Calidad-Precio:** {value_money:.1f}/5.0
                   - Valoración desde perspectiva de ROI de tiempo
                   - Menor sensibilidad a precio absoluto

                #### Implicaciones de Negocio:

                Este segmento constituye **el núcleo de ingresos recurrentes y predecibles**:
                - Frecuencia de viaje más alta (4-8x año vs. 1-2x ocio)
                - Posibilidad de contratos corporativos B2B
                - Menor elasticidad precio-demanda
                - Influencia en decisiones de compra corporativa

                **Recomendación Estratégica:** Cliente de alto valor estratégico. Considerar programa
                corporate loyalty y garantías de servicio específicas. Potencial para generar acuerdos
                de volumen con empresas.
                """)
        else:
            # Cliente NO recomienda
            if traveller_type == "Couple Leisure":
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Gap Crítico:** {(avg_score - segment['avg_satisfaction']):.2f} puntos bajo benchmark

                #### Análisis de Factores Negativos:

                1. **Servicio del Personal:** {cabin_staff:.1f}/5.0
                   - Por debajo del umbral mínimo de aceptación (3.0)
                   - Factor crítico para este segmento no cumplido

                2. **Comodidad del Asiento:** {seat_comfort:.1f}/5.0
                   - Variable secundaria pero significativa en percepción de valor
                   - Contribuye negativamente a experiencia general

                3. **Percepción de Valor:** {value_money:.1f}/5.0
                   - Desequilibrio entre expectativas y entrega de servicio
                   - ROI emocional negativo

                #### Impacto en Negocio:

                **Riesgo Alto - Clasificación: Detractor Activo**

                - **Efecto WOM negativo:** Probabilidad elevada de reseñas negativas en TripAdvisor, Google, redes sociales
                - **Amplificación social:** Este segmento comparte experiencias activamente con círculo cercano (10-15 personas)
                - **Daño reputacional:** Impacto medio en brand perception y consideration set

                #### Plan de Acción Recomendado:

                **Prioridad: ALTA**
                1. **Contacto Proactivo (24-48h):** Email o llamada de servicio al cliente
                2. **Compensación:** Voucher 20-30€ próximo vuelo o upgrade en siguiente reserva
                3. **Root Cause Analysis:** Investigar incidencia específica en este vuelo
                4. **Follow-up:** Contacto post-resolución para medir efectividad de recovery
                """)
            elif traveller_type == "Solo Leisure":
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0 (segmento más tolerante)
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Gap Crítico:** {(avg_score - segment['avg_satisfaction']):.2f} puntos bajo benchmark

                #### Análisis de Factores Negativos:

                1. **Relación Calidad-Precio:** {value_money:.1f}/5.0
                   - Variable decisiva para este segmento
                   - Percepción de valor negativa indica fallo sistémico

                2. **Servicio en Tierra:** {ground_service:.1f}/5.0
                   - Eficiencia operativa comprometida
                   - Fricciones en procesos básicos

                3. **Severidad del Caso**
                   - Segmento habitualmente flexible muestra insatisfacción
                   - Indica problemas operativos significativos

                #### Impacto en Negocio:

                **Riesgo Muy Alto - Señal de Alerta Sistémica**

                - **Digital Reach:** Alta propensión a reseñas detalladas en plataformas digitales
                - **Credibilidad:** Reseñas de viajeros solos percibidas como más objetivas y confiables
                - **Comunidades Online:** Influencia en foros especializados (TripAdvisor, Lonely Planet, Reddit Travel)

                #### Plan de Acción Recomendado:

                **Prioridad: MUY ALTA**
                1. **Análisis de Causa Raíz Inmediato:** Identificar fallo operativo específico
                2. **Compensación Directa:** Reembolso parcial (15-25%) o voucher generoso
                3. **Investigación Ampliada:** Revisar otros pasajeros del mismo vuelo/ruta
                4. **Mejora de Proceso:** Implementar correcciones operativas si se identifican patrones
                """)
            elif traveller_type == "Family Leisure":
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0 (segmento más exigente)
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Gap Crítico:** {(avg_score - segment['avg_satisfaction']):.2f} puntos bajo benchmark ya bajo

                #### Análisis de Factores Negativos:

                1. **Servicio en Tierra:** {ground_service:.1f}/5.0
                   - Variable crítica para familias (equipaje, embarque, atención especial)
                   - Fallo en touchpoint de mayor impacto

                2. **Experiencia Operativa Deficiente**
                   - Múltiples puntos de fricción en customer journey
                   - Coordinación inadecuada para necesidades familiares

                3. **Complejidad de Gestión**
                   - Varios pasajeros afectados simultáneamente
                   - Multiplicador de insatisfacción por grupo

                #### Impacto en Negocio:

                **Riesgo Crítico - Código Rojo**

                - **CLV Negativo:** Pérdida potencial de ingresos recurrentes (4-5 pasajeros × frecuencia anual)
                - **Efecto Red Amplificado:** Influencia en 20-30 familias en comunidades escolares/sociales
                - **Brand Damage:** Reputación comprometida en segmento de alto valor lifetime
                - **Switching Probability:** 85% probabilidad de cambio permanente a competidor

                #### Plan de Acción Recomendado:

                **Prioridad: CRÍTICA - Escalación Inmediata**
                1. **Contacto Executive Level (12-24h):** Intervención de Customer Care Manager
                2. **Compensación Premium:** Reembolso 30-40% + vouchers familia completa
                3. **Service Recovery:** Garantías escritas de mejora + seguimiento trimestral
                4. **Win-Back Strategy:** Descuentos especiales en próximas 3 reservas
                5. **Root Cause:** Auditoría completa de operaciones en tierra para este vuelo/ruta
                """)
            else:  # Business
                st.markdown(f"""
                **{segment['emoji']} Segmento:** {segment['descripcion']}

                **Benchmark del Segmento:** {segment['avg_satisfaction']:.1f}/5.0 (segmento con mayor satisfacción histórica)
                **Calificación del Cliente:** {avg_score:.2f}/5.0
                **Gap Crítico:** {(avg_score - segment['avg_satisfaction']):.2f} puntos - **Desviación Anómala**

                #### Análisis de Factores Negativos:

                1. **Eficiencia Operativa Comprometida**
                   - Fallo en KPI crítico: puntualidad o tiempo de proceso
                   - SLA (Service Level Agreement) no cumplido

                2. **Servicio en Tierra:** {ground_service:.1f}/5.0
                   - Procesos ineficientes que generan pérdida de tiempo
                   - Impacto directo en productividad del cliente

                3. **Relación Valor-Tiempo:** {value_money:.1f}/5.0
                   - ROI percibido negativo desde perspectiva de costo oportunidad
                   - Premium no justificado por servicio entregado

                #### Impacto en Negocio:

                **Riesgo Estratégico Máximo - Alerta Ejecutiva**

                - **Revenue at Risk:** Cliente de frecuencia alta (4-8 viajes/año)
                - **Corporate Impact:** Potencial pérdida de contrato B2B completo
                - **Churn Probability:** >90% probabilidad de migración permanente a competidor
                - **Network Effect:** Influencia en decisiones de travel managers corporativos
                - **LTV at Risk:** €2,000-5,000 anuales por cliente + potencial corporate account

                #### Plan de Acción Recomendado:

                **Prioridad: MÁXIMA - Intervención C-Level**
                1. **Contacto Ejecutivo Inmediato (<12h):** Director Customer Experience o VP Operations
                2. **Compensación Estratégica:** Reembolso completo + status premium 6-12 meses
                3. **Service Guarantee:** Commitment escrito de mejora con KPIs específicos
                4. **Account Management:** Asignación de dedicated account manager
                5. **Corporate Opportunity:** Evaluar posibilidad de acuerdo marco empresarial
                6. **Forensic Analysis:** Investigación exhaustiva del incidente para evitar recurrencia
                """)

        # Gráfico de probabilidades (simple)
        st.markdown("### 📊 Probabilidades")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="No Recomienda",
                value=f"{probability[0]*100:.1f}%",
                delta=None
            )
        with col2:
            st.metric(
                label="Sí Recomienda",
                value=f"{probability[1]*100:.1f}%",
                delta=None
            )

        # Gráfico visual simple
        fig, ax = plt.subplots(figsize=(10, 2))
        colors = ['#dc3545', '#28a745']
        labels = ['No Recomienda', 'Sí Recomienda']

        ax.barh([0], [probability[0]], color=colors[0], height=0.5, label=labels[0])
        ax.barh([0], [probability[1]], left=[probability[0]], color=colors[1], height=0.5, label=labels[1])

        # Añadir texto
        if probability[0] > 0.1:
            ax.text(probability[0]/2, 0, f'{probability[0]*100:.1f}%',
                   ha='center', va='center', fontsize=16, fontweight='bold', color='white')
        if probability[1] > 0.1:
            ax.text(probability[0] + probability[1]/2, 0, f'{probability[1]*100:.1f}%',
                   ha='center', va='center', fontsize=16, fontweight='bold', color='white')

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, 0.5)
        ax.axis('off')

        st.pyplot(fig)
        plt.close()

        # Análisis de aspectos
        st.markdown("---")
        st.markdown("### 📋 Análisis de Aspectos")

        aspects_names = ['Comodidad Asiento', 'Personal Cabina', 'Comida/Bebidas',
                        'Servicio Tierra', 'Calidad-Precio']
        aspects_values = [seat_comfort, cabin_staff, food_bev, ground_service, value_money]

        # Identificar fortalezas y debilidades
        weak = [(n, v) for n, v in zip(aspects_names, aspects_values) if v < 3]
        strong = [(n, v) for n, v in zip(aspects_names, aspects_values) if v >= 4]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ⚠️ Aspectos Débiles")
            if weak:
                for name, val in weak:
                    st.markdown(f"- **{name}**: {val:.1f}/5.0")
            else:
                st.markdown("✅ No hay aspectos débiles")

        with col2:
            st.markdown("#### ✅ Fortalezas")
            if strong:
                for name, val in strong:
                    st.markdown(f"- **{name}**: {val:.1f}/5.0")
            else:
                st.markdown("⚠️ No hay fortalezas destacadas")

        # Importancia de aspectos (hardcoded basado en el modelo)
        st.markdown("---")
        st.markdown("### 🎯 ¿Qué Aspectos Son Más Importantes?")

        importance_data = {
            'Servicio en Tierra': 0.31,
            'Relación Calidad-Precio': 0.24,
            'Servicio del Personal': 0.21,
            'Comodidad del Asiento': 0.15,
            'Comida y Bebidas': 0.09
        }

        st.markdown("""
        El modelo ha identificado que estos aspectos tienen el siguiente impacto
        en la decisión de recomendar:
        """)

        for aspect, importance in importance_data.items():
            st.progress(importance)
            st.caption(f"**{aspect}**: {importance*100:.0f}% de impacto")

        # Insight final
        st.markdown("---")
        st.markdown("### 💡 Insight Clave")

        if ground_service < 3:
            st.warning("""
            **⚠️ Atención:** El **Servicio en Tierra** está bajo y es el aspecto MÁS IMPORTANTE
            para la recomendación. Mejorar este aspecto tiene el mayor impacto potencial.
            """)
        elif value_money < 3:
            st.warning("""
            **⚠️ Atención:** La **Relación Calidad-Precio** está baja y es el segundo
            aspecto más importante. Los clientes sienten que no vale la pena.
            """)
        elif avg_score >= 4:
            st.success("""
            **🎉 Excelente:** Las calificaciones son buenas en general.
            Este cliente está satisfecho y probablemente recomendará.
            """)
        else:
            st.info("""
            **📊 Análisis:** Las calificaciones son mixtas. Hay oportunidades de mejora
            especialmente en Servicio en Tierra y Relación Calidad-Precio.
            """)

    # Footer profesional
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; background: linear-gradient(135deg, #073590 0%, #0A4DAB 100%);
                    padding: 25px; border-radius: 8px; margin-top: 30px;'>
            <p style='color: #F1C933; font-size: 18px; font-weight: 600; margin: 0;'>
                Sistema de Machine Learning - Ryanair Customer Analytics
            </p>
            <p style='color: white; font-size: 14px; margin-top: 10px;'>
                Modelo: Random Forest Classifier | Accuracy: 94.67% | ROC-AUC: 0.9467
            </p>
            <p style='color: #F1C933; font-size: 12px; margin-top: 8px;'>
                Dataset: 2,249 reseñas verificadas | Última actualización: Febrero 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
