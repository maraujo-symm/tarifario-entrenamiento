import streamlit as st

st.title("Calculadora de Tarifas Flexibles - Centro de Entrenamiento")
st.write("Cotizador basado en la densidad de entrenamiento (sesiones / semanas) y tarifas oficiales.")

sesiones = st.number_input("Cantidad de sesiones", min_value=1, max_value=50, value=8, step=1)
semanas = st.number_input("Límite de semanas de vigencia", min_value=1, max_value=52, value=4, step=1)

def calcular_tarifa_por_densidad(sesiones, semanas):
    # 1. Calcular la densidad real de consumo (sesiones por semana)
    densidad = sesiones / semanas
    
    # 2. Definir el precio por sesión proporcional según la densidad
    # Tomamos como referencias los extremos de tu tarifario oficial:
    # - Densidad de 1 vez/sem (o menor): S/ 45.00 por sesión (180 / 4)[cite: 1]
    # - Densidad de 2 veces/sem: S/ 37.50 por sesión (300 / 8)[cite: 1]
    # - Densidad de 3 veces/sem: S/ 31.67 por sesión (380 / 12)[cite: 1]
    # - Densidad de 4 veces/sem: S/ 28.75 por sesión (460 / 16)[cite: 1]
    # - Densidad de 5 veces/sem (o mayor): S/ 26.00 por sesión (520 / 20)[cite: 1]
    
    if densidad <= 1.0:
        precio_por_sesion = 45.00
    elif densidad <= 2.0:
        # Interpolación lineal proporcional entre densidad 1.0 y 2.0
        proporcion = (densidad - 1.0) / (2.0 - 1.0)
        precio_por_sesion = 45.00 - proporcion * (45.00 - 37.50)
    elif densidad <= 3.0:
        proporcion = (densidad - 2.0) / (3.0 - 2.0)
        precio_por_sesion = 37.50 - proporcion * (37.50 - 31.67)
    elif densidad <= 4.0:
        proporcion = (densidad - 3.0) / (4.0 - 3.0)
        precio_por_sesion = 31.67 - proporcion * (31.67 - 28.75)
    else:
        proporcion = min(1.0, (densidad - 4.0) / (5.0 - 4.0))
        precio_por_sesion = 28.75 - proporcion * (28.75 - 26.00)

    # 3. Excepción de control para respetar los paquetes oficiales exactos (ej. 4 sesiones en 4-5 semanas = S/ 180, 8 sesiones en 4-5 sem = S/ 300)[cite: 1]
    if sesiones == 4 and semanas <= 5:
        return 180.0, 45.00, densidad, "Tarifa Oficial Exacta (4 sesiones)"[cite: 1]
    elif sesiones == 8 and semanas <= 5:
        return 300.0, 37.50, densidad, "Tarifa Oficial Exacta (8 sesiones)"[cite: 1]
    elif sesiones == 12 and semanas <= 6:
        return 380.0, 31.67, densidad, "Tarifa Oficial Exacta (12 sesiones)"[cite: 1]

    # 4. Cálculo final proporcional puro para cualquier otro caso
    precio_total = sesiones * precio_por_sesion
    return precio_total, precio_por_sesion, densidad, "Tarifa Proporcional por Densidad"

if st.button("Calcular Tarifa"):
    total, unitario, dens, detalle = calcular_tarifa_por_densidad(sesiones, semanas)
    
    st.success(f"### Precio Total: S/ {total:,.2f}")
    st.info(f"**Detalle del cálculo:**\n- **Tipo:** {detalle}\n- **Densidad:** {dens:.2f} sesiones/semana\n- **Precio unitario aplicado:** S/ {unitario:.2f} por sesión")