import time

from elasticsearch import Elasticsearch

from settings import get_settings

if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=get_settings().es_host,
        verify_certs=False
    )
    while True:
        if es_client.ping():
            print('Elasticsearch is connected.')
            break
        print('Elasticsearch is not connected, retry in 1 seconds...')
        time.sleep(1) 