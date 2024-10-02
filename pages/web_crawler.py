import os
import streamlit as st
import json
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from serpapi import GoogleSearch


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

system_template = """Use the following pieces of context to know more about the
company or brand you're going to create content for. Create content for the company based on the following context.
"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(messages)
chain_type_kwargs = {"prompt": prompt}


def main():

    st.title('🦜🔗Website')
    st.subheader('Enter your website URL to write content for  your company,')

    url = st.text_input("Insert The website URL")

    prompt = """Your job is to analyze the given context of a company or brand as a Business analyst and content writer.
    Output a report in JSON describing the work they're doing. The format should be as follows,if you 
    found a blog or articles enter in the way you should create content like the author :

    {
        "Brand Name": "Company Name",
        "Example content": "Description of the company's work",
        "Niche targeting": "Target audience or market",
        "Key Words":"Top Keywords for content",
        "Example contents": "you should write the example content of the brand or company so as to reprduce the content"
    }
    """
    if st.button("Submit Query"):
        ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
        DB_DIR: str = os.path.join(ABS_PATH, "../db")

        # Load data from the specified URL
        loader = WebBaseLoader(url)
        data = loader.load()

        # Split the loaded data
        text_splitter = CharacterTextSplitter(separator='\n',
                                              chunk_size=500,
                                              chunk_overlap=40)

        docs = text_splitter.split_documents(data)

        # Create OpenAI embeddings
        openai_embeddings = OpenAIEmbeddings()

        # Create a Chroma vector database from the documents
        vectordb = Chroma.from_documents(documents=docs,
                                         embedding=openai_embeddings,
                                         persist_directory=DB_DIR)

        vectordb.persist()

        # Create a retriever from the Chroma vector database
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        # Use a ChatOpenAI model
        llm = ChatOpenAI(model_name='gpt-3.5-turbo')


        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)


        response = qa(prompt)

        st.write(response)

        result_json = json.loads(response.get("result", "{}"))

        # Extract relevant information from the response and create a JSON report
        brand_name = result_json.get("Brand Name", "")
        example_content = result_json.get("Example content", "")
        niche_targeting = result_json.get("Niche targeting", "")
        keywords = result_json.get("Key Words", "")



        def get_top_keywords_for_list(keywords, location, api_key):
            all_top_keywords = {}

            for keyword in keywords:
                params = {
                    "q": keyword,
                    "location": location,
                    "hl": "en",
                    "gl": "us",
                    "google_domain": "google.com",
                    "api_key": api_key
                }

                search = GoogleSearch(params)
                results = search.get_dict()

                # Extract top keywords from the results
                top_keywords = []
                for organic_result in results.get('organic_results', []):
                    top_keywords.append(organic_result.get('title'))

                all_top_keywords[keyword] = top_keywords

            return all_top_keywords


        google_api_key =os.getenv("GOOGLE_API_KEY")

        # Location for the search
        location = "Austin, Texas, United States"

        keywords = keywords.split(', ')




        result_keywords = get_top_keywords_for_list(keywords, location, google_api_key)

        report = {
            "Brand Name": brand_name,
            "Example content": example_content,
            "Niche targeting": niche_targeting,
            "Key Words": keywords,
            "Top Keywords": result_keywords
        }


        save_path = "../output_report.json"
        with open(save_path, "w") as json_file:
            json.dump(report, json_file, indent=4)


        st.title('Top Keywords Analysis')
        st.subheader(f'Results for Brand: {brand_name}')

        for original_keyword, top_keywords in result_keywords.items():
            st.write(f"Last 3 Keywords for '{original_keyword}':")
            for index, kw in enumerate(top_keywords[-3:], start=1):
                st.write(f"{index}. {kw}")



        st.text(report)

if __name__ == '__main__':
    main()
