from flask import Blueprint, current_app, jsonify, request
import openai
import os
from flask_cors import CORS
from geopy.geocoders import Nominatim
from datetime import datetime

recommendations = Blueprint('recommendations', __name__)

CORS(recommendations)

@recommendations.route("/api/login", methods=["POST"])
def login():
    db = current_app.config["MONGO_DB"]
    users_collection = db["clientData"]

    # Obtener el correo del request JSON
    email = request.json.get("email")  
    if not email:
        return jsonify({"error": "Correo es requerido"}), 400

    # Buscar usuario en MongoDB (ajustando al campo correcto)
    user = users_collection.find_one({"Usuario.Correo": email}, {"_id": 0})  # Excluye _id
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(user), 200


def get_personalized_prompt(correo):

    openai.api_key = os.getenv("GPT_API_KEY")

    # Connect to MongoDB
    db = current_app.config["MONGO_DB"]
    
    # Access collections
    cliente = db['clientData']
    clima = db['clima']
    noticias = db['noticias']
    seguros = db['seguros']
    
    # Obtener datos del cliente
    cliente_data = cliente.find_one({"Usuario.Correo": correo})

    #Ubicacion si no viaja
    geolocator = Nominatim(user_agent="mi_aplicacion")
    latitud = cliente_data["UbicacionPersona"]["Latitud"]
    longitud = cliente_data["UbicacionPersona"]["Longitud"]
    ubicacion = geolocator.reverse((latitud, longitud))
    ciudad = ubicacion.raw['address'].get('city', '')

    print(f"Datos del cliente: {cliente_data}")  # Debugging line
    
    if not cliente_data:
        return "Cliente no encontrado"
    
    # Extraer información del calendario
    calendar_events = cliente_data.get("Calendar", [])
    destinos_viaje = []
    
    if not calendar_events:
        destino = ciudad
        fecha_inicio = datetime.now().strftime("%Y-%m-%d")
        fecha_fin = datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
        destinos_viaje.append({
            "destino": destino,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        })
    else:
        for event in calendar_events:
            if "Destino" in event:
                destino = event["Destino"]
                fecha_inicio = event["FechaInicio"]
                fecha_fin = event["FechaFin"]
                destinos_viaje.append({
                    "destino": destino,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                })
    
    
    # Obtener clima para los destinos - corregido para la estructura real
    clima_destinos = {}
    for viaje in destinos_viaje:
        destino = viaje["destino"]
        # Buscar directamente por el nombre de la ciudad
        clima_destino = clima.find_one({"Nombre": destino})
        
        if clima_destino:
            # Filtrar solo las fechas relevantes para el viaje
            fechas_relevantes = {}
            fecha_inicio = viaje["fecha_inicio"]
            fecha_fin = viaje["fecha_fin"]
            
            for fecha, datos in clima_destino.get("Predicciones", {}).items():
                if fecha >= fecha_inicio and fecha <= fecha_fin:
                    fechas_relevantes[fecha] = datos
            
            if fechas_relevantes:
                clima_destinos[destino] = fechas_relevantes
    
    # Obtener noticias relevantes para los destinos
    noticias_destinos = []
    for viaje in destinos_viaje:
        destino = viaje["destino"]
        # Buscar noticias relacionadas con el destino
        noticias_destino = list(noticias.find({
            "$or": [
                {"ubicacion.ciudad": destino},
                {"ubicacion.pais": destino},
                {"titularNoticia": {"$regex": destino, "$options": "i"}},
                {"noticia": {"$regex": destino, "$options": "i"}}
            ]
        }))
        
        noticias_destinos.extend(noticias_destino)
    
    # Obtener seguros contratados
    seguros_cliente = cliente_data.get("SegurosContratados", [])
    
    # Obtener catálogo de seguros
    catalogo_seguros = list(seguros.find({}, {"_id": 0}))
    
    # Construir el prompt personalizado
    system_message = f"""
        # Asistente de Recomendación Personalizada de AXA Seguros
        Eres un asistente virtual especializado en recomendaciones de seguros de AXA, diseñado para ofrecer sugerencias personalizadas y alertas de seguridad relevantes.

        ## DATOS DE ENTRADA
        - Cliente: {cliente_data['Usuario']['Nombre']}
        - Seguros actuales: {seguros_cliente}
        - Agenda y eventos programados: {calendar_events}
        - Catálogo de seguros AXA: {catalogo_seguros}
        - Información contextual:
          - Clima en destinos: {clima_destinos}
          - Noticias relevantes: {noticias_destinos}

        ## INSTRUCCIONES
        1. Analiza el perfil del cliente y sus seguros actuales.
        2. Revisa su agenda para identificar posibles necesidades futuras de protección.
        3. Examina la información contextual para detectar riesgos inmediatos.
        4. Consulta nuestro catálogo para identificar productos relevantes.

        ## FORMATO DE RESPUESTA
        1. Saluda al cliente por su nombre de forma cordial.
        2. Menciona brevemente los seguros que ya tiene contratados.
        3. Recomienda 1-2 productos específicos de nuestro catálogo que cubran necesidades no atendidas, explicando claramente el beneficio para su situación particular.
        4. Alerta sobre cualquier riesgo relevante basado en la información contextual o su agenda.
        5. Finaliza con una invitación a contactar con su asesor personal para más información tlf +34 600 600 600.

        Mantén un tono profesional, cercano y centrado en las necesidades del cliente, no en la venta.
    """
    
    return system_message, cliente_data['Usuario']['Nombre']

def chat_with_gpt(system_prompt, user_query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Puedes cambiar a "gpt-3.5-turbo" si prefieres
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al comunicarse con ChatGPT: {str(e)}"


@recommendations.route("/api/recommendations", methods=["POST"])
def interactive_chat_session():
    correo = request.json.get("email")
    system_prompt, nombre_cliente = get_personalized_prompt(correo)
    
    print(f"\n--- Iniciando sesión de chat para {nombre_cliente} ---\n")
    
    # Mensaje inicial automático
    initial_query = "Hola, ¿qué recomendaciones tienes para mí hoy?"
    response = chat_with_gpt(system_prompt, initial_query)
    print(f"Asistente AXA: {response}\n")

    return jsonify({"response": response}), 200