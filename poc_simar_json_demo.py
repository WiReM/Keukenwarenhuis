
import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="POC: Orderformulier naar SIMAR JSON", layout="wide")
st.title("🧾 POC Demo – Van handmatig formulier naar SIMAR JSON")

st.markdown("""
Deze demo simuleert het proces van:
1. Orderregelherkenning uit een formulier
2. Automatische mapping via IDM
3. Output naar SIMAR-compatibele JSON
""")

# Upload sectie
uploaded_file = st.file_uploader("📤 Upload een gesimuleerd Excel-orderformulier", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Formulier succesvol geladen:")
        st.dataframe(df)

        # Voor demo: voeg mock-data toe en bouw JSON
        json_result = {
            "order": {
                "customerNo": "POC1234",
                "project": "Demo OCR naar JSON",
                "status": "open"
            },
            "longParts": []
        }

        for i, row in df.iterrows():
            part = {
                "id": i + 1,
                "articleNo": row.get("Artikelcode", f"CODE{i}"),
                "description": row.get("Omschrijving", "Omschrijving onbekend"),
                "price": row.get("Prijs (€)", 0),
                "amount": row.get("Aantal", 1),
                "width": int(row.get("Breedte (mm)", 600)),
                "depth": int(row.get("Diepte (mm)", 561)),
                "height": int(row.get("Hoogte (mm)", 720)),
                "functionNumber": int(row.get("FunctieNr", 99)),
                "functionTypeName": row.get("Omschrijving", "Type onbekend"),
                "longPartEnum": row.get("Categorie", "CABINET")
            }
            json_result["longParts"].append(part)

        st.markdown("### 🧾 Gegenereerde JSON")
        st.json(json_result, expanded=False)

        json_str = json.dumps(json_result, indent=2)
        st.download_button("📥 Download JSON", data=json_str, file_name="poc_simar_output.json", mime="application/json")

    except Exception as e:
        st.error(f"Fout bij verwerken van bestand: {e}")
else:
    st.info("Upload eerst een Excel-bestand met artikelregels.")
