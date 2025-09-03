# from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import settings
from langchain_openai import ChatOpenAI

class AIEngine:
    def __init__(
        self,
        model: str = "llama3-70b-8192",
        temperature: float = 0.3,
        system_prompt: str = None
    ):
        self.system_prompt = system_prompt or self.__default_prompt()

        self.model = ChatOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            model=model,
            temperature=temperature
        )

    def __setup_chain(self, model=None):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{query}")
        ])
        return prompt | (model or self.model)

    def __default_prompt(self) -> str:
        return "You are an intelligent text evaluator AI. You compare two pieces of text and provide insightful, structured feedback."

    def evaluate(self, text_1: str, text_2: str) -> str:
        prompt_input = f"""
        Compare the following two pieces of text.

        Text 1:
        {text_1}

        Text 2:
        {text_2}

        Now do the following:
        1. Identify similarities and differences
        2. Point out missing or complementary information
        3. Suggest improvements to align both
        4. Give a match score out of 10
        """
        chain = self.__setup_chain()
        response = chain.invoke({"query": prompt_input})
        return response.content

    def suggest_resume_improvements(self, resume_text: str, job_description: str = "") -> str:
        prompt_input = f"""
        Resume:
        {resume_text}

        Job Description:
        {job_description}
        """
        chain = self.__setup_chain()
        response = chain.invoke({"query": prompt_input})
        return response.content
