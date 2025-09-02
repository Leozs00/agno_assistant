import uvicorn
import asyncio
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
import json

from src.assistant.agent import run_assistant
from src.services.evolution_api import send_text_message
from src.redis_client import redis_client

MESSAGE_BUFFER_SECONDS = 8

app = FastAPI(title="WhatsApp Agno Assistant")

async def process_user_buffer(sender: str):
    print(f"[Buffer] Tarefa iniciada para {sender}. Aguardando {MESSAGE_BUFFER_SECONDS} segundos...")
    
    await asyncio.sleep(MESSAGE_BUFFER_SECONDS)
    redis_key = f"buffer:{sender}"
    try:
        if not redis_client.exists(redis_key):
            print(f"[Buffer] Tarefa para {sender} cancelada (uma nova mensagem chegou).")
            return
        messages = redis_client.lrange(redis_key, 0, -1)
        messages.reverse()
        if not messages:
            print(f"[Buffer] Tarefa para {sender} finalizada sem mensagens.")
            return
        print(f"[Buffer] Processando {len(messages)} mensagens para {sender}.")
        full_message = "\n".join(messages)
        redis_client.delete(redis_key)
        assistant_response = run_assistant(user_message=full_message, conversation_id=sender)
        print("="*50)
        print(f"Resposta do Assistente para {sender}: {assistant_response}")
        print("="*50)
        if assistant_response:
            message_parts = assistant_response.strip().split('\n')
            for part in message_parts:
                if part.strip():
                    send_text_message(recipient_jid=sender, text=part.strip())
                    await asyncio.sleep(1.5)
    except Exception as e:
        print(f"[Buffer] ERRO ao processar buffer para {sender}: {e}")


@app.get("/")
async def root():
    return {"status": "ok", "message": "Servidor do assistente está rodando."}


@app.post("/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    print(">>> Webhook Recebido! <<<")
    data = await request.json()
    
    message_data = data.get('data', {})
    message_text = message_data.get('message', {}).get('conversation')
    
    if message_text:
        key_data = message_data.get('key', {})
        
        
        sender_jid = key_data.get('remoteJid')
        
       
        is_from_me = key_data.get('fromMe', False)

        
        if sender_jid and not is_from_me:
            redis_key = f"buffer:{sender_jid}"
            print(f"[Webhook] Adicionando mensagem ao buffer para {sender_jid}: '{message_text}'")
            
            redis_client.lpush(redis_key, message_text)
            redis_client.expire(redis_key, MESSAGE_BUFFER_SECONDS + 2)
            
            background_tasks.add_task(process_user_buffer, sender_jid)

    return {"status": "ok", "message": "recebido"}