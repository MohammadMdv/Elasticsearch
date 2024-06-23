# built-in
import random

# third-side
import yaml
from faker import Faker

# my-own
from src.logger import Logger


class FakerWrapper:
    def __init__(self):
        self.logger = Logger(__name__)
        # Load the mapping from a YAML file
        with open('data/faker_mappings.yml', 'r') as f:
            self.mapping = yaml.safe_load(f)['mappings']

        # Create an instance of the Faker class
        self.fake = Faker()
        self.logger.info("Initialize FakerWrapper Class")

    def generate_data(self, mapping=None, num_documents=1) -> list:
        """
        Generate fake data based on the provided mapping.

        @:param mapping (dict): Mapping of fields to Faker providers and their arguments.
        @:param  num_documents (int): Number of fake documents to generate.
        @:return: list: List of generated fake documents.
        """
        if mapping is None:
            mapping = self.mapping

        for i in range(num_documents):
            document = {}
            for field, value in mapping.items():
                if value['faker'] == 'uniform':
                    # If the Faker provider is uniform, get the kwargs and generate a random float within the range.
                    kwargs = value.get('kwargs', {})
                    min_value = kwargs.get('min_value', 0)
                    max_value = kwargs.get('max_value', 1)
                    document[field] = round(random.uniform(min_value, max_value), 2)
                else:
                    # Otherwise, get the Faker provider and its kwargs and call the provider.
                    faker_method = value.get('faker')
                    kwargs = value.get('kwargs', {})
                    document[field] = getattr(self.fake, faker_method)(**kwargs)
            yield document

