import redis
from src import config

# Cria uma instância do cliente Redis que será usada em toda a aplicação
redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    username=config.REDIS_USER, 
    password=config.REDIS_PASSWORD,
    decode_responses=True
)

try:
    redis_client.ping()
    print("[Redis] Conexão com o Redis estabelecida com sucesso.")
except redis.exceptions.ConnectionError as e:
    print(f"[Redis] ERRO: Não foi possível conectar ao Redis: {e}")
except redis.exceptions.AuthenticationError:
    print("[Redis] ERRO: Falha na autenticação. Verifique usuário e senha.")