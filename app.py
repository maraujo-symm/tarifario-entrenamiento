import streamlit as st

st.title("Calculadora de Tarifas Flexibles - Centro de Entrenamiento")
st.write("Calcula el precio respetando el límite oficial de aplazamiento (hasta 5 semanas para 8 sesiones).")

sesiones = st.number_input("Cantidad de sesiones", min_value=1, max_value=50, value=8, step=1)
semanas = st.number_input("Límite de semanas de vigencia", min_value=1, max_value=52, value=4, step=1)

def calcular_tarifa_con_limite_exacto(sesiones, semanas):
    # Definir los parámetros base según la tabla oficial
    if sesiones <= 4:
        precio_base_oficial = 180.0
        semanas_max_toleradas = 5  # Hasta 5 semanas para 1 paquete de 4 sesiones
    elif sesiones <= 8:
        precio_base_oficial = 300.0
        semanas_max_toleradas = 5  # Hasta 5 semanas para el paquete de 8 sesiones (2v/sem)
    elif sesiones <= 12:
        precio_base_oficial = 380.0
        semanas_max_toleradas = 6  # Hasta 6 semanas para el paquete de 12 sesiones (3v/sem)
    else:
        precio_base_oficial = (520 / 20) * sesiones
        semanas_max_toleradas = int(4 * (sesiones / 4) * 1.25)

    # Regla: Si está dentro de las semanas máximas toleradas con aplazamiento, mantiene el precio oficial
    if semanas <= semanas_max_toleradas:
        return precio_base_oficial, f"Tarifa Oficial (Incluye aplazamiento permitido de hasta {semanas_max_toleradas} semanas)"
    
    else:
        # Si supera el límite de semanas permitidas (ej. 8 sesiones en 6 semanas), aplica recargo proporcional
        densidad = sesiones / semanas
        if densidad <= 1.0:
            precio_por_sesion = 45.00
        else:
            precio_por_sesion = 37.50 * 1.15  # Se aplica un recargo por extender el tiempo más allá del aplazamiento
            
        precio_total = sesiones * precio_por_sesion
        return precio_total, "Tarifa con Recargo por Exceso de Vigencia (Supera el aplazamiento de 5 semanas)"

if st.button("Calcular Tarifa"):
    total, detalle = calcular_tarifa_con_limite_exacto(sesiones, semanas)
    
    st.success(f"### Precio Total: S/ {total:,.2f}")
    st.info(f"**Detalle:** {detalle}")