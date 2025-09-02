import requests
import json
from src import config

def send_text_message(recipient_jid: str, text: str):
    """
    Envia uma mensagem de texto para um destinatário usando a Evolution API.
    """
    recipient_number = recipient_jid.split('@')[0]

    
    url = f"{config.EVOLUTION_API_URL}/message/sendText/{config.EVOLUTION_INSTANCE_NAME}"

    
    payload = {
        "number": recipient_number,
        "text": text
    }

    headers = {
        "Content-Type": "application/json",
        "apikey": config.EVOLUTION_API_KEY
    }

    print(f"[Evolution API] Enviando para a URL: {url}")
    print(f"[Evolution API] Enviando payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        print(f"[Evolution API] Resposta recebida: {response.status_code}")
        print(f"[Evolution API] Corpo da resposta: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[Evolution API] ERRO ao enviar mensagem: {e}")
        return False