from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llm_wrapper import GeminiLLM

class ResponseHandler:
    def __init__(self):
        self.llm = GeminiLLM()

        self.answer_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["question"],
                template="You are a helpful assistant. Answer the following question:\n\nQuestion: {question}\n\nAnswer:"
            )
        )

    def handle_user_query(self, user_query):
        try:
            answer = self.answer_chain.run({"question": user_query})
            return {"answer": answer}
        except Exception as e:
            print(f"Error: {e}")
            return {"answer": "An error occurred while generating the response."}
