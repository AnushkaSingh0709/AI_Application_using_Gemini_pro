import os
import json
import google.generativeai as genai

# get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_directory}/config.json"
config_data = json.load(open(config_file_path))

# loading the api key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# CONFIGURING GOOGLE.GENERATIVEAI WITH API KEY
genai.configure(api_key=GOOGLE_API_KEY)


def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

#function for image captioning
def gemini_1_5_flash_response(prompt, image):
    # Initialize the new model
    gemini_1_5_flash_model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate content using the new model
    response = gemini_1_5_flash_model.generate_content([prompt, image])

    # Extract and return the result
    result = response.text
    return result

#function to get embeddings for text
def embedding_model_response(input_text):
    embedding_model="models/text-embedding-004"
    embedding=genai.embed_content(model=embedding_model,
                                  content=input_text,
                                  task_type="retrieval_document")
    embedding_list=embedding["embedding"]
    return embedding_list

#function to get a response from gemini-pro-model
def gemini_pro_response(user_prompt):
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    response=gemini_pro_model.generate_content(user_prompt)
    result=response.text
    return result
