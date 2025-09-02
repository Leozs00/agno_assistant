import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Configurações do Redis ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_USER = os.getenv("REDIS_USER") or None
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None

# --- Configurações da Evolution API ---
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
EVOLUTION_INSTANCE_NAME = os.getenv("EVOLUTION_INSTANCE_NAME")

# Validação simples para garantir que as variáveis essenciais foram carregadas
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi definida.")
if not EVOLUTION_API_URL:
    raise ValueError("A variável de ambiente EVOLUTION_API_URL não foi definida.")