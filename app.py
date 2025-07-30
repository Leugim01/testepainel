# app.py (Painel FuelTech adaptado para web com Streamlit)

import streamlit as st
import time
import random
import math
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(layout="centered", page_title="Painel FuelTech MVP")

st.markdown("<h1 style='text-align: center;'>Painel FuelTech MVP</h1>", unsafe_allow_html=True)

# Entradas iniciais
with st.sidebar:
    st.header("Configuração Inicial")
    consumo = st.number_input("Quantos km por litro sua moto faz?", min_value=1.0, value=25.0)
    preco_gasolina = st.number_input("Qual o preço da gasolina por litro (R$)?", min_value=0.0, value=5.0)

# Estado inicial (usando session_state)
if 'aem_ativo' not in st.session_state:
    st.session_state.aem_ativo = True
if 'velocidade' not in st.session_state:
    st.session_state.velocidade = 0.0
if 'economia_total' not in st.session_state:
    st.session_state.economia_total = 0.0
if 'km_percorrido' not in st.session_state:
    st.session_state.km_percorrido = 0.0

# Atualização da economia
economia_percentual = 0.2 if st.session_state.aem_ativo else 0.0
consumo_economico = consumo / (1 - economia_percentual)
economia_por_km = preco_gasolina * (1 / consumo - 1 / consumo_economico)
economia_mensal = economia_por_km * 2000

# Velocímetro
st.write("### ")
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(4, 2.2), subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location('W')
ax.set_theta_direction(-1)
ax.set_thetamin(0)
ax.set_thetamax(180)

for i in range(0, 181, 22):
    theta = np.deg2rad(i)
    ax.plot([theta, theta], [0.9, 1.0], color='gray', lw=2)

ponteiro_theta = np.deg2rad((st.session_state.velocidade / 120) * 180)
ax.plot([ponteiro_theta, ponteiro_theta], [0, 0.85], color='blue', lw=5)

ax.set_yticklabels([])
ax.set_xticklabels([])
ax.spines['polar'].set_visible(False)
ax.grid(False)
ax.set_facecolor('white')
st.pyplot(fig)

# Velocidade numérica
vel = int(st.session_state.velocidade)
cor_vel = "#00008B"
st.markdown(f"<h1 style='text-align: center; color:{cor_vel};'>{vel:03d}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>km/h</p>", unsafe_allow_html=True)

# Simulação dinâmica
rpm = int((st.session_state.velocidade / 85) * 11000)
tps = random.randint(10, 70)
potencia = round((tps / 100) * 100, 1)
marcha = min(1 + int(st.session_state.velocidade) // 15, 5)
km_por_seg = st.session_state.velocidade / 3600
st.session_state.km_percorrido += km_por_seg * 1
litros = (km_por_seg * 1) / consumo
eco_litros = litros * economia_percentual
eco_reais = eco_litros * preco_gasolina
st.session_state.economia_total += eco_reais

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("RPM", rpm)
col2.metric("GEAR", marcha)
col3.metric("TPS", f"{tps}%")
col4, col5, col6 = st.columns(3)
col4.metric("ECONOMY", f"R$ {st.session_state.economia_total:.2f}")
col5.metric("POWER", f"{potencia}%")
col6.metric("DISTANCE", f"{st.session_state.km_percorrido:.2f} km")

st.write("---")
st.markdown(f"<p style='text-align: center;'>Consumo original: {consumo:.2f} km/l &nbsp;&nbsp;&nbsp; Com economia: {consumo_economico:.2f} km/l</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Economia por km: R$ {economia_por_km:.3f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color:green'>Projeção mensal: R$ {economia_mensal:.2f}</p>", unsafe_allow_html=True)

# Botões
col7, col8, col9 = st.columns([1, 2, 1])
with col8:
    if st.button("Desligar AEM" if st.session_state.aem_ativo else "Ligar AEM"):
        st.session_state.aem_ativo = not st.session_state.aem_ativo
        st.rerun()

col10, col11, col12 = st.columns([1, 1, 1])
if col10.button("\U0001F53C Acelerar"):
    st.session_state.velocidade = min(st.session_state.velocidade + 1, 120)
if col11.button("\U0001F53D Frear"):
    st.session_state.velocidade = max(st.session_state.velocidade - 2, 0)

# Atualiza a cada execução
st.experimental_rerun()
