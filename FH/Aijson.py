import json
from difflib import get_close_matches
import pyttsx3
import openai
import time
import datetime
import random
import speech_recognition as sr


engine = pyttsx3.init()  
voice_id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty("voice",voice_id)
newVoiceRate = 140
engine.setProperty('rate',newVoiceRate)
engine.setProperty("voice",voice_id)

apikey="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"
chatStr = ""

def speak(audio):
    engine.say(audio)
    #print(audio)
    engine.runAndWait()

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"{query}\n ZIRA: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    print(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Find the closest matching question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def unknown():
    response = ["Could you please re-phrase that? ",                
                "What does that mean?",
                "Can you be more clear?",
                "Sorry, I did not understand?"][
        random.randrange(4)]
    speak(response)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return unknown()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=6 and hour<=12:
        speak("good morning, sir")
    elif hour>12 and hour<18:
        speak("good afternoon, sir")
    elif hour>=0 and hour<6:
        speak("good night, sir")
    else: 
        speak("good evening, sir")

# Main function to handle user input and respond
def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    wish()
    time.sleep(0.5)
    speak("how can i help you?")
    while True:
        #user_input: str = input("You: ")
        print("listening.......")
        user_input: str = takeCommand()

        if user_input.lower() == 'quit':
            break

        # Finds the best match, otherwise returns None
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            # If there is a best match, return the answer from the knowledge base
            answer: str = get_answer_for_question(best_match, knowledge_base)
            text=f"{answer}"
            print(text)
            speak(text)
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer: str = chat(user_input)

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                speak(new_answer)
                print("Bot: Thank you! I've learned something new.")


if __name__ == "__main__":
    chatbot()