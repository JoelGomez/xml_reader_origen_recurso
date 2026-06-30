import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd


def main():
    uploaded_file = st.file_uploader("Agrega los xml para analizar", accept_multiple_files=True)

    namespaces = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'nomina12': 'http://www.sat.gob.mx/nomina12',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }

    if uploaded_file:
        registros = []
        
        if len(uploaded_file) == 1:
            st.write("Se agregó 1 archivo")
        else:
            st.write(f"Se agregaron {len(uploaded_file)} archivos")

        for file in uploaded_file:
            
            tree = ET.parse(file)
            root = tree.getroot()

            entidad = root.find('.//nomina12:EntidadSNCF', namespaces)

            if entidad is not None:
                origen_recurso = entidad.get('OrigenRecurso')
                monto_recurso = entidad.get('MontoRecursoPropio')
                
                registros.append({
                    "Archivo": file.name,
                    "Origen recurso": origen_recurso,
                    "Monto recurso propio": monto_recurso
                })

        df = pd.DataFrame(registros)
        st.dataframe(df, use_container_width=True)



if __name__ == "__main__":
    main()
