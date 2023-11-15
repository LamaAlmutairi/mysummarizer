import os 
import openai
import streamlit as st
import re 

from PyPDF2 import PdfReader 
from dotenv import load_dotenv 

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_files():
        text = ""
        data_dir = os.path.join(os.getcwd(),"data")
        for filename in os.listdir(data_dir):
                if filename.endswith(".txt"):
                        with open(os.path.join(data_dir,filename),"r") as f:
                                text += f.read()
        return text                        


def extract_text_from_pdf(pdf_file):
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
                content=page.extract_text()
                if content:
                        text+=content
        return text

def get_response(text,summary_length,summary_language):

        sentences="3-5" if summary_length=="3-5 Sentences" else "6-8"
        summary_lang="Arabic" if summary_language=="Arabic" else "English"

        prompt = f""" 
                You are an expert in summarizing text. You will be given a text delimited by four backquotes,
                Make sure to capture the main points, key arguements, and any supporting evidence presented in the article.
                Your summary should be informative and well-structured, consisting of {sentences} sentences.
                Your summary should be in {summary_lang} language.

                text:`{text}`
                """
        client=openai.OpenAI()        
        response = client.chat.completions.create(  

                model = "gpt-3.5-turbo",
                messages=[
                        {
                                "role": "system",
                                "content":prompt,
                        },
                ],
        )
        return response.choices[0].message.content

def word_count(paragraph):
        word_list = paragraph.split()
        return len(word_list)

def sentence_count(paragraph):
        sentence_list = paragraph.split('.')
        return len(sentence_list)

def main():
        st.set_page_config(
                page_title="Summarizer",
                page_icon="🎀" 
        )
        st.title("AI Summarizer tool")
        st.divider()

        option = st.radio("Select input type",("Text","PDF"))
        s_length = st.radio("Select length of the summary",("3-5 Sentences","6-8 Sentences"))
        lang=st.selectbox("Select language of the summary",("English","Arabic"))
        if option == "Text":
                
                user_input = st.text_area("Enter Text","")
                if st.button("Summarize") and user_input!= "":
                        response=get_response(text=user_input,summary_length=s_length,summary_language=lang)
                        st.subheader("Summary")
                        st.markdown(f">{response}")
                        
                        st.subheader(f'Words:{word_count(response)}')
                        st.subheader(f'Sentences: {sentence_count(response)}')

                else:
                        st.error("Please enter text")
        else:
                uploaded_file=st.file_uploader("Choose a PDF file",type="pdf")
 
                if st.button("Summarize") and uploaded_file is not None:
                        text= extract_text_from_pdf(uploaded_file)
                        response=get_response(text=text,summary_length=s_length,summary_language=lang)
                        st.subheader("Summary")
                        st.markdown(f">{response}")
##
                        st.subheader(f'Words:{word_count(response)}')
                        st.subheader(f'Sentences: {sentence_count(response)}')
                        
                else:
                        st.error("Please upload a file")


if __name__=="__main__":
        main()