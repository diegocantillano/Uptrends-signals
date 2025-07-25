import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import warnings
import requests
import json
warnings.filterwarnings('ignore')

# Instalación automática de dependencias si no están disponibles
try:
    import yfinance as yf
except ImportError:
    st.error("📦 Installing yfinance...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf

try:
    import ta
except ImportError:
    st.error("📦 Installing ta...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ta"])
    import ta

# Configuración de la página
st.set_page_config(
    page_title="🚀 Uptrend Signals Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .uptrend-signal {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .sidebar-info {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class UptrendAnalyzer:
    def __init__(self):
        self.symbols = {
            # S&P 500 - Top 100 por capitalización de mercado (2025)
            'sp500_mega_cap': [
                'NVDA', 'MSFT', 'AAPL', 'GOOGL', 'GOOG', 'AMZN', 'META', 'TSLA', 'BRK.B', 'AVGO',
                'LLY', 'WMT', 'JPM', 'UNH', 'XOM', 'ORCL', 'MA', 'COST', 'HD', 'PG',
                'NFLX', 'JNJ', 'BAC', 'CRM', 'ABBV', 'CVX', 'KO', 'AMD', 'PEP', 'TMO',
                'MRK', 'WFC', 'LIN', 'CSCO', 'ACN', 'DIS', 'ABT', 'VZ', 'ADBE', 'DHR',
                'TXN', 'PM', 'CMCSA', 'INTC', 'NKE', 'PFE', 'COP', 'NOW', 'QCOM', 'SPGI'
            ],
            
            # S&P 500 - Large Cap (51-150)
            'sp500_large_cap': [
                'AMAT', 'CAT', 'INTU', 'UNP', 'GE', 'BKNG', 'T', 'LOW', 'TJX', 'PLD',
                'UBER', 'AXP', 'UPS', 'RTX', 'BMY', 'ISRG', 'MS', 'SCHW', 'NEE', 'HON',
                'MU', 'BLK', 'SYK', 'ELV', 'DE', 'AMGN', 'LMT', 'PGR', 'VRTX', 'ADI',
                'IBM', 'GILD', 'MDLZ', 'TGT', 'CI', 'CB', 'BSX', 'SO', 'REGN', 'CL',
                'TMUS', 'PYPL', 'PANW', 'LRCX', 'AON', 'CME', 'ITW', 'SHW', 'ZTS', 'APH'
            ],
            
            # S&P 500 - Mid Cap (151-300)
            'sp500_mid_cap': [
                'CDNS', 'SNPS', 'MMC', 'CSX', 'PNC', 'ICE', 'APD', 'WM', 'ORLY', 'FCX',
                'KLAC', 'TFC', 'F', 'ECL', 'NSC', 'USB', 'GM', 'EMR', 'MCO', 'HCA',
                'DUK', 'EOG', 'FDX', 'WELL', 'GD', 'TDG', 'SLB', 'PSA', 'AJG', 'BDX',
                'CARR', 'OXY', 'ADSK', 'EW', 'TRV', 'PCAR', 'ROP', 'NXPI', 'CMG', 'CNC',
                'NOC', 'AFL', 'JCI', 'O', 'AEP', 'ROST', 'SRE', 'PAYX', 'EXC', 'KMB'
            ],
            
            # S&P 500 - Small-Mid Cap (301-500)
            'sp500_small_cap': [
                'FAST', 'CTAS', 'EA', 'ODFL', 'KR', 'AMT', 'BK', 'GLW', 'VRSK', 'A',
                'DOW', 'CTSH', 'IT', 'FANG', 'VMC', 'EXR', 'MCHP', 'SPG', 'GWW', 'XEL',
                'DD', 'WY', 'VICI', 'KMI', 'MSCI', 'HPQ', 'PWR', 'CPRT', 'IQV', 'MPWR',
                'DXCM', 'YUM', 'ANSS', 'GEHC', 'IDXX', 'CMI', 'GRMN', 'RMD', 'ED', 'WTW',
                'ROK', 'OTIS', 'IR', 'ALL', 'FICO', 'EFX', 'ACGL', 'TRGP', 'HSY', 'HIG'
            ],
            
            # NASDAQ Growth Stocks (no incluidas en S&P 500)
            'nasdaq_growth': [
                'QQQ', 'SQQQ', 'TQQQ', 'ARKK', 'ARKQ', 'ARKG', 'SHOP', 'ROKU', 'ZM', 'DOCU',
                'SNOW', 'CRWD', 'OKTA', 'DDOG', 'NET', 'FSLY', 'TWLO', 'PLTR', 'COIN', 'HOOD',
                'RBLX', 'U', 'PATH', 'DASH', 'ABNB', 'PINS', 'SNAP', 'SPOT', 'SQ', 'PYPL'
            ],
            
            # NYSE Blue Chips y Industriales
            'nyse_industrials': [
                'BA', 'MMM', 'GS', 'MCD', 'IBM', 'DIS', 'DD', 'CAT', 'XOM', 'CVX',
                'PG', 'JNJ', 'KO', 'MRK', 'PFE', 'WMT', 'T', 'VZ', 'NKE', 'HD',
                'BAC', 'C', 'JPM', 'WFC', 'USB', 'PNC', 'TFC', 'COF', 'AXP', 'BLK'
            ],
            
            # Sectores Específicos
            'tech_leaders': [
                'NVDA', 'MSFT', 'AAPL', 'GOOGL', 'META', 'TSLA', 'AMZN', 'NFLX', 'CRM', 'ORCL',
                'AMD', 'INTC', 'QCOM', 'AVGO', 'TXN', 'ADI', 'LRCX', 'KLAC', 'AMAT', 'MU'
            ],
            
            'biotech_pharma': [
                'LLY', 'JNJ', 'PFE', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN',
                'GILD', 'VRTX', 'REGN', 'ZTS', 'BDX', 'EW', 'SYK', 'BSX', 'ISRG', 'DXCM'
            ],
            
            'financial_services': [
                'BRK.B', 'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC',
                'SCHW', 'BLK', 'SPGI', 'ICE', 'CME', 'MCO', 'AON', 'MMC', 'AJG', 'CB'
            ],
            
            'energy_utilities': [
                'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'OXY', 'FANG', 'KMI', 'TRGP', 'FCX',
                'NEE', 'SO', 'DUK', 'AEP', 'EXC', 'XEL', 'ED', 'SRE', 'D', 'NGG'
            ],
            
            'consumer_retail': [
                'WMT', 'COST', 'HD', 'LOW', 'TGT', 'TJX', 'NKE', 'SBUX', 'MCD', 'CMG',
                'YUM', 'KR', 'DG', 'DLTR', 'WBA', 'CVS', 'ROST', 'ORLY', 'AZO', 'AAP'
            ],
            
            # Mantenemos categorías internacionales
            'stocks_global': ['ASML', 'TSM', 'BABA', 'TM', 'NVO', 'NESN.SW', 'MC.PA', 'OR.PA', 'SAP', 'UL'],
            'etfs': ['SPY', 'QQQ', 'IWM', 'EFA', 'EEM', 'VTI', 'VEA', 'IEFA', 'VWO', 'AGG'],
            'crypto': ['BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'SOL-USD', 'DOT-USD', 'AVAX-USD', 'MATIC-USD', 'LINK-USD', 'UNI-USD'],
            'forex': ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X', 'USDCHF=X', 'NZDUSD=X', 'EURGBP=X', 'EURJPY=X', 'GBPJPY=X']
        }
    
    def get_data(self, symbol, period='6mo'):
        """Obtiene datos históricos del símbolo"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            if data.empty:
                return None
            return data
        except Exception as e:
            # En caso de error, generar datos simulados para demostración
            if st.session_state.get('demo_mode', False):
                return self.generate_demo_data(symbol)
            st.warning(f"Error obteniendo datos para {symbol}: {str(e)}")
            return None
    
    def generate_demo_data(self, symbol):
        """Genera datos simulados para demostración"""
        try:
            dates = pd.date_range(start=datetime.now() - timedelta(days=180), 
                                end=datetime.now(), freq='D')
            np.random.seed(hash(symbol) % 2147483647)  # Seed basado en el símbolo
            
            # Generar datos simulados con tendencia alcista
            base_price = 100 + np.random.uniform(-50, 200)
            returns = np.random.normal(0.001, 0.02, len(dates))  # Tendencia alcista leve
            prices = [base_price]
            
            for ret in returns[1:]:
                prices.append(prices[-1] * (1 + ret))
            
            # Crear DataFrame con formato de yfinance
            data = pd.DataFrame({
                'Open': prices,
                'High': [p * (1 + np.random.uniform(0, 0.03)) for p in prices],
                'Low': [p * (1 - np.random.uniform(0, 0.03)) for p in prices],
                'Close': prices,
                'Volume': np.random.randint(1000000, 10000000, len(dates))
            }, index=dates)
            
            # Ajustar High y Low para que sean consistentes
            data['High'] = np.maximum(data[['Open', 'Close']].max(axis=1), data['High'])
            data['Low'] = np.minimum(data[['Open', 'Close']].min(axis=1), data['Low'])
            
            return data
        except Exception as e:
            st.error(f"Error generando datos demo: {str(e)}")
            return None
    
    def calculate_indicators(self, data):
        """Calcula indicadores técnicos"""
        try:
            # Medias móviles
            data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
            data['SMA_50'] = ta.trend.sma_indicator(data['Close'], window=50)
            data['EMA_12'] = ta.trend.ema_indicator(data['Close'], window=12)
            data['EMA_26'] = ta.trend.ema_indicator(data['Close'], window=26)
            
            # MACD
            data['MACD'] = ta.trend.macd_diff(data['Close'])
            data['MACD_Signal'] = ta.trend.macd_signal(data['Close'])
            
            # RSI
            data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
            
            # Bandas de Bollinger
            bollinger = ta.volatility.BollingerBands(data['Close'])
            data['BB_High'] = bollinger.bollinger_hband()
            data['BB_Low'] = bollinger.bollinger_lband()
            data['BB_Mid'] = bollinger.bollinger_mavg()
            
            # ADX para fuerza de tendencia
            data['ADX'] = ta.trend.adx(data['High'], data['Low'], data['Close'])
            
            # Volume indicators
            data['Volume_SMA'] = data['Volume'].rolling(window=20).mean()
            
            return data
        except Exception as e:
            st.error(f"Error calculando indicadores: {str(e)}")
            return data
    
    def detect_uptrend_signal(self, data):
        """Detecta señales de uptrend basadas en condiciones cuantitativas"""
        if data is None or len(data) < 50:
            return False, 0, {}
        
        try:
            latest = data.iloc[-1]
            prev = data.iloc[-2]
            
            signals = {}
            score = 0
            
            # 1. Precio por encima de medias móviles (25 puntos)
            if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
                signals['price_above_ma'] = True
                score += 25
            
            # 2. Medias móviles en orden alcista (20 puntos)
            if latest['SMA_20'] > latest['SMA_50']:
                signals['ma_bullish_order'] = True
                score += 20
            
            # 3. MACD por encima de señal y en territorio positivo (15 puntos)
            if latest['MACD'] > latest['MACD_Signal'] and latest['MACD'] > 0:
                signals['macd_bullish'] = True
                score += 15
            
            # 4. RSI en zona favorable (30-70) (10 puntos)
            if 30 < latest['RSI'] < 70:
                signals['rsi_favorable'] = True
                score += 10
            
            # 5. Precio rompiendo banda de Bollinger superior (15 puntos)
            if latest['Close'] > latest['BB_High']:
                signals['bb_breakout'] = True
                score += 15
            
            # 6. ADX indica tendencia fuerte (>25) (10 puntos)
            if latest['ADX'] > 25:
                signals['strong_trend'] = True
                score += 10
            
            # 7. Volumen por encima del promedio (5 puntos)
            if latest['Volume'] > latest['Volume_SMA']:
                signals['volume_confirmation'] = True
                score += 5
            
            # Señal de uptrend si score >= 60
            is_uptrend = score >= 60
            
            return is_uptrend, score, signals
            
        except Exception as e:
            st.error(f"Error detectando señal: {str(e)}")
            return False, 0, {}
    
    def analyze_symbol(self, symbol):
        """Analiza un símbolo completo"""
        data = self.get_data(symbol)
        if data is None:
            return None
        
        data = self.calculate_indicators(data)
        is_uptrend, score, signals = self.detect_uptrend_signal(data)
        
        latest_price = data['Close'].iloc[-1]
        price_change = ((latest_price - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
        
        return {
            'symbol': symbol,
            'price': latest_price,
            'change_pct': price_change,
            'is_uptrend': is_uptrend,
            'score': score,
            'signals': signals,
            'data': data
        }

def main():
    st.markdown('<h1 class="main-header">🚀 Uptrend Signals Pro</h1>', unsafe_allow_html=True)
    
    # Inicializar session state
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False
    
    analyzer = UptrendAnalyzer()
    
    # Sidebar
    st.sidebar.markdown('<div class="sidebar-info"><h3>📊 Panel de Control</h3></div>', unsafe_allow_html=True)
    
    # Modo demo para cuando no hay conexión a internet
    demo_mode = st.sidebar.checkbox(
        "🧪 Modo Demo (datos simulados)", 
        value=st.session_state.demo_mode,
        help="Usa datos simulados si no tienes conexión a internet"
    )
    st.session_state.demo_mode = demo_mode
    
    if demo_mode:
        st.sidebar.warning("⚠️ Usando datos simulados para demostración")
    
    # Selección de categorías
    categories = {
        '🏆 S&P 500 Mega Cap': 'sp500_mega_cap',
        '📈 S&P 500 Large Cap': 'sp500_large_cap', 
        '📊 S&P 500 Mid Cap': 'sp500_mid_cap',
        '🔹 S&P 500 Small Cap': 'sp500_small_cap',
        '🚀 NASDAQ Growth': 'nasdaq_growth',
        '🏭 NYSE Industrials': 'nyse_industrials',
        '💻 Tech Leaders': 'tech_leaders',
        '🧬 Biotech/Pharma': 'biotech_pharma',
        '🏦 Financial Services': 'financial_services',
        '⚡ Energy/Utilities': 'energy_utilities',
        '🛍️ Consumer/Retail': 'consumer_retail',
        '🌍 Global Stocks': 'stocks_global',
        '📊 ETFs': 'etfs',
        '₿ Crypto': 'crypto',
        '💱 Forex': 'forex'
    }
    
    selected_categories = st.sidebar.multiselect(
        "Selecciona categorías a analizar:",
        list(categories.keys()),
        default=['🏆 S&P 500 Mega Cap', '💻 Tech Leaders']
    )
    
    # Configuración de filtros
    min_score = st.sidebar.slider("Puntuación mínima para señal:", 0, 100, 60)
    show_all = st.sidebar.checkbox("Mostrar todos los símbolos (no solo uptrends)")
    
    if st.sidebar.button("🔄 Actualizar Análisis", type="primary"):
        st.rerun()
    
    # Test de conexión
    if not demo_mode:
        with st.sidebar:
            if st.button("🔍 Test Conexión"):
                with st.spinner("Probando conexión..."):
                    test_result = analyzer.analyze_symbol('AAPL')
                    if test_result:
                        st.success("✅ Conexión OK")
                    else:
                        st.error("❌ Sin conexión - Activa modo demo")
    
    # Información sobre el algoritmo
    with st.sidebar.expander("ℹ️ Sobre el Algoritmo Uptrend"):
        st.write("""
        **Condiciones para señal Uptrend:**
        - Precio > SMA20 > SMA50 (25 pts)
        - Orden alcista de MAs (20 pts)
        - MACD bullish (15 pts)
        - RSI 30-70 (10 pts)
        - Breakout Bollinger (15 pts)
        - ADX > 25 (10 pts)
        - Volumen alto (5 pts)
        
        **Señal:** Score ≥ 60 puntos
        """)
    
    if not selected_categories:
        st.warning("⚠️ Selecciona al menos una categoría para analizar.")
        return
    
    # Análisis principal
    with st.spinner("🔍 Analizando mercados..."):
        all_results = []
        
        for cat_name in selected_categories:
            cat_key = categories[cat_name]
            symbols = analyzer.symbols[cat_key]
            
            # Análisis paralelo para mejor rendimiento
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(analyzer.analyze_symbol, symbols))
            
            valid_results = [r for r in results if r is not None]
            
            for result in valid_results:
                result['category'] = cat_name
                all_results.append(result)
    
    if not all_results:
        st.error("❌ No se pudieron obtener datos. Verifica tu conexión a internet.")
        return
    
    # Filtrar resultados
    if not show_all:
        filtered_results = [r for r in all_results if r['is_uptrend'] and r['score'] >= min_score]
    else:
        filtered_results = [r for r in all_results if r['score'] >= min_score]
    
    # Estadísticas generales
    total_analyzed = len(all_results)
    uptrend_count = len([r for r in all_results if r['is_uptrend']])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Analizados", total_analyzed)
    
    with col2:
        st.metric("🚀 Señales Uptrend", uptrend_count)
    
    with col3:
        percentage = (uptrend_count / total_analyzed * 100) if total_analyzed > 0 else 0
        st.metric("📈 % en Uptrend", f"{percentage:.1f}%")
    
    with col4:
        st.metric("🎯 Filtrados", len(filtered_results))
    
    # Mostrar resultados
    if filtered_results:
        st.subheader("🎯 Señales Detectadas")
        
        # Ordenar por score
        filtered_results.sort(key=lambda x: x['score'], reverse=True)
        
        # Crear DataFrame para mostrar
        display_data = []
        for result in filtered_results:
            signals_text = ", ".join([k.replace('_', ' ').title() for k, v in result['signals'].items() if v])
            
            display_data.append({
                'Símbolo': result['symbol'],
                'Categoría': result['category'],
                'Precio': f"${result['price']:.2f}",
                'Cambio %': f"{result['change_pct']:+.2f}%",
                'Score': result['score'],
                'Uptrend': "✅" if result['is_uptrend'] else "⚠️",
                'Señales Activas': signals_text[:50] + "..." if len(signals_text) > 50 else signals_text
            })
        
        df_display = pd.DataFrame(display_data)
        
        # Mostrar tabla con formato
        st.dataframe(
            df_display,
            use_container_width=True,
            column_config={
                'Score': st.column_config.ProgressColumn(
                    'Score',
                    help='Puntuación del algoritmo Uptrend',
                    min_value=0,
                    max_value=100,
                ),
                'Cambio %': st.column_config.NumberColumn(
                    'Cambio %',
                    format="%.2f%%"
                )
            }
        )
        
        # Gráfico de distribución por categoría
        st.subheader("📊 Distribución por Categoría")
        
        category_counts = pd.DataFrame(filtered_results).groupby('category').size().reset_index(name='count')
        
        fig_bar = px.bar(
            category_counts,
            x='category',
            y='count',
            title='Señales Uptrend por Categoría',
            color='count',
            color_continuous_scale='viridis'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Análisis detallado del mejor símbolo
        if filtered_results:
            st.subheader("🏆 Análisis Detallado - Mejor Señal")
            
            best_result = filtered_results[0]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gráfico de precio
                data = best_result['data']
                fig = go.Figure()
                
                # Precio
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode='lines',
                    name='Precio',
                    line=dict(color='blue', width=2)
                ))
                
                # Medias móviles
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['SMA_20'],
                    mode='lines',
                    name='SMA 20',
                    line=dict(color='orange', width=1)
                ))
                
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['SMA_50'],
                    mode='lines',
                    name='SMA 50',
                    line=dict(color='red', width=1)
                ))
                
                # Bandas de Bollinger
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['BB_High'],
                    mode='lines',
                    name='BB Superior',
                    line=dict(color='gray', dash='dash', width=1)
                ))
                
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['BB_Low'],
                    mode='lines',
                    name='BB Inferior',
                    line=dict(color='gray', dash='dash', width=1),
                    fill='tonexty',
                    fillcolor='rgba(128,128,128,0.1)'
                ))
                
                fig.update_layout(
                    title=f'{best_result["symbol"]} - Análisis Técnico',
                    xaxis_title='Fecha',
                    yaxis_title='Precio',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{best_result['symbol']}</h4>
                    <p><strong>Precio:</strong> ${best_result['price']:.2f}</p>
                    <p><strong>Cambio:</strong> {best_result['change_pct']:+.2f}%</p>
                    <p><strong>Score:</strong> {best_result['score']}/100</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("**Señales Activas:**")
                for signal, active in best_result['signals'].items():
                    if active:
                        signal_name = signal.replace('_', ' ').title()
                        st.write(f"✅ {signal_name}")
    
    else:
        st.info("🔍 No se encontraron señales Uptrend con los filtros actuales. Prueba reducir la puntuación mínima.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🚀 Uptrend Signals Pro | Análisis Cuantitativo en Tiempo Real</p>
        <p><small>⚠️ Este análisis es solo para fines educativos. No constituye asesoramiento financiero.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
