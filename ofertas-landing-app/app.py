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

st.title("🏦 ¡Hola! Consulta tus ofertas disponibles")
st.markdown("Ingresa tu número de **DUI** para descubrir las ofertas exclusivas que tenemos preparadas para ti hoy. 🚀")

df = load_data()

if df is not None:
    # 🔥 MODO DEBUG: Si no existe la columna, mostramos un error claro en pantalla
    if "DUI_CORREGIDO" not in df.columns:
        st.error(f"🚨 Error de formato: No se encontró la columna 'DUI_CORREGIDO' en tu archivo.")
        st.warning(f"**Las columnas que tu archivo realmente tiene son:** {', '.join(df.columns.tolist())}")
        st.info("💡 Solución: Cambia el nombre de la columna en tu Excel/CSV a 'DUI_CORREGIDO' o actualiza el código para usar el nombre correcto.")
    else:
        # Formulario de búsqueda (solo se muestra si la columna existe)
        with st.container():
            dui_input = st.text_input("Introduce tu DUI:", placeholder="00000000-0")
            btn_consultar = st.button("🔍 Ver mis ofertas")

        if btn_consultar:
            if dui_input:
                dui = clean_dui(dui_input)
                result = df[df["DUI_CORREGIDO"] == dui]

                if not result.empty:
                    row = result.iloc[0]
                    
                    st.balloons()
                    # Manejo seguro por si tampoco existe "NOMBRE DEL EMPLEADO"
                    nombre = row.get('NOMBRE DEL EMPLEADO', 'Cliente')
                    st.success(f"### 🎉 ¡Felicidades, {nombre}!")
                    st.write("Estas son tus opciones de crédito disponibles:")

                    ofertas = [
                        ("💳", "Límite Tarjeta de Crédito", row.get("Limite TC")),
                        ("💳", "Tipo de Tarjeta de Crédito", row.get("Tipo TC")),
                        ("📱", "Consumo Móvil", row.get("Consumo Movil")),
                        ("💸", "Adelanto de Salario", row.get("Adelanto de Salario")),
                        ("🏦", "Orden de Descuento", row.get("Consumo con Orden de Descuento")),
                        ("🔥", "Combo Oferta Especial", row.get("Combo_Oferta"))
                    ]

                    for icono, nombre, valor in ofertas:
                        if pd.notna(valor) and str(valor).strip() not in ["0", "0.0", "nan", ""]:
                            st.markdown(f"""
                                <div class="offer-card">
                                    <strong>{icono} {nombre}:</strong><br>
                                    <span style='font-size: 1.2em; color: #1f77b4;'>$ {valor}</span>
                                </div>
                            """, unsafe_allow_html=True)

                    st.divider()
                    total = row.get('Total Ofertado', 'No disponible')
                    st.metric(label="💰 TOTAL DISPONIBLE PARA TI", value=f"$ {total}")
                    
                    st.info("ℹ️ Para activar cualquiera de estas ofertas, acércate a tu agencia más cercana o llámanos. 📞")
                else:
                    st.error("😕 Lo sentimos, no encontramos ofertas asociadas a ese DUI. Por favor, verifica el número.")
            else:
                st.warning("⚠️ Por favor, ingresa un número de DUI primero.")
else:
    st.error("⚠️ Hubo un problema al cargar la base de datos. Contacta a soporte.")

st.markdown("<br><br><center><small>Powered by Streamlit & Data Team 📊</small></center>", unsafe_allow_html=True)
