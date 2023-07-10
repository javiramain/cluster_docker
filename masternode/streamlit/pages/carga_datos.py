import os.path
import pathlib
import streamlit as st
import subprocess
import sys

st.write("""
# Carga de Ficheros
""")
st.write("""
## Precargar fichero a File System
""")
uploaded_file = st.file_uploader("Choose a JSON file")
# if uploaded_file is not None:
    # bytes_data = uploaded_file.getvalue()
    # data = uploaded_file.getvalue().decode('utf-8').splitlines()
    # st.session_state["preview"] = ''
    #for i in range(0, min(5, len(data))):
        # st.session_state["preview"] += data[i]
# preview = st.text_area("CSV Preview", "", height=150, key="preview")
upload_state = st.text_area("Estado Fichero", "", key="upload_state")
def upload():
    if uploaded_file is None:
        st.session_state["upload_state"] = "Seleccione primero un fichero para subir"
    else:
        data = uploaded_file.getvalue().decode('utf-8')
        parent_path = pathlib.Path(__file__).parent.parent.resolve()
        save_path = os.path.join(parent_path, "data")
        complete_name = os.path.join(save_path, uploaded_file.name)
        destination_file = open(complete_name, "w")
        destination_file.write(data)
        destination_file.close()
        st.session_state["upload_state"] = "El fichero se ha cargado correctamente en " + complete_name
st.button("Subir fichero a  File System", on_click=upload)

st.write("""
## Subir fichero a HDFS
""")
def uploadToHDFS():
    subprocess.run(['bash', "/home/scripts/putFileToHDFS.sh"])
    st.write("Fichero subido. Revise HDFS.")
FsToHdfs = st.button("Subir a HDFS", on_click=uploadToHDFS)

st.write("""
## Cargar informacion en base de datos
""")

def loadInfoToMongo():
    subprocess.run(['bash', "/home/scripts/run-spark-batch.sh"])
    st.write("Fichero subido. Revise HDFS.")

loadToMongo = st.button("Cargar en base de datos", on_click=loadInfoToMongo)