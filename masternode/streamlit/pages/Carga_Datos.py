import os.path
import pathlib
import streamlit as st
import subprocess

st.header('Estás en la seccion de Carga de Ficheros')
parent_path = pathlib.Path(__file__).parent.parent.resolve()
save_path = os.path.join(parent_path, "data")

uploaded_files = st.file_uploader(label="Choose a JSON file", type='json',
                                  accept_multiple_files=True, help='Navega y selecciona los ficheros que quieras subir',
                                  )
upload_state = st.text_area(label="Estado de la carga:", placeholder="Aqui se mostrara el estado de la carga",
                            key="upload_state")


def get_dir_files(path: str):
    return os.listdir(path)


def get_fs_state():
    st.session_state["staging_fs_state"] = "Ficheros en el File System:\n" + ', '.join(get_dir_files(save_path))


staging_fs_state = st.text_area("Estado del File System:", value= get_fs_state(), key="staging_fs_state")

"---"


def clean_fs():
    st.spinner(text="Limpiando File System")
    subprocess.run(['bash', "/home/scripts/cleanFileSystem.sh"])
    get_fs_state()


def upload():
    if not uploaded_files:
        st.session_state["upload_state"] = "Seleccione primero un fichero para subir"
    else:
        if limpiarFileSystem:
            clean_fs()
        files_to_upload = []
        for file in uploaded_files:
            files_to_upload.append(file)
        for file in files_to_upload:
            complete_name = os.path.join(save_path, file.name)
            destination_file = open(complete_name, "w")
            destination_file.write(file.getvalue().decode('utf-8'))

            destination_file.close()
        st.session_state["upload_state"] = "El fichero se ha cargado correctamente en el File System"
        get_fs_state()


limpiarFileSystem = st.checkbox('Limpiar el File System antes de subir nuevos ficheros')

st.button("Subir fichero a  File System", on_click=upload)

"---"

limpiarHDFS = st.checkbox('Limpiar HDFS antes de subir ficheros')


def clean_hdfs():
    subprocess.run(['bash', "/home/scripts/cleanHDFS.sh"])


def upload_to_hdfs():
    if not get_dir_files(save_path):
        st.session_state["upload_state"] = "La ruta del File System está vacía. Seleccione y suba antes un fichero."
        get_fs_state()
    else:
        with st.spinner('Subiendo Ficheros a HDFS...'):
            if limpiarHDFS:
                clean_hdfs()
                subprocess.run(['bash', "/home/scripts/putFileToHDFS.sh"])
                st.session_state["upload_state"] = "La ruta de HDFS se limpió y los ficheros se cargaron correctamente."

            else:
                subprocess.run(['bash', "/home/scripts/putFileToHDFS.sh"])
                st.session_state[
                    "upload_state"] = "Los ficheros se han cargado en HDFS. Los ficheros previos no se borraron. "
        st.success('Carga en Hdfs completa!')
    get_fs_state()
    st.balloons()


FsToHdfs = st.button("Subir a HDFS", on_click=upload_to_hdfs)


def load_info_to_mongo():
    with st.spinner('Cargando la información en base de datos...'):
        subprocess.run(['bash', "/home/scripts/run-spark-batch.sh"])
    st.success('Carga en base de datos completa!')
    st.session_state["upload_state"] = "La información se ha cargado en base de datos y ya puede ser consultada."
    st.balloons()


"---"

loadToMongo = st.button("Cargar en base de datos", on_click=load_info_to_mongo)
