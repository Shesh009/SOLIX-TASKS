import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

load_dotenv()
groq_api_key = os.environ.get('GROQ_API_KEY')

class RetrievalChain:
    def __init__(self, qdrant_handler=None):
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

        self.prompt = ChatPromptTemplate.from_template("""
            You are an intelligent assistant helping answer questions based on a provided document context.

            Use the context below to answer the question as accurately and concisely as possible.
            If the answer is not explicitly stated in the context, respond with "The information is not available in the provided context."

            ---
            Context:
            {context}
            ---
            Question:
            {input}

            Instructions:
            - Base your answer *only* on the context above.
            - Do not assume any information that is not present in the context.
            - If the context seems to partially answer the question, acknowledge that but don't make up details.
            - Respond in full sentences, clearly and professionally.

            Answer:
            """)

        self.answer_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=self.prompt,
            document_variable_name="context"
        )

        self.qdrant_handler = qdrant_handler

    def generate_query_embedding(self, query, embedder=None):
        return embedder.embed_query(query)

    def retrieve_documents(self, query_text, embedder=None, top_k=10, score_threshold=None):
        query_embedding = self.generate_query_embedding(query_text, embedder)

        filters = Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value="report")
                )
            ]
        )

        search_results = self.qdrant_handler.search_similar(
            query_vector=query_embedding,
            top_k=top_k,
            score_threshold=score_threshold,
            filters=filters
        )

        documents = []
        for result in search_results:
            text = result.payload.get("text", "")
            if text:
                documents.append(Document(page_content=text, metadata=result.payload))

        return documents

    def generate_answer(self, query_text, embedder=None):
        retrieved_docs = self.retrieve_documents(query_text, embedder)

        answer = self.answer_chain.invoke({
            "input": query_text,
            "context": retrieved_docs
        })
        return answer