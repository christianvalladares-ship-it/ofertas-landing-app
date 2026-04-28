import streamlit as st
import pandas as pd
from utils.loader import load_data, clean_dui

# Configuración de página con icono
st.set_page_config(page_title="Mis Ofertas Disponibles", page_icon="💰", layout="centered")

# Estilo personalizado básico
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    .offer-card { padding: 15px; border-radius: 10px; background-color: white; border-left: 5px solid #FF4B4B; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 ¡Hola! Consulta tus beneficios")
st.markdown("Ingresa tu número de **DUI** para descubrir las ofertas exclusivas que tenemos preparadas para ti hoy. 🚀")

df = load_data()

if df is not None:
    # Formulario de búsqueda
    with st.container():
        dui_input = st.text_input("Introduce tu DUI:", placeholder="00000000-0")
        btn_consultar = st.button("🔍 Ver mis ofertas")

    if btn_consultar:
        if dui_input:
            dui = clean_dui(dui_input)
            result = df[df["DUI_CORREGIDO"] == dui]

            if not result.empty:
                row = result.iloc[0]
                
                st.balloons() # ✨ Efecto visual de celebración
                st.success(f"### 🎉 ¡Felicidades, {row.get('NOMBRE DEL EMPLEADO', 'Cliente')}!")
                st.write("Estas son tus opciones de crédito disponibles:")

                # Definimos los iconos, etiquetas, el nombre EXACTO de la columna y si lleva "$" (True/False)
                ofertas = ofertas = [
                    ("💳", "Límite Tarjeta de Crédito", row.get("LIMITE TC"), True),
                    ("💳", "Tipo de Tarjeta de Crédito", row.get("TIPO TC"), False),
                    ("📱", "Consumo Móvil", row.get("CONSUMO MOVIL"), True),
                    ("💸", "Adelanto de Salario", row.get("ADELANTO DE SALARIO"), True),
                    ("🏦", "Orden de Descuento", row.get("CONSUMO CON ORDEN DE DESCUENTO"), True),
                    ("🔥", "Combo Oferta Especial", row.get("COMBO_OFERTA"), True)
                ]

                # Mostramos las ofertas filtrando ceros y nulos en varios formatos
                ofertas_mostradas = 0
                for icono, nombre, valor, es_moneda in ofertas:
                    val_str = str(valor).strip().lower()
                    
                    if pd.notna(valor) and val_str not in ["0", "0.0", "0.00", "nan", "none", "null", ""]:
                        prefix = "$ " if es_moneda else ""
                        st.markdown(f"""
                            <div class="offer-card">
                                <strong>{icono} {nombre}:</strong><br>
                                <span style='font-size: 1.2em; color: #1f77b4;'>{prefix}{valor}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        ofertas_mostradas += 1

                if ofertas_mostradas == 0:
                    st.info("Actualmente no tienes ofertas de crédito pre-aprobadas, pero acércate a la agencia para evaluar tu caso.")

                st.divider()
                
                # Total destacado
                total = row.get("Total Ofertado")
                if pd.notna(total) and str(total).strip().lower() not in ["nan", "none", "0", "0.0", ""]:
                    st.metric(label="💰 TOTAL DISPONIBLE PARA TI", value=f"$ {total}")
                
                st.info("ℹ️ Para activar cualquiera de estas ofertas, acércate a tu agencia más cercana o llámanos. 📞")

            else:
                st.error("😕 Lo sentimos, no encontramos ofertas asociadas a ese DUI. Por favor, verifica el número.")
        else:
            st.warning("⚠️ Por favor, ingresa un número de DUI primero.")
else:
    st.error("⚠️ Hubo un problema al cargar la base de datos. Contacta a soporte.")

# Footer
st.markdown("<br><br><center><small>Powered by Streamlit & Data Team 📊</small></center>", unsafe_allow_html=True)
