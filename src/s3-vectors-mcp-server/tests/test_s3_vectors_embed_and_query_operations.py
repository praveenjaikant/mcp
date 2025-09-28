import datasets
import os
import pytest
from awslabs.s3_vectors_mcp_server.consts import IMAGE_EMBEDDING_MODELS
from awslabs.s3_vectors_mcp_server.models import (
    CreateIndexRequest,
    EmbedAndQueryTextRequest,
    EmbedAndStoreFileRequest,
    EmbedAndStoreTextRequest,
)
from awslabs.s3_vectors_mcp_server.server import (
    create_index,
    embed_and_query,
    embed_and_store_file,
    embed_and_store_text,
)
from tests.helpers import process_stdout_results


@pytest.mark.asyncio
async def test_create_text_index_for_retrieval():
    """Test create_index tool for text-based index."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'text-vector-index'
    dimension = 1024

    create_index_request = CreateIndexRequest(
        vectorBucketName=bucket_name, indexName=index_name, dimension=dimension
    )

    results = await create_index(create_index_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200


@pytest.mark.asyncio
async def test_create_text_vectors_for_retrieval():
    """Test embed_and_store_text tool with raw text input."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'text-vector-index'
    # text_value = 'hello world'
    content_type = 'text'
    dimension = 1024

    data = datasets.load_dataset('roneneldan/TinyStories')

    for context_data in data.data['train'][0][:10]:
        text_value = context_data.as_py()

        embed_and_store_text_request = EmbedAndStoreTextRequest(
            vectorBucketName=bucket_name, indexName=index_name, textValue=text_value
        )

        results = await embed_and_store_text(embed_and_store_text_request)

        assert results['bucket'] == bucket_name
        assert results['index'] == index_name
        assert results['contentType'] == content_type
        assert results['embeddingDimensions'] == dimension


@pytest.mark.asyncio
async def test_retrieval_from_raw_text_vectors():
    """Test embed_and_query tool with raw text query."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'text-vector-index'
    query_input = 'What did Lily and her mom use the needle for?'
    query_type = 'text'
    dimension = 1024
    top_k = 3

    embed_and_query_request = EmbedAndQueryTextRequest(
        vectorBucketName=bucket_name,
        indexName=index_name,
        queryInput=query_input,
        topK=str(top_k),
        returnDistance=True,
    )

    results = await embed_and_query(embed_and_query_request)
    processed_results = process_stdout_results(results)

    assert processed_results['summary']['queryType'] == query_type
    assert processed_results['summary']['index'] == index_name
    assert processed_results['summary']['queryDimensions'] == dimension
    assert processed_results['summary']['resultsFound'] == top_k


@pytest.mark.asyncio
async def test_retrieval_from_file_text_vectors():
    """Test embed_and_query tool with local file query."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'text-vector-index'
    query_input = './data/text_query/text_query.txt'
    query_type = 'text'
    dimension = 1024
    top_k = 3

    embed_and_query_request = EmbedAndQueryTextRequest(
        vectorBucketName=bucket_name, indexName=index_name, queryInput=query_input, topK=str(top_k)
    )

    results = await embed_and_query(embed_and_query_request)
    processed_results = process_stdout_results(results)

    assert processed_results['summary']['queryType'] == query_type
    assert processed_results['summary']['index'] == index_name
    assert processed_results['summary']['queryDimensions'] == dimension
    assert processed_results['summary']['resultsFound'] == top_k


@pytest.mark.asyncio
async def test_create_image_index_for_retrieval():
    """Test create_index tool for image-based index."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'image-vector-index'
    dimension = 1024

    create_index_request = CreateIndexRequest(
        vectorBucketName=bucket_name, indexName=index_name, dimension=dimension
    )

    results = await create_index(create_index_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200


@pytest.mark.asyncio
async def test_create_image_vectors_for_retrieval():
    """Test embed_and_store_file tool with local image files input."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'image-vector-index'
    content_type = 'image'
    dimension = 1024

    DIR = './data/image_query'

    for file in os.listdir(DIR):
        file_path = f'{DIR}/{file}'

        embed_and_store_file_request = EmbedAndStoreFileRequest(
            vectorBucketName=bucket_name,
            indexName=index_name,
            modality=content_type,
            modelId=IMAGE_EMBEDDING_MODELS[0],
            file=file_path,
        )

        results = await embed_and_store_file(embed_and_store_file_request)

        assert results['bucket'] == bucket_name
        assert results['index'] == index_name
        assert results['contentType'] == content_type
        assert results['embeddingDimensions'] == dimension


@pytest.mark.asyncio
async def test_retrieval_from_s3_file_image_vectors():
    """Test embed_and_query tool with S3 image file query."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'image-vector-index'
    query_input = 's3://s3-bucket-for-mcp-server-test/image/pizza.webp'
    query_type = 'image'
    dimension = 1024
    top_k = 3

    embed_and_query_request = EmbedAndQueryTextRequest(
        vectorBucketName=bucket_name,
        indexName=index_name,
        queryInput=query_input,
        topK=str(top_k),
        modelId=IMAGE_EMBEDDING_MODELS[0],
    )

    results = await embed_and_query(embed_and_query_request)
    processed_results = process_stdout_results(results)

    assert processed_results['summary']['queryType'] == query_type
    assert processed_results['summary']['index'] == index_name
    assert processed_results['summary']['queryDimensions'] == dimension
    assert processed_results['summary']['resultsFound'] == top_k


@pytest.mark.asyncio
async def test_retrieval_from_local_file_image_vectors():
    """Test embed_and_query tool with local image file query."""
    bucket_name = 'test-s3-vector-for-mcp-server'
    index_name = 'image-vector-index'
    query_input = './data/image/family-dinner.webp'
    query_type = 'image'
    dimension = 1024
    top_k = 3

    embed_and_query_request = EmbedAndQueryTextRequest(
        vectorBucketName=bucket_name,
        indexName=index_name,
        queryInput=query_input,
        topK=str(top_k),
        modelId=IMAGE_EMBEDDING_MODELS[0],
    )

    results = await embed_and_query(embed_and_query_request)
    processed_results = process_stdout_results(results)

    assert processed_results['summary']['queryType'] == query_type
    assert processed_results['summary']['index'] == index_name
    assert processed_results['summary']['queryDimensions'] == dimension
    assert processed_results['summary']['resultsFound'] == top_k
