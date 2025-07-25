# 🚀 Uptrend Signals Pro

**Aplicación de Streamlit para detectar señales Uptrend en mercados financieros globales**

Una herramienta avanzada de análisis técnico que utiliza algoritmos cuantitativos para identificar oportunidades de inversión en acciones, ETFs, criptomonedas y pares de divisas.

## 📊 Demo en Vivo

🔗 **[Ver Aplicación](https://uptrends-signals.streamlit.app/)** 
## ✨ Características Principales

### 🎯 **Algoritmo Uptrend Cuantitativo**
Sistema de puntuación basado en 7 indicadores técnicos profesionales:

| Indicador | Puntos | Descripción |
|-----------|--------|-------------|
| **Precio vs Medias Móviles** | 25 pts | Precio > SMA20 > SMA50 |
| **Orden Alcista de MAs** | 20 pts | Medias móviles en tendencia alcista |
| **MACD Bullish** | 15 pts | MACD por encima de señal y positivo |
| **RSI Favorable** | 10 pts | RSI entre 30-70 (zona balanceada) |
| **Breakout Bollinger** | 15 pts | Precio rompiendo banda superior |
| **Tendencia Fuerte ADX** | 10 pts | ADX > 25 indica tendencia fuerte |
| **Confirmación Volumen** | 5 pts | Volumen por encima del promedio |

**🎯 Señal Uptrend:** Score ≥ 60 puntos

### 🌍 **Mercados Cubiertos**

- 📈 **Acciones US**: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, NFLX, AMD, CRM
- 🌍 **Acciones Globales**: ASML, TSM, BABA, Toyota, Nestlé, LVMH, SAP, Unilever
- 🏦 **ETFs**: SPY, QQQ, IWM, EFA, EEM, VTI, VEA, IEFA, VWO, AGG
- ₿ **Criptomonedas**: BTC, ETH, BNB, ADA, SOL, DOT, AVAX, MATIC, LINK, UNI
- 💱 **Forex**: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF

### 🛠️ **Funcionalidades**

- ✅ **Análisis en Tiempo Real** con datos de Yahoo Finance
- ✅ **Filtros Personalizables** por puntuación y categoría
- ✅ **Visualizaciones Interactivas** con Plotly
- ✅ **Análisis Técnico Detallado** del mejor símbolo
- ✅ **Estadísticas del Mercado** en tiempo real
- ✅ **Procesamiento Paralelo** para mejor rendimiento
- ✅ **Modo Demo** con datos simulados
- ✅ **Interfaz Moderna** y responsiva
- ✅ **Test de Conectividad** automático

## 🚀 Instalación y Uso

### **Opción 1: Streamlit Cloud (Recomendado)**

1. **Fork este repositorio** en GitHub
2. **Ve a [share.streamlit.io](https://share.streamlit.io)**
3. **Conecta tu repositorio** y especifica `uptrend_app.py`
4. **¡Listo!** La app se deployará automáticamente

### **Opción 2: Instalación Local**

```bash
# Clonar el repositorio
git clone https://github.com/diegocantillano/uptrend-signals.git
cd uptrend-signals

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run uptrend_app.py
```

### **Opción 3: Docker (Opcional)**

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "uptrend_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t uptrend-signals .
docker run -p 8501:8501 uptrend-signals
```

## 📱 Cómo Usar la Aplicación

### **1. Panel de Control**
- Selecciona las **categorías** de instrumentos a analizar
- Ajusta la **puntuación mínima** (recomendado: 60-80)
- Activa **"Mostrar todos"** para ver símbolos sin señal
- Usa **"Modo Demo"** si no tienes conexión a internet

### **2. Análisis de Resultados**
- **Tabla Principal**: Lista de señales ordenadas por puntuación
- **Métricas Generales**: Total analizados, % en uptrend
- **Distribución por Categoría**: Gráfico de barras interactivo
- **Análisis Detallado**: Gráfico técnico del mejor símbolo

### **3. Interpretación de Señales**

| Score | Interpretación | Acción Sugerida |
|-------|----------------|-----------------|
| 80-100 | 🟢 **Señal Muy Fuerte** | Considerar entrada |
| 60-79 | 🟡 **Señal Moderada** | Analizar más a fondo |
| 40-59 | 🟠 **Señal Débil** | Esperar confirmación |
| 0-39 | 🔴 **Sin Señal** | Evitar o considerar salida |

## 🧠 Metodología del Algoritmo

### **Base Teórica**
El algoritmo se basa en principios de análisis técnico reconocidos:

- **Teoría de Dow**: Tendencias confirmadas por múltiples indicadores
- **Análisis de Momentum**: RSI y MACD para fuerza del movimiento
- **Soporte/Resistencia**: Bandas de Bollinger para niveles clave
- **Confirmación de Volumen**: Validación institucional del movimiento

### **Scoring System**
```python
def calculate_uptrend_score(data):
    score = 0
    
    # Precio vs Medias Móviles (25 pts)
    if price > sma20 > sma50:
        score += 25
    
    # MACD Bullish (15 pts)
    if macd > macd_signal and macd > 0:
        score += 15
    
    # ... más condiciones
    
    return score >= 60  # Umbral de señal
```

## 📊 Ejemplos de Uso

### **Caso 1: Análisis S&P 500 Mega Cap**
```python
# Configuración para las empresas más grandes
categories = ['🏆 S&P 500 Mega Cap']
min_score = 75  # Más estricto para mega caps
show_all = False

# Resultado esperado
# NVDA: Score 88 ✅ (Tendencia muy fuerte)
# MSFT: Score 79 ✅ (Tendencia sólida)
# AAPL: Score 72 ✅ (Señal moderada)
```

### **Caso 2: Screening por Sectores**
```python
# Para análisis sectorial específico
categories = ['💻 Tech Leaders', '🧬 Biotech/Pharma']
min_score = 65
show_all = True

# Análisis comparativo entre sectores
# Identifica líderes sectoriales en uptrend
```

### **Caso 3: Cobertura Completa del Mercado**
```python
# Para análisis exhaustivo del mercado US
categories = [
    '🏆 S&P 500 Mega Cap',
    '📈 S&P 500 Large Cap', 
    '📊 S&P 500 Mid Cap',
    '🚀 NASDAQ Growth'
]
min_score = 60

# Análisis de 200+ acciones principales
# Vista panorámica del mercado
```

## 🛡️ Limitaciones y Disclaimers

### **⚠️ Advertencias Importantes**
- **No es asesoramiento financiero**: Solo para fines educativos
- **Datos históricos**: Rendimiento pasado no garantiza resultados futuros
- **Mercados volátiles**: Las señales pueden cambiar rápidamente
- **Verificación requerida**: Siempre confirma con análisis adicional

### **🔧 Limitaciones Técnicas**
- Dependiente de la calidad de datos de Yahoo Finance
- Requiere conexión a internet (excepto modo demo)
- Análisis basado en timeframe diario
- No incluye factores fundamentales

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. **Fork** el proyecto
2. **Crea una rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre un Pull Request**

### **Ideas para Contribuir**
- 📈 Añadir más indicadores técnicos
- 🌍 Incluir más mercados internacionales
- 📱 Mejorar la interfaz móvil
- 🔔 Sistema de alertas por email
- 📊 Backtesting histórico
- 🤖 Integración con APIs de brokers

## 📈 Roadmap

### **v2.0 (Próxima Versión)**
- [ ] Sistema de alertas por email/Telegram
- [ ] Backtesting histórico de señales
- [ ] Análisis de correlaciones entre activos
- [ ] Exportación a Excel/PDF
- [ ] API REST para integraciones

### **v3.0 (Futuro)**
- [ ] Machine Learning para optimizar scores
- [ ] Análisis de sentimiento de noticias
- [ ] Integración con brokers (paper trading)
- [ ] Dashboard ejecutivo personalizable

## 📞 Soporte y Contacto

- 🐛 **Reportar Bugs**: [Issues](https://github.com/diegocantillano/uptrend-signals/issues)
- 💡 **Sugerir Features**: [Discussions](https://github.com/diegocantillano/uptrend-signals/discussions)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **Yahoo Finance** por los datos de mercado
- **Streamlit** por la excelente plataforma
- **Plotly** por las visualizaciones interactivas
- **TA-Lib** por los indicadores técnicos
- **Comunidad Open Source** por la inspiración

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella ⭐**

**🚀 Hecho con ❤️ para la comunidad de trading**

[🔝 Volver arriba](#-uptrend-signals-pro)

</div>
