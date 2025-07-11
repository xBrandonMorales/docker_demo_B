"""
Chat con Datos - Aplicación Principal
Aplicación Streamlit para interactuar con datos usando IA
"""

import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import logging

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de la página
st.set_page_config(
    page_title="Chat con Datos",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_api_keys():
    """Verificar si las API keys están configuradas"""
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    return {
        "openai": openai_key and openai_key != "sk_p6Od0sbJQMXLGp56y0ojWGdyb3FYQPQDAAlHWvWsYAl9IpuIDjOP",
        "anthropic": anthropic_key and anthropic_key != "tu_api_key_de_anthropic_aqui"
    }

def main():
    """Función principal de la aplicación"""
    
    # Título principal
    st.title("🤖 Chat con Datos")
    st.subtitle("Aplicación desplegada con Docker")
    
    # Sidebar con información
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Verificar API keys
        api_status = check_api_keys()
        
        st.subheader("🔑 Estado de API Keys")
        if api_status["openai"]:
            st.success("✅ OpenAI API Key configurada")
        else:
            st.error("❌ OpenAI API Key no configurada")
            
        if api_status["anthropic"]:
            st.success("✅ Anthropic API Key configurada")
        else:
            st.error("❌ Anthropic API Key no configurada")
        
        st.divider()
        
        # Información del sistema
        st.subheader("ℹ️ Información del Sistema")
        st.info(f"""
        **Versión:** {os.getenv('APP_VERSION', '1.0.0')}
        **Puerto:** {os.getenv('STREAMLIT_SERVER_PORT', '8501')}
        **Modo Debug:** {os.getenv('DEBUG_MODE', 'false')}
        """)
    
    # Contenido principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat Interface")
        
        # Verificar si hay API keys configuradas
        if not any(api_status.values()):
            st.warning("""
            ⚠️ **No hay API keys configuradas**
            
            Para usar esta aplicación, necesitas configurar al menos una API key:
            1. Edita el archivo `.env` 
            2. Añade tu API key de OpenAI o Anthropic
            3. Reinicia el contenedor Docker
            """)
            return
        
        # Área de chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Mostrar mensajes anteriores
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input del usuario
        if prompt := st.chat_input("Escribe tu mensaje aquí..."):
            # Añadir mensaje del usuario
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Simular respuesta del asistente
            with st.chat_message("assistant"):
                response = f"""
                🤖 **Respuesta simulada**
                
                Recibí tu mensaje: "{prompt}"
                
                Esta es una respuesta de prueba. Para implementar la funcionalidad completa:
                1. Integra tu lógica de IA aquí
                2. Conecta con OpenAI o Anthropic APIs
                3. Procesa los datos según tu caso de uso
                
                **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.header("📊 Panel de Datos")
        
        # Ejemplo de datos
        st.subheader("📈 Métricas del Sistema")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Mensajes", len(st.session_state.get('messages', [])))
        with col_b:
            st.metric("Sesión", "Activa" if st.session_state.get('messages') else "Nueva")
        
        st.divider()
        
        # Área de carga de archivos
        st.subheader("📁 Cargar Datos")
        uploaded_file = st.file_uploader(
            "Sube un archivo",
            type=['pdf', 'txt', 'csv', 'docx'],
            help="Formatos soportados: PDF, TXT, CSV, DOCX"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ Archivo cargado: {uploaded_file.name}")
            st.info(f"📏 Tamaño: {uploaded_file.size} bytes")
            
            # Mostrar preview si es CSV
            if uploaded_file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(uploaded_file)
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"Error al leer CSV: {str(e)}")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🐳 Aplicación desplegada con Docker | 
        🚀 Funcionando en GitHub Codespaces | 
        ⚡ Powered by Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        logger.info("Iniciando aplicación Chat con Datos")
        main()
    except Exception as e:
        logger.error(f"Error en la aplicación: {str(e)}")
        st.error(f"Error en la aplicación: {str(e)}")
        st.error("Revisa los logs del contenedor para más detalles.")