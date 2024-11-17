from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from argparse import ArgumentParser
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()


class LLM():
    def __init__(self, endpoint=os.getenv("ENDPOINT_URL"), deployment=os.getenv("DEPLOYMENT_NAME"), subscription_key=os.getenv("AZURE_OPENAI_API_KEY")):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=subscription_key,
            api_version="2024-05-01-preview",
        )
        self.deployment = deployment

    def chat(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=prompt,
            max_tokens=20000,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        return completion

    def format_text(self, text):
        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{
                "role": "system",
                        "content": f"Organize these text to pretty format {text}"
            }
            ],
            stream=False
        )
        return completion.to_dict()['choices'][0]['message']['content']


def extract_text_from_pdf(pdf_file):
    loader = PyPDFLoader(pdf_file)
    pages = loader.load_and_split()
    return " ".join(list(map(lambda page: page.page_content, pages)))


def write_text_to_file(text, file_name):
    with open(file_name, "w") as f:
        f.write(text)


def upload_file_to_azure(file_path, container_name=os.getenv("CONTAINER_NAME"), connection_string=os.getenv("BLOB_CONNECTION_STRING")):
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string)

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)

    # Get the blob client
    blob_name = os.path.basename(file_path)
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    print(
        f"File {file_path} uploaded to Azure Blob Storage in container {container_name}.")


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("--pdf_file", type=str)
    args = args.parse_args()

    llm = LLM()
    pdf_file = args.pdf_file
    text = extract_text_from_pdf(pdf_file)
    formatted_text = llm.format_text(text)

    result = formatted_text if len(formatted_text) > len(text) else text

    result_path = f"extracted/{pdf_file.split('/')[-1][:-4]}.txt"
    write_text_to_file(result, result_path)
    print("Extracted to ", result_path)
    upload_file_to_azure(result_path)
