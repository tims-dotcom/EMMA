import os 
from groq import Groq

os.environ['GROQ_API_KEY'] = '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'

Client = Groq()

chat_history = [{
    'role': 'system',
    'content': 'Ти Джарвіс як з фільма залізна людина, але твоє імя Emma маєш відповідати коротко лаконічно'
}]

def ask_emma(user_text):
    chat_history.append({
        "role": "user",
        "content": user_text
    })
    print("Обробка ...")

    completion = Client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=chat_history,
        temperature=0.7,
        max_tokens=1024
    )

    emma_response = completion.choices[0].message.content

    chat_history.append({
        "role": "assistant",
        "content": emma_response
    })

    return emma_response

if __name__ == "__main__":
    print("E.M.M.A: активована (напишіть вихід для завершення)")

    while True:
        user_input = input("\n Ти:")

        if user_input.lower == "вихід":
            print("E.M.M.A: відключаю живлення, до побаченя")
            break
        response = ask_emma(user_input)
        print("E.M.M.A:" + response)