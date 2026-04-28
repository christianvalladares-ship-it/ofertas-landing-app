import pandas as pd
import streamlit as st
import os
import re

def clean_dui(x):
    # 1. Convertimos a texto
    val = str(x).strip()
    
    # 2. Si pandas lo convirtió en decimal (ej. "6338053.0"), le quitamos el ".0"
    if val.endswith(".0"):
        val = val[:-2]
        
    # 3. Limpieza profunda con REGEX: Extraemos SOLO los números \d
    # Esto elimina guiones, espacios, comas o letras accidentales.
    numeros = re.sub(r'\D', '', val)
    
    # Si después de limpiar no quedó nada (ej. era "nan" o celdas vacías)
    if not numeros:
        return ""
        
    # 4. Rellenamos con ceros a la izquierda hasta llegar a los 9 dígitos exactos
    numeros = numeros.zfill(9)
    
    # 5. Formateamos al estándar oficial de El Salvador: ^\d{8}-\d$
    dui_oficial = f"{numeros[:8]}-{numeros[8]}"
    
    # Opcional: Validamos internamente que cumpla el regex antes de devolverlo
    if re.match(r'^\d{8}-\d$', dui_oficial):
        return dui_oficial
    else:
        return "" # O devuelve un valor por defecto si falla algo rarísimo

@st.cache_data
def load_data():
    # Buscamos la ruta base del proyecto de forma dinámica
    # Subimos un nivel desde utils/ para llegar a la raíz
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    csv_path = os.path.join(base_path, "data", "Ofertas_San_Vicente_SUR.csv")
    xlsx_path = os.path.join(base_path, "data", "Ofertas_San_Vicente_SUR.xlsx")

    df = None
    
    # 1. Intentar leer CSV con diferentes encodings
    if os.path.exists(csv_path):
        for encoding in ["utf-8", "latin1", "iso-8859-1", "cp1252"]:
            try:
                df = pd.read_csv(csv_path, sep=";", encoding=encoding)
                print(f"✅ CSV cargado con éxito ({encoding})")
                break
            except Exception:
                continue

    # 2. Si no funcionó el CSV, intentar con Excel
    if df is None and os.path.exists(xlsx_path):
        try:
            df = pd.read_excel(xlsx_path)
            print("✅ Excel cargado con éxito")
        except Exception as e:
            st.error(f"❌ Error crítico: No se pudo leer ni CSV ni Excel. {e}")
            return None

    if df is not None:
        # Limpieza estándar
        df.columns = df.columns.str.strip()
        
        # Verificamos que existan las columnas necesarias para no romper la app
        if "DUI_CORREGIDO" in df.columns:
            df["DUI_CORREGIDO"] = df["DUI_CORREGIDO"].apply(clean_dui)
        
        if "NOMBRE DEL EMPLEADO" in df.columns:
            df["NOMBRE DEL EMPLEADO"] = df["NOMBRE DEL EMPLEADO"].astype(str).str.strip()
            
        return df
    
    return None