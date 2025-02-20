from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

def analyze_resume(resume_text):
    prompt = PromptTemplate(
        template="Analyze the following resume text and suggest improvements:\n\n{resume_text}",
        input_variables=["resume_text"],
    )
    response = llm(prompt.format(resume_text=resume_text))
    return response
