import pandas as pd
import streamlit as st
import os
import re

def clean_dui(x):
    val = str(x).strip()
    if val.endswith(".0"):
        val = val[:-2]
        
    numeros = re.sub(r'\D', '', val)
    
    if not numeros:
        return ""
        
    numeros = numeros.zfill(9)
    dui_oficial = f"{numeros[:8]}-{numeros[8]}"
    
    if re.match(r'^\d{8}-\d$', dui_oficial):
        return dui_oficial
    else:
        return ""

@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    csv_path = os.path.join(base_path, "data", "Ofertas_San_Vicente_SUR.csv")
    xlsx_path = os.path.join(base_path, "data", "Ofertas_San_Vicente_SUR.xlsx")

    df = None
    
    # 🔥 AQUÍ AGREGAMOS dtype=str de nuevo
    if os.path.exists(csv_path):
        for encoding in ["utf-8", "latin1", "iso-8859-1", "cp1252"]:
            try:
                df = pd.read_csv(csv_path, sep=",", encoding=encoding, dtype=str)
                print(f"✅ CSV cargado con éxito ({encoding})")
                break
            except Exception:
                continue

    # 🔥 AQUÍ TAMBIÉN AGREGAMOS dtype=str
    if df is None and os.path.exists(xlsx_path):
        try:
            df = pd.read_excel(xlsx_path, dtype=str)
            print("✅ Excel cargado con éxito")
        except Exception as e:
            st.error(f"❌ Error crítico: No se pudo leer ni CSV ni Excel. {e}")
            return None

    if df is not None:
        # Forzamos los nombres de las columnas a mayúsculas y quitamos espacios para evitar errores tontos
        df.columns = df.columns.str.strip().str.upper()
        
        if "DUI_CORREGIDO" in df.columns:
            df["DUI_CORREGIDO"] = df["DUI_CORREGIDO"].apply(clean_dui)
        
        if "NOMBRE DEL EMPLEADO" in df.columns:
            df["NOMBRE DEL EMPLEADO"] = df["NOMBRE DEL EMPLEADO"].astype(str).str.strip()
            
        return df
    
    return None
