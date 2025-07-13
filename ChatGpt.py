#zzz
from openai import OpenAI    #debe instalarse       pip install openai

#carga variables de entorno   pip install python-dotenv   
import os
from dotenv import load_dotenv
load_dotenv() # Carga las variables del archivo .env
token_chatgpt = os.getenv("OPENAI_API_KEY")# Ahora puedes acceder a ellas como si fueran variables de entorno normales
  # Verifica que la clave se haya cargado correctamente


def consultar_chatgpt_mini(query, rag_context=None):
    """
    Función para consultar un modelo de lenguaje como ChatGPT Mini (o similar de OpenAI).
    Requiere una API Key de OpenAI.
    """
    print(f"\n--- Consultando ChatGPT Mini para: '{query}' ---")

    # Asegúrate de que la clave de API esté configurada como variable de entorno
    # o pásala directamente (menos recomendado para producción)
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # O para una demostración, puedes ponerla directamente (NO RECOMENDADO EN CÓDIGO FINAL)
    # client = OpenAI(api_key="TU_API_KEY_DE_OPENAI") # ¡Reemplaza con tu clave real!

    # Por seguridad y buenas prácticas, es mejor usar variables de entorno:

    try:
        client = OpenAI(api_key=token_chatgpt)
    except KeyError:
        print("Error: La variable de entorno 'OPENAI_API_KEY' no está configurada.")
        print("Por favor, configura tu clave de API de OpenAI.")
        return "Error de configuración de API."

    messages = []
    if rag_context:
        messages.append({"role": "system", "content": f"Basado en la siguiente información: {rag_context}. Responde a la pregunta del usuario."})
    messages.append({"role": "user", "content": query})

    try:
        # Elige el modelo que consideres "mini" o adecuado para tu caso.
        # "gpt-3.5-turbo" es una opción común y más económica.
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", # Puedes probar otros modelos si tienes acceso
            messages=messages,
            max_tokens=300, # Limita la longitud de la respuesta
            temperature=0.7 # Controla la creatividad de la respuesta (0.0 a 1.0)
        )
        response = completion.choices[0].message.content
        print("Respuesta de ChatGPT Mini:\n", response)
        return response
    except Exception as e:
        print(f"Error al consultar ChatGPT Mini: {e}")
        return f"Error al consultar ChatGPT Mini: {e}"


def ConsultandoChatGPT(pregunta_GPT):

  respuesta_chatgpt_sin_contexto = consultar_chatgpt_mini(pregunta_GPT, rag_context=None)
  
  print("\n--- Ejemplo de consulta solo a ChatGPT Mini sin contexto RAG ---")
  print(f"Respuesta de ChatGPT Mini sin contexto: {respuesta_chatgpt_sin_contexto}")

  return respuesta_chatgpt_sin_contexto
# --- Flujo de consulta ---

if __name__ == "__main__":
    print("Bienvenido al sistema de consulta a ChatGPT Mini.")
    print(f"Valor Nombre usuario: {os.environ.get("NOMBRE_USUARIO_APP")}")
  #  pregunta_ChatGPT = input("Por favor, introduce tu Consulta: ")
 #   ConsultandoChatGPT(pregunta_ChatGPT)