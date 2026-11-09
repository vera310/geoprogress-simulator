import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Настройка шрифтов для корректного отображения кириллицы на графиках
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Настройка страницы
st.set_page_config(page_title="GeoProgress Simulator", layout="wide")
st.title("GeoProgress Simulator")
st.markdown("Интерактивный симулятор геометрической прогрессии в природе и экономике.")

# Создаем вкладки для трех моделей
tab1, tab2, tab3 = st.tabs(["💰 Финансы (Сложный процент)", "🦠 Эпидемия (Модель SIR)", "🌱 Экология (Логистический рост)"])

# ==========================================
# ВКЛАДКА 1: ФИНАНСЫ
# ==========================================
with tab1:
    st.header("Сложный vs Простой процент")
    st.markdown("Сравнение арифметической и геометрической прогрессии в финансах.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Параметры:")
        principal = st.slider("Начальная сумма (₽)", 1000, 100000, 10000, step=1000)
        rate = st.slider("Годовая ставка (%)", 1, 30, 10)
        years = st.slider("Количество лет", 1, 50, 10)
    
    with col2:
        # Расчеты
        n = np.arange(0, years + 1)
        simple = principal + principal * (rate / 100) * n
        compound = principal * (1 + rate / 100) ** n
        
        # Построение графика
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(n, simple, label="Простой процент (Арифметическая прогрессия)", color='blue', linewidth=2)
        ax1.plot(n, compound, label="Сложный процент (Геометрическая прогрессия)", color='green', linewidth=2)
        ax1.set_xlabel("Год")
        ax1.set_ylabel("Сумма (₽)")
        ax1.set_title("Рост капитала во времени")
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig1)

# ==========================================
# ВКЛАДКА 2: ЭПИДЕМИЯ
# ==========================================
with tab2:
    st.header("Модель распространения инфекции")
    st.markdown("Упрощенная модель SIR (Восприимчивые - Инфицированные - Выздоровевшие).")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Параметры:")
        initial_infected = st.slider("Начальное число заражённых", 1, 100, 1)
        r0 = st.slider("Коэффициент заражения (R0)", 1.0, 5.0, 2.0, step=0.1)
        duration = st.slider("Длительность инфекции (дней)", 1, 14, 7)
        days_to_simulate = st.slider("Дней для симуляции", 10, 60, 30)
        
    with col2:
        # Расчеты (упрощенная модель на основе формул из Excel)
        days = np.arange(0, days_to_simulate + 1)
        
        # В формулах Excel: Зараженные = старые * R0, Выздоровевшие = старые + (начальные / длительность) * дни
        infected = initial_infected * (r0 ** days)
        recovered = (initial_infected / duration) * days
        active = infected - recovered
        
        # Защита от отрицательных значений на графике
        active = np.maximum(active, 0)
        
        # Построение графика
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(days, infected, label="Всего заражённых (Геом. прогрессия)", color='red', linewidth=2)
        ax2.plot(days, active, label="Активные больные", color='orange', linewidth=2)
        ax2.plot(days, recovered, label="Выздоровевшие", color='green', linewidth=2)
        ax2.set_xlabel("День")
        ax2.set_ylabel("Количество человек")
        ax2.set_title("Динамика эпидемии")
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig2)

# ==========================================
# ВКЛАДКА 3: ЭКОЛОГИЯ
# ==========================================
with tab3:
    st.header("Логистический рост популяции")
    st.markdown("Рост популяции, ограниченный ресурсами среды (ёмкостью).")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Параметры:")
        initial_pop = st.slider("Начальная популяция", 1, 100, 10)
        growth_rate = st.slider("Коэффициент роста (r)", 0.1, 1.0, 0.5, step=0.1)
        capacity = st.slider("Ёмкость среды (K)", 100, 2000, 1000, step=100)
        years_eco = st.slider("Лет для симуляции", 10, 100, 50)
        
    with col2:
        # Расчеты
        years_array = np.arange(0, years_eco + 1)
        population = np.zeros(len(years_array))
        population[0] = initial_pop
        
        for i in range(1, len(years_array)):
            # Формула: P + r * P * (1 - P/K)
            p_prev = population[i-1]
            population[i] = p_prev + growth_rate * p_prev * (1 - p_prev / capacity)
            
        # Построение графика
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(years_array, population, label="Популяция (Логистическая кривая)", color='forestgreen', linewidth=3)
        ax3.axhline(y=capacity, color='gray', linestyle='--', label="Ёмкость среды (K)")
        ax3.set_xlabel("Год")
        ax3.set_ylabel("Численность")
        ax3.set_title("Экологический рост популяции")
        ax3.legend()
        ax3.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig3)