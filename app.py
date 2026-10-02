import streamlit as st

st.title("Calculadora de Tarifas Flexibles - Centro de Entrenamiento")
st.write("Ingresa la cantidad de sesiones y el límite de semanas de vigencia para cotizar.")

# Entradas del usuario
sesiones = st.number_input("Cantidad de sesiones", min_value=1, max_value=50, value=8, step=1)
semanas = st.number_input("Límite de semanas de vigencia", min_value=1, max_value=52, value=4, step=1)

def calcular_tarifa_proporcional(sesiones, semanas):
    # Definir los tramos base oficiales según la imagen (4 semanas de referencia)
    # Tramos: (sesiones_base, precio_base)
    tramos = [
        (4, 180),   # 1 vez/sem[cite: 1]
        (8, 300),   # 2 veces/sem[cite: 1]
        (12, 380),  # 3 veces/sem[cite: 1]
        (16, 460),  # 4 veces/sem[cite: 1]
        (20, 520)   # 5 veces/sem[cite: 1]
    ]
    
    # Encontrar el tramo correspondiente por proporción lineal
    if sesiones <= 4:
        precio_base = (180 / 4) * sesiones
    elif sesiones <= 8:
        # Interpolación entre 4 y 8 sesiones
        precio_base = 180 + ((sesiones - 4) / (8 - 4)) * (300 - 180)
    elif sesiones <= 12:
        # Interpolación entre 8 y 12 sesiones
        precio_base = 300 + ((sesiones - 8) / (12 - 8)) * (380 - 300)
    elif sesiones <= 16:
        precio_base = 380 + ((sesiones - 12) / (16 - 12)) * (460 - 380)
    elif sesiones <= 20:
        precio_base = 460 + ((sesiones - 16) / (20 - 16)) * (520 - 460)
    else:
        # Proporción extendida para más de 20 sesiones
        precio_base = (520 / 20) * sesiones

    # Regla de aplazamiento / límites de semanas permitidas (máximo 25% extra por bloque de 4 semanas aprox)
    semanas_base_estimadas = max(4, round((sesiones / 4) * 4))
    semanas_maximas = semanas_base_estimadas * 1.25

    mensaje_tipo = "Ritmo Estándar / Flexible"
    descuento = 0.0

    # Beneficio por formato rápido (si consume en la mitad o menos del tiempo base estándar)
    if semanas <= (semanas_base_estimadas / 2) and semanas <= 2:
        descuento = 0.10  # 10% de descuento por alta intensidad / express
        mensaje_tipo = "¡Formato Express! (Descuento del 10% por alta intensidad)"
    elif semanas > semanas_maximas:
        return None, f"⚠️ El plazo de {semanas} semanas excede el límite máximo de aplazamiento permitido ({int(semanas_maximas)} semanas) para esta cantidad de sesiones."

    precio_final = precio_base * (1 - descuento)
    return precio_final, mensaje_tipo

# Botón y resultados
if st.button("Calcular Tarifa"):
    resultado, mensaje = calcular_tarifa_proporcional(sesiones, semanas)
    
    if resultado is None:
        st.error(mensaje)
    else:
        st.success(f"### Precio Total: S/ {resultado:,.2f}")
        st.info(f"**Detalle:** {mensaje}")