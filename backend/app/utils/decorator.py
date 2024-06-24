import functools
from elasticsearch.exceptions import ConnectionError, NotFoundError, RequestError
from ..logger import Logger

logger = Logger(__name__)


def handle_elasticsearch_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundError as e:
            logger.error(f"Index or document not found: {e}")
        except RequestError as e:
            logger.error(f"Invalid request: {e}")
        except ConnectionError as e:
            logger.error(f"Connection failed: {e}")
        except Exception as e:
            logger.error(f'General Error {str(e)}')

    return wrapper
