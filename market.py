import streamlit as st
import pandas as pd

def calcular_subtotal(nombre_producto, precio_producto, cantidad_producto):
    """Calcula el subtotal y agrega el producto a la tabla"""
    subtotal = float(precio_producto) * float(cantidad_producto)
    nueva_fila = {
        "Producto": nombre_producto,
        "Precio": precio_producto,
        "Cantidad": cantidad_producto,
        "Subtotal": subtotal
    }
    
    if 'temp_data' not in st.session_state:
        st.session_state.temp_data = []
    
    st.session_state.temp_data.append(nueva_fila)
    
    st.session_state.table_data = pd.DataFrame(st.session_state.temp_data)

def calcular_total():
    """Calcula el total con impuesto del 15% fijo"""
    if not st.session_state.table_data.empty:
        subtotal = st.session_state.table_data["Subtotal"].sum()
        impuesto = subtotal * 0.15  # 15% fijo
        total = subtotal + impuesto
        return subtotal, impuesto, total
    return 0, 0, 0

def limpiar_datos():
    """Limpia todos los datos de la sesión"""
    st.session_state.table_data = pd.DataFrame(
        columns=["Producto", "Precio", "Cantidad", "Subtotal"]
    )
    if 'temp_data' in st.session_state:
        st.session_state.temp_data = []

# Inicializar el estado de la sesión
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame(
        columns=["Producto", "Precio", "Cantidad", "Subtotal"]
    )

st.title("SuperMarket Amador")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Agregar Productos")
    with st.form("producto_form", clear_on_submit=True):
        producto_nombre = st.text_input("Nombre del producto")
        producto_precio = st.number_input("Precio unitario ($)", min_value=0.0, step=0.1, format="%.2f")
        producto_cantidad = st.number_input("Cantidad", min_value=1, step=1)
        
        agregar_button = st.form_submit_button("Agregar Producto")
        
        if agregar_button and producto_nombre:
            calcular_subtotal(producto_nombre, producto_precio, producto_cantidad)
            st.success(f"{producto_nombre} agregado correctamente")

with col2:
    st.header("Impuesto")
    st.info("Impuesto fijo: 15%")

st.header("Productos en el Carrito")
if not st.session_state.table_data.empty:
    styled_data = st.session_state.table_data.copy()
    styled_data["Precio"] = styled_data["Precio"].apply(lambda x: f"${x:.2f}")
    styled_data["Subtotal"] = styled_data["Subtotal"].apply(lambda x: f"${x:.2f}")
    st.dataframe(styled_data, use_container_width=True)
else:
    st.info("No hay productos en el carrito...")

col3, col4, col5 = st.columns(3)

with col3:
    if st.button("Calcular Total", type="primary", use_container_width=True):
        if not st.session_state.table_data.empty:
            subtotal, impuesto, total = calcular_total()
            
            st.subheader("Resumen de Compra")
            
            # Usar columnas con proporciones más amplias
            col_result1, col_result2 = st.columns([1, 1])
            
            with col_result1:
                st.metric("Subtotal", f"${subtotal:,.2f}")
                st.metric("Impuesto (15%)", f"${impuesto:,.2f}")
            
            with col_result2:
                st.metric("Total a Pagar", f"${total:,.2f}")
            
            # Solo el desglose detallado (sin la tabla adicional)
            with st.expander("Ver desglose detallado"):
                st.write(f"**Subtotal:** ${subtotal:,.2f}")
                st.write(f"**Impuesto (15%):** ${impuesto:,.2f}")
                st.write(f"**Total con impuesto incluido:** ${total:,.2f}")
                
        else:
            st.warning("No hay productos para calcular el total.")

with col4:
    if st.button("Limpiar Todo", type="secondary", use_container_width=True):
        limpiar_datos()
        st.success("Carrito limpiado correctamente")
        st.rerun()

with col5:
    if st.button("Nueva Compra", use_container_width=True):
        limpiar_datos()
        st.success("Listo para nueva compra!")
        st.rerun()

# Agregar CSS personalizado para aumentar el ancho de los números
st.markdown("""
<style>
    /* Aumentar el tamaño de fuente de los números en las métricas */
    div[data-testid="stMetricValue"] {
        font-size: 24px !important;
    }
    
    /* Asegurar que el texto no se trunque */
    .stMetric {
        min-width: 200px;
    }
</style>
""", unsafe_allow_html=True)