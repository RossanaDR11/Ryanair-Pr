# 🤖 App Interactiva de Machine Learning - Ryanair

## 📋 Descripción

Aplicación web interactiva que utiliza **Machine Learning** para predecir en tiempo real si un cliente recomendará Ryanair basándose en su experiencia de vuelo.

### ✨ Características Principales

1. **Predicción en Tiempo Real**
   - Ingresa calificaciones de los 5 aspectos del servicio
   - Obtén predicción instantánea: SÍ/NO recomendará
   - Visualización de probabilidades

2. **Modelo de ML**
   - Random Forest Classifier
   - Precisión: ~95%
   - ROC-AUC: 0.9467
   - Entrenado con 2,249 reseñas reales

3. **Análisis Visual**
   - Gráficos de probabilidad
   - Clasificación: Promotor/Neutral/Detractor
   - Evaluación por aspecto
   - Feature importance (importancia de cada aspecto)

4. **Interfaz Profesional**
   - Diseño moderno y responsive
   - Sliders interactivos para cada aspecto
   - Resultados visuales impactantes
   - Métricas del modelo en sidebar

---

## 🚀 Cómo Usar

### Opción 1: Script Automático (Más Fácil)
```bash
run_ml_app.bat
```

### Opción 2: Comando Manual
```bash
streamlit run src\ml_app.py --server.port 8502
```

La app se abrirá automáticamente en: **http://localhost:8502**

---

## 📊 Aspectos que Evalúa

La app predice recomendación basándose en 5 aspectos clave:

| Aspecto | Descripción | Impacto |
|---------|-------------|---------|
| **Seat Comfort** | Comodidad del asiento | ⭐⭐⭐ Medio |
| **Cabin Staff Service** | Servicio del personal de cabina | ⭐⭐⭐⭐ Alto |
| **Food & Beverages** | Calidad de comida y bebidas | ⭐⭐ Bajo |
| **Ground Service** | Servicio en tierra (check-in, etc.) | ⭐⭐⭐⭐⭐ Muy Alto |
| **Value For Money** | Relación calidad-precio | ⭐⭐⭐⭐ Alto |

---

## 🎯 Casos de Uso

### 1. **Presentación Ejecutiva**
- Demuestra capacidad predictiva del modelo
- Muestra en tiempo real cómo cada aspecto afecta la recomendación
- Ideal para explicar insights a stakeholders

### 2. **Simulación de Escenarios**
- ¿Qué pasa si mejoramos Ground Service de 2 a 4?
- ¿Cuánto impacta mejorar Cabin Staff Service?
- Prueba diferentes combinaciones

### 3. **Training de Personal**
- Muestra al equipo qué aspectos son más críticos
- Ayuda a priorizar mejoras
- Visualiza el impacto de cada área

---

## 📈 Ejemplo de Uso en Presentación

### Escenario 1: Cliente Insatisfecho
```
Seat Comfort: 2.0
Cabin Staff Service: 2.5
Food & Beverages: 1.0
Ground Service: 1.5
Value For Money: 2.0

Predicción: ❌ NO RECOMENDARÁ (85% probabilidad)
Clasificación: 🔴 Detractor
```

### Escenario 2: Cliente Satisfecho
```
Seat Comfort: 4.0
Cabin Staff Service: 5.0
Food & Beverages: 3.0
Ground Service: 4.5
Value For Money: 5.0

Predicción: ✅ SÍ RECOMENDARÁ (92% probabilidad)
Clasificación: 🟢 Promotor
```

### Escenario 3: Cliente en el Límite
```
Seat Comfort: 3.0
Cabin Staff Service: 3.5
Food & Beverages: 2.5
Ground Service: 3.0
Value For Money: 3.5

Predicción: Depende del modelo
Clasificación: 🟡 Neutral
```

---

## 🎨 Capturas de Funcionalidades

### Panel Principal
- Sliders para cada aspecto (1-5)
- Botón de predicción destacado
- Tipo de viajero (opcional)

### Resultado de Predicción
- Box grande con resultado (SÍ/NO)
- Porcentaje de probabilidad
- Clasificación (Promotor/Neutral/Detractor)
- Gráfico de barras con probabilidades

### Análisis Detallado
- Gráfico de evaluación por aspecto
- Recomendaciones personalizadas
- Identificación de fortalezas y debilidades

### Feature Importance
- Ranking de aspectos más importantes
- Gráfico de importancia
- Porcentajes de impacto

---

## 🔧 Personalización

### Cambiar Modelo
Si tienes ambos modelos (Random Forest y Logistic Regression), puedes seleccionar entre ellos en el sidebar.

### Ajustar Valores por Defecto
Edita en `ml_app.py` las líneas:
```python
value=3.0  # Cambiar valor inicial del slider
```

### Añadir Más Aspectos
Si quieres incluir más variables (tipo de viajero, país, etc.), modifica la sección de preparación de datos.

---

## 📊 Métricas del Modelo

### Random Forest (Recomendado)
- **Accuracy:** 94.67%
- **Precision:** 90.14%
- **Recall:** 91.03%
- **F1-Score:** 90.58%
- **ROC-AUC:** 0.9467

### Interpretación
- **Accuracy 94.67%:** El modelo acierta el 94.67% de las veces
- **ROC-AUC 0.9467:** Excelente capacidad de discriminación (>0.9 es excelente)
- **F1-Score 90.58%:** Buen balance entre precisión y recall

---

## 💡 Tips para la Presentación

### 1. **Empieza con un Caso Extremo**
- Pon todos los valores en 1-2 → Mostrará claramente NO RECOMIENDA
- Cambia Ground Service de 1 a 5 → Muestra el impacto

### 2. **Demuestra Feature Importance**
- Explica que Ground Service es el aspecto más crítico
- Muestra que mejorar este aspecto tiene mayor ROI

### 3. **Usa Casos Reales**
- Prepara 2-3 perfiles de clientes típicos
- Muestra cómo el modelo predice correctamente

### 4. **Interacción con la Audiencia**
- Pide que sugieran valores
- Haz predicciones en vivo

---

## 🔍 Solución de Problemas

### El modelo no carga
```bash
# Entrenar el modelo primero
python run_ml_analysis.py
```

### La app no inicia
```bash
# Verificar que Streamlit está instalado
pip install streamlit

# Ejecutar manualmente
streamlit run src\ml_app.py --server.port 8502
```

### Puerto 8502 ocupado
```bash
# Cambiar puerto
streamlit run src\ml_app.py --server.port 8503
```

---

## 📚 Archivos Relacionados

- `src/ml_app.py` - Código de la aplicación
- `run_ml_app.bat` - Script de inicio
- `ryanair_recommendation_model.pkl` - Modelo Random Forest
- `ryanair_scaler.pkl` - Escalador de datos
- `ryanair_feature_importance.csv` - Importancia de features
- `ryanair_ml_results.csv` - Métricas del modelo

---

## 🎓 Conceptos Técnicos (Para Presentación)

### ¿Qué es Random Forest?
- Conjunto de múltiples árboles de decisión
- Cada árbol "vota" y se toma la decisión mayoritaria
- Más robusto que un solo árbol

### ¿Cómo Funciona?
1. Se entrena con 2,249 reseñas históricas
2. Aprende patrones: qué combinaciones llevan a recomendación
3. Cuando ingresas nuevos valores, predice basándose en patrones aprendidos

### ¿Por Qué 95% de Precisión?
- Modelo bien entrenado con datos reales
- Balance adecuado entre variables
- Validación con datos de prueba (20% del dataset)

---

## ✅ Checklist Pre-Presentación

- [ ] Ejecutar `run_ml_app.bat` y verificar que carga
- [ ] Probar 2-3 escenarios diferentes
- [ ] Verificar que los gráficos se muestran correctamente
- [ ] Preparar historia: "Este es un cliente típico con..."
- [ ] Tener datos de backup por si internet falla
- [ ] Screenshot de la app como backup

---

## 🚀 Siguiente Nivel

### Ideas para Expandir:
1. **Añadir más variables:** País, tipo de viajero, ruta
2. **Predicción de Overall Rating:** No solo recomendación, también rating numérico
3. **Análisis SHAP:** Explicaciones más detalladas de cada predicción
4. **API REST:** Convertir en API para integración con sistemas
5. **Batch Predictions:** Subir CSV y predecir para múltiples clientes

---

**🎉 ¡Listo para Presentar!**

Esta app demuestra aplicación práctica de Machine Learning en experiencia del cliente.

*Creado con Streamlit + Random Forest | Ryanair Customer Analytics*
