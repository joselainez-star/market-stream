import streamlit as st

st.title("Conversor de Lempiras a Dólares")

st.sidebar.header("Configuración")
tasa_cambio = st.sidebar.number_input(
    "Tasa de cambio (Lempiras por Dólar)", 
    value=26.00, 
    min_value=0.01,
    step=0.01,
    help="Ingrese la tasa de cambio actual"
)

lempiras = st.number_input(
    "Ingrese la cantidad de Lempiras", 
    min_value=0.0,
    step=100.0,
    format="%.2f"
)

if st.button("Procesar", type="primary"):
    if tasa_cambio > 0:
        dolares = lempiras / tasa_cambio
        st.success(f"El equivalente en dólares es: **${dolares:,.2f}**")
        
        with st.expander("Ver detalles"):
            st.write(f"- Cantidad en Lempiras: L {lempiras:,.2f}")
            st.write(f"- Tasa de cambio: L {tasa_cambio:.2f} por $1")
            st.write(f"- Resultado: $ {dolares:,.2f}")
    else:
        st.error("La tasa de cambio debe ser mayor que 0")