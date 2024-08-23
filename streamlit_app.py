import streamlit as st
from openai import OpenAI
import io
from docx import Document
import PyPDF2

def read_file(file):
    file_type = file.name.split('.')[-1].lower()
    if file_type == 'txt':
        return file.getvalue().decode()
    elif file_type == 'md':
        return file.getvalue().decode()
    elif file_type == 'docx':
        doc = Document(io.BytesIO(file.getvalue()))
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    elif file_type == 'pdf':
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
        return '\n'.join([page.extract_text() for page in pdf_reader.pages])
    else:
        return "Unsupported file format"

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .md, .docx, or .pdf)", type=("txt", "md", "docx", "pdf")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file and question.
        document = read_file(uploaded_file)
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)