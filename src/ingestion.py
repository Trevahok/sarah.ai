import json 
import os 
from tqdm.auto import tqdm
from uuid import uuid4
from typing import List

from dotenv import load_dotenv
import pinecone

from src.lib import init_pinecone, embedder, chunkifier


load_dotenv()

def load_dataset():
    file = open('./data/scraped_data.json', 'r')
    dataset = json.load(file)
    file.close()
    return dataset

PINECONE_INDEX = os.getenv("PINECONE_INDEX")
print("SETTING UP PINECONE...")
init_pinecone()

embed = embedder()
chunkifier = chunkifier()



if __name__ == '__main__':

    print("LOADING DATASET...")
    dataset = load_dataset()
    index = pinecone.GRPCIndex(PINECONE_INDEX)

    print('PINECONE INDEX: ', index.describe_index_stats()  )



    batch_limit = 100

    texts = []
    metadatas = []

    for i, row in enumerate(tqdm(dataset)):
        if row['data'] in ['', None] :
            print("SKIPPING : ", row['url'] )
        print('PROCESSING: ', row['url'])
        metadata = {
            'source': row['url'],
        }
        # now we create chunks from the record text
        record_texts = chunkifier.split_text(row['data'])
        # create individual metadata dicts for each chunk
        record_metadatas = [{
            "chunk": j, "text": text, **metadata
        } for j, text in enumerate(record_texts)]
        # append these to current batches
        texts.extend(record_texts)
        metadatas.extend(record_metadatas)
        # if we have reached the batch_limit we can add texts
        if len(texts) >= batch_limit:
            ids = [str(uuid4()) for _ in range(len(texts))]
            embeds = embed.embed_documents(texts)
            index.upsert(vectors=zip(ids, embeds, metadatas))
            texts = []
            metadatas = []

    if len(texts) > 0:
        ids = [str(uuid4()) for _ in range(len(texts))]
        embeds = embed.embed_documents(texts)
        index.upsert(vectors=zip(ids, embeds, metadatas))


    print("COMPLETED SUCCESSFULLY...")
    print(index.describe_index_stats())


def ingest(strings: List[str], metadata: List[dict], index_name: str):
    index = pinecone.GRPCIndex(index_name)
    print('setting index: ', index_name)
    for i,row in enumerate(strings):
        record_texts = chunkifier.split_text(row)
        print(metadata[i].values())
        record_metadatas = [{
            "chunk": j, "text": text + '\n\n'.join(map(str,metadata[i].values())) , **metadata[i]
        } for j, text in enumerate(record_texts)]

        ids = [str(uuid4()) for _ in range(len(record_texts))] 
        embeds = embed.embed_documents(record_texts)
        index.upsert(vectors=zip(ids, embeds, record_metadatas))
    print("Done ingesting file...")
    print(index.describe_index_stats())






