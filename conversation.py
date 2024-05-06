from train import chain

chat_history = []
def generate_answer(question):
    global chat_history
    query = "Prompt: Kamu adalah chatbot tanya jawab cerdas untuk menjawab pertanyaan seputar komponen cadangan. menjawab menggunakan bahasa indonesia dengan jelas dan lengkap. jawablah sesuai data yang saya berikan diembedding "+question
    result = chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result['answer']))
    return(result['answer'])