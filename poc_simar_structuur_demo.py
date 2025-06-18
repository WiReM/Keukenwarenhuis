
import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="POC: Simar JSON Generator", layout="wide")
st.title("🔧 Demo – Genereer volledige SIMAR-structuur JSON")

st.markdown("""
Deze demo converteert een Excelbestand met artikelregels naar een JSON die de structuur volgt van een echte Simar-export.
Upload een Excel met kolommen zoals:
- `POSX`, `POSY`, `POSZ`, `ARTICLE`, `TEXT1`, `WIDTH`, `DEPTH`, `HEIGHT`
""")

uploaded_file = st.file_uploader("📤 Upload een Excelbestand", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Ingelezen gegevens:")
        st.dataframe(df)

        kitchen_json = {
            "KITCHEN": {
                "NAME": "NOBILIA",
                "PLANINFO": {
                    "ROOMLENGTH": 4000,
                    "ROOMWIDTH": 3700,
                    "ROOMHEIGHT": 2500
                },
                "CABINET": []
            }
        }

        for i, row in df.iterrows():
            kitchen_json["KITCHEN"]["CABINET"].append({
                "POSX": int(row.get("POSX", 0)),
                "POSY": int(row.get("POSY", 0)),
                "POSZ": int(row.get("POSZ", 0)),
                "CATALOG": row.get("CATALOG", "NOBILIA"),
                "ARTICLE": str(row.get("ARTICLE", f"ART{i+1}")),
                "TEXT1": row.get("TEXT1", "Kast"),
                "WIDTH": int(row.get("WIDTH", 600)),
                "HEIGHT": int(row.get("HEIGHT", 720)),
                "DEPTH": int(row.get("DEPTH", 561))
            })

        st.markdown("### 📄 Gegenereerde SIMAR JSON:")
        st.json(kitchen_json)

        st.download_button(
            "📥 Download JSON",
            data=json.dumps(kitchen_json, indent=2),
            file_name="simar_poc_output.json",
            mime="application/json"
        )

    except Exception as e:
        st.error(f"Fout bij verwerken bestand: {e}")
else:
    st.info("Upload een Excel met kasten- of objectinformatie.")
