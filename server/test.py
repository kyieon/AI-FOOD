from dotenv import load_dotenv
import os
import google.generativeai as gemini

load_dotenv()

API_KEY = os.environ.get("API_KEY")

gemini.configure(api_key=API_KEY)
model = gemini.GenerativeModel("gemini-pro")

# Single
response = model.generate_content("내가 오늘 먹고 싶은 걸 알려 줘")
print(response.text)


#
#
# # Prompt
# chat = model.start_chat(history=["나는 참고로 짬뽕을 좋아해"])
#
# response = chat.send_message("내가 오늘 먹고 싶은 걸 알려 줘")
# print(response.text)
