import streamlit as st

st.title("Calculadora de Tarifas Flexibles - Centro de Entrenamiento")
st.write("Cotizador basado en el tarifario oficial y proporciones por sesión con límites de aplazamiento.")

sesiones = st.number_input("Cantidad de sesiones", min_value=1, max_value=50, value=4, step=1)
semanas = st.number_input("Límite de semanas de vigencia", min_value=1, max_value=52, value=4, step=1)

def calcular_tarifa_oficial_flexible(sesiones, semanas):
    # Determinamos el precio unitario de referencia según la densidad de sesiones por semana base (asumiendo 4 semanas de tiempo base)
    densidad_base = sesiones / 4.0
    
    if densidad_base <= 1.0:
        precio_unitario = 180.0 / 4.0  # S/ 45.00
        semanas_max_toleradas = 5     # 4 a 5 semanas cuesta lo mismo (S/ 180)
    elif densidad_base <= 2.0:
        precio_unitario = 300.0 / 8.0  # S/ 37.50
        semanas_max_toleradas = 5     # 4 a 5 semanas cuesta lo mismo (S/ 300)
    elif densidad_base <= 3.0:
        precio_unitario = 380.0 / 12.0 # S/ 31.67
        semanas_max_toleradas = 6     # Hasta 6 semanas mantiene el precio base
    elif densidad_base <= 4.0:
        precio_unitario = 460.0 / 16.0 # S/ 28.75
        semanas_max_toleradas = 6
    else:
        precio_unitario = 520.0 / 20.0 # S/ 26.00
        semanas_max_toleradas = 6

    # Regla de aplazamiento oficial (Si está dentro del tiempo base o el aplazamiento permitido, respeta el precio exacto del paquete)
    if semanas <= semanas_max_toleradas:
        if sesiones <= 4:
            return 180.0, "Tarifa Oficial Exacta (Respeta precio base de 4-5 semanas)"
        elif sesiones <= 8:
            return 300.0, "Tarifa Oficial Exacta (Respeta precio base de 4-5 semanas)"
        elif sesiones <= 12:
            return 380.0, "Tarifa Oficial Exacta (Respeta precio base de 4-6 semanas)"

    # Si excede las semanas de aplazamiento o es una cantidad totalmente proporcional fuera de los paquetes cerrados:
    precio_total = sesiones * precio_unitario
    
    if semanas > semanas_max_toleradas:
        # Aplicamos un recargo proporcional por extensión de vigencia
        precio_total = precio_total * 1.10
        return precio_total, f"Tarifa Proporcional con Recargo por Exceder el Aplazamiento de {semanas_max_toleradas} semanas"
    
    return precio_total, "Tarifa Proporcional Directa por Sesión"

if st.button("Calcular Tarifa"):
    total, detalle = calcular_tarifa_oficial_flexible(sesiones, semanas)
    
    st.success(f"### Precio Total: S/ {total:,.2f}")
    st.info(f"**Detalle:** {detalle}")