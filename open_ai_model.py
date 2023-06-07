import openai

def load_file_contents(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()
    
def openai_chatbot(api_key,file_contents, user_input):
    openai.api_key = api_key
    # prompt = f"You are KT Informatik. Based on your information about KT Informatik you will answer. Now answer the following question.\n\n{user_input} ->"

    prompt = [{"role": "system", "content": f"Suppose You are KT Informatik's Chatbot. You will Provide Project information informatik Based on the following information:\n{file_contents}. If you do not find the informtion above information Just answere. 'I don't know about it'. Or If you need more information Just ask the user for more information. You will provide only estimation not more than that."}]

    # if len(messages) != 0:
    #     for message in messages:
    #         prompt.append({"role": "user", "content": message["question"]})
    #         prompt.append({"role": "assistant", "content": message["message"]})
   

    prompt.append({"role": "user", "content": user_input})


    # prompt = f"Suppose You are KT Informatik. You will answere like KT informatik Based on the following information:\n{file_contents}. If you do not find the informtion above information Just answere. 'I don't know about it' otherwise\n\nUser: {user_input}\nChatbot:"
    
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=256,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
    
    
    generated_text = response.choices[0].message.content.strip()
    return generated_text