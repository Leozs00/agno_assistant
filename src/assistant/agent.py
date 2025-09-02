from agno.agent import Agent 
from agno.models.google import Gemini
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src import config
from src.assistant import prompt
from src.rag.retriever import retriever

assistant_agent = None

def busca_em_documento_pdf(query: str) -> str:
    """Use esta ferramenta para buscar e responder perguntas baseadas em um documento PDF. Esta é a fonte primária de conhecimento sobre este tópico."""
    print(f"[Tool] Buscando no PDF por: '{query}'")
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    if not context:
        return "Nenhuma informação relevante foi encontrada no documento sobre este tópico."
    print(f"[Tool] Contexto encontrado:\n{context[:500]}...")
    return context

try:
    llm_model = Gemini(
        api_key=config.GOOGLE_API_KEY,
        id="gemini-2.5-flash" 
    )
    print(f"[Agente] Instância do Gemini ('{llm_model.id}') criada com sucesso.")
    
    # Não vamos mais passar a memória para o agente na criação.
    # Vamos gerenciá-la externamente.
    assistant_agent = Agent(
        instructions=prompt.SYSTEM_PROMPT_PT,
        model=llm_model,
        tools=[busca_em_documento_pdf]
    )
    print("[Agente] Instância do Agente criada com sucesso.")

except Exception as e:
    print(f"[Agente] ERRO CRÍTICO durante a inicialização: {e}")
    assistant_agent = None


def run_assistant(user_message: str, conversation_id: str) -> str:
    if not assistant_agent:
        return "Desculpe, o assistente de IA não está funcionando no momento."

    print(f"[Agente] Processando mensagem para a conversa '{conversation_id}': '{user_message}'")
    
    try:
        # --- GERENCIAMENTO DE MEMÓRIA ---

        # 1. Conectamos ao histórico da sessão no Redis.
        redis_url = f"redis://{config.REDIS_USER or ''}:{config.REDIS_PASSWORD or ''}@{config.REDIS_HOST}:{config.REDIS_PORT}"
        chat_history = RedisChatMessageHistory(url=redis_url, session_id=conversation_id)

        # 2. Carregamos as mensagens anteriores.
        previous_messages = chat_history.messages
        print(f"[Memória] Carregadas {len(previous_messages)} mensagens do histórico.")

        # 3. Montamos a lista de mensagens para o agente, incluindo o histórico.
        messages_for_agent = [
            SystemMessage(content=prompt.SYSTEM_PROMPT_PT)
        ]
        # Adicionamos o histórico anterior
        messages_for_agent.extend(previous_messages)
        # Adicionamos a nova mensagem do usuário
        messages_for_agent.append(HumanMessage(content=user_message))

        # 4. Executamos o agente com a lista completa de mensagens.
        # Passamos a conversa inteira em vez de apenas a última mensagem.
        response_object = assistant_agent.run(messages_for_agent)
        assistant_text_response = response_object.content
        
        # 5. Salvamos a interação atual de volta no histórico.
        chat_history.add_user_message(user_message)
        chat_history.add_ai_message(assistant_text_response)
        print("[Memória] Nova interação salva no Redis.")
        
        
        print(f"[Agente] Resposta gerada: '{assistant_text_response}'")
        return assistant_text_response
    except Exception as e:
        print(f"[Agente] ERRO durante a execução do agente: {e}")
        return "Desculpe, ocorreu um erro ao processar sua mensagem."