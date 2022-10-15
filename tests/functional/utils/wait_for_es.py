import logging

from elasticsearch import Elasticsearch

from settings import get_settings
from utils.backoff import backoff


class ElasticsearchIsNotConnected(Exception):
    """Исключение вызываемое если не удалось подключиться к Elasticsearch."""
    pass
    

@backoff()
def wait_for_es():
    es_client = Elasticsearch(
        hosts=get_settings().es_host,
        verify_certs=False
    )
    
    if es_client.ping():
        logging.info('Elasticsearch is connected.')
        return
    
    raise ElasticsearchIsNotConnected('Elasticsearch is not connected.')


if __name__ == '__main__':
    logging.exception('gddgdgdgdgdgdgdgdgd dgdgdgfdgd gdddg 3#####################################')
    wait_for_es()