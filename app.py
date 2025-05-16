import requests
import streamlit as st
import time


st.title("Chatbot Legal POC - DataOffice")
st.subheader("Haz tu consulta legal")

# Inicializar estado
if "pregunta" not in st.session_state:
    st.session_state.pregunta = ""
if "respuesta_final" not in st.session_state:
    st.session_state.respuesta_final = None
if "documentos" not in st.session_state:
    st.session_state.documentos = []
if "enviada" not in st.session_state:
    st.session_state.enviada = False

# Botón para limpiar todo
if st.button("Nueva pregunta"):
    st.session_state.pregunta = ""
    st.session_state.respuesta_final = None
    st.session_state.documentos = []
    st.session_state.enviada = False

# Campo de texto
st.session_state.pregunta = st.text_area("Escribe tu pregunta aquí", value=st.session_state.pregunta, height=150)

# Función para procesar la pregunta
def enviar_pregunta():
    st.session_state.enviada = True
    try:
        with st.spinner("El asistente está redactando la respuesta..."):
            url = "https://backend-chatbot-legalpoc-624205664083.us-central1.run.app" #https://backend-chatbot-legalpoc-624205664083.us-central1.run.app
            payload = {"pregunta": st.session_state.pregunta}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

        if data.get("success"):
            st.session_state.respuesta_final = data["data"]["respuesta_final"]
            st.session_state.documentos = data["data"]["documentos_finales"]
            st.success("Respuesta generada correctamente.")
        else:
            st.error(f"Error en la respuesta: {data.get('message', 'Desconocido')}")
            st.session_state.enviada = False
    except Exception as e:
        st.error(f"Error al procesar la solicitud: {e}")
        st.session_state.enviada = False

# Mostrar botón solo si no ha sido enviada
if not st.session_state.enviada and st.session_state.pregunta.strip():
    st.button("Enviar pregunta", key="btn_enviar", on_click=enviar_pregunta)

# Mostrar resultados si existen
if st.session_state.respuesta_final:
    st.markdown("## Respuesta Final")
    st.markdown(st.session_state.respuesta_final)

    st.markdown("## Documentos Referenciados")
    for idx, doc in enumerate(st.session_state.documentos, 1):
        with st.expander(f"{idx}. Documento: {doc['file_id']}"):
            st.markdown("**Resumen del Documento:**")
            st.markdown(doc["respuesta"])

            st.markdown("**Leyes:**")
            leyes = doc.get("leyes")
            if leyes:
                for kw in leyes:
                    st.markdown(f"- {kw}")

            st.markdown("**Keywords:**")
            keywords = doc.get("keywords")
            if keywords:
                for kw in keywords:
                    st.markdown(f"- {kw}")



