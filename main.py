from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth, helpers
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import OpenSearchVectorSearch
from langchain.document_loaders import TextLoader
import boto3
import json
import os
import getpass

host = "yl0p9uqdvbuhdvg1hthd.us-east-1.aoss.amazonaws.com"
port = 443
region = "us-east-1"
service = "aoss"
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    pool_maxsize=20
)

try:
    response = client.indices.get("espn-news")
    print(json.dumps(response, indent=2))
except Exception as ex:
    print(ex)

q = 'NFL'
query = {
  'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['headline']
    }
  }
}

response = client.search(
    body=query,
    index='espn-news'
)

print(response)

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")



