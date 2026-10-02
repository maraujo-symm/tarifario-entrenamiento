import streamlit as st

st.title("Calculadora de Tarifas Flexibles - Centro de Entrenamiento")
st.write("Cotizador basado en la densidad de entrenamiento (sesiones / semanas) y tarifas oficiales.")

sesiones = st.number_input("Cantidad de sesiones", min_value=1, max_value=50, value=8, step=1)
semanas = st.number_input("Límite de semanas de vigencia", min_value=1, max_value=52, value=2, step=1)

def calcular_tarifa_por_densidad(sesiones, semanas):
    # 1. Calcular la densidad real de consumo (sesiones por semana)
    densidad = sesiones / semanas
    
    # 2. Definir el precio por sesión proporcional según la densidad
    if densidad <= 1.0:
        precio_por_sesion = 45.00
    elif densidad <= 2.0:
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

    # 3. Excepción de control solo cuando el tiempo de vigencia es el estándar (4 a 5/6 semanas)
    # Si se hace en menos tiempo (ej. 2 semanas), pasa directamente al cálculo por densidad (express).
    if sesiones == 4 and 4 <= semanas <= 5:
        return 180.0, 45.00, densidad, "Tarifa Oficial Exacta (4 sesiones en su tiempo base)"
    elif sesiones == 8 and 4 <= semanas <= 5:
        return 300.0, 37.50, densidad, "Tarifa Oficial Exacta (8 sesiones en su tiempo base)"
    elif sesiones == 12 and 4 <= semanas <= 6:
        return 380.0, 31.67, densidad, "Tarifa Oficial Exacta (12 sesiones en su tiempo base)"

    # 4. Cálculo final proporcional por densidad para formatos rápidos o cantidades libres
    precio_total = sesiones * precio_por_sesion
    return precio_total, precio_por_sesion, densidad, "Tarifa Proporcional por Densidad (Formato Express / Acelerado)"

if st.button("Calcular Tarifa"):
    total, unitario, dens, detalle = calcular_tarifa_por_densidad(sesiones, semanas)
    
    st.success(f"### Precio Total: S/ {total:,.2f}")
    st.info(f"**Detalle del cálculo:**\n- **Tipo:** {detalle}\n- **Densidad:** {dens:.2f} sesiones/semana\n- **Precio unitario aplicado:** S/ {unitario:.2f} por sesión")