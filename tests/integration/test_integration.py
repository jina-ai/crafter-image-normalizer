import pytest
import os
import numpy as np
from PIL.Image import fromarray

from jina import Flow, Document
from jinahub.image.normalizer import ImageNormalizer

cur_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def numpy_image_uri(tmpdir):
    blob = np.random.randint(255, size=(96, 96, 3), dtype='uint8')
    im = fromarray(blob)
    uri = os.path.join(tmpdir, 'tmp.png')
    im.save(uri)
    return uri


def data_generator(num_docs, numpy_image_uri):
    for i in range(num_docs):
        doc = Document(uri=numpy_image_uri)
        doc.convert_image_uri_to_blob()
        yield doc


def test_use_in_flow(numpy_image_uri):
    with Flow.load_config('flow.yml') as flow:
        data = flow.post(
            on='/index', inputs=data_generator(5, numpy_image_uri), return_results=True
        )
        for doc in data[0].docs:
            assert doc.blob.shape == (64, 64, 3)
