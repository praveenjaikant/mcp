# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the MCP tools that use the s3vectors-embed-cli command."""

import pytest
from awslabs.s3_vectors_mcp_server.consts import IMAGE_EMBEDDING_MODELS
from awslabs.s3_vectors_mcp_server.models import EmbedAndStoreFileRequest, EmbedAndStoreTextRequest
from awslabs.s3_vectors_mcp_server.server import (
    embed_and_store_file,
    embed_and_store_text,
)
from tests.helpers import process_stdout_results


# Process raw text
# Process single local text files
# Process files from a local file path using wildcard characters
# Process single text file in S3
# Process files from an S3 directory path using wildcard characters
# Process --image + --text-value
#
# Process


# Resource Tests
@pytest.mark.asyncio
async def test_embed_and_store_text():
    """Test embed_and_store_text resource."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'text-vector-index'
    text_value = 'hello world'
    content_type = 'text'
    dimension = 1024

    embed_and_store_text_request = EmbedAndStoreTextRequest(
        vectorBucketName=bucket_name, indexName=index_name, textValue=text_value
    )

    results = await embed_and_store_text(embed_and_store_text_request)

    assert results['bucket'] == bucket_name
    assert results['index'] == index_name
    assert results['contentType'] == content_type
    assert results['embeddingDimensions'] == dimension


@pytest.mark.asyncio
async def test_embed_and_store_file():
    """Test test_embed_and_store_file resource."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'text-vector-index'
    file = './tests/data/text/TEST.md'
    content_type = 'text'
    dimension = 1024

    test_embed_and_store_file_request = EmbedAndStoreFileRequest(
        vectorBucketName=bucket_name, indexName=index_name, file=file
    )

    results = await embed_and_store_file(test_embed_and_store_file_request)

    assert results['bucket'] == bucket_name
    assert results['index'] == index_name
    assert results['contentType'] == content_type
    assert results['embeddingDimensions'] == dimension


@pytest.mark.asyncio
async def test_embed_and_store_file_with_wildcard():
    """Test test_embed_and_store_file resource."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'text-vector-index'
    file = './tests/data/text/*.txt'

    test_embed_and_store_file_request = EmbedAndStoreFileRequest(
        vectorBucketName=bucket_name, indexName=index_name, file=file
    )

    results = await embed_and_store_file(test_embed_and_store_file_request)
    processed_results = process_stdout_results(results)

    assert processed_results['status'] == 'success'
    assert processed_results['pattern'] == file
    assert processed_results['bucket'] == bucket_name
    assert processed_results['index'] == index_name
    assert len(processed_results['Keys']) == 3


@pytest.mark.asyncio
async def test_embed_and_store_image_file():
    """Test embed_and_store_file tool with single local .png file."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'image-vector-index'
    file = './tests/data/image/hey.png'

    model_id = IMAGE_EMBEDDING_MODELS[0]
    content_type = 'image'
    dimension = 1024

    test_embed_and_store_file_request = EmbedAndStoreFileRequest(
        vectorBucketName=bucket_name,
        indexName=index_name,
        modality=content_type,
        modelId=model_id,
        file=file,
    )

    results = await embed_and_store_file(test_embed_and_store_file_request)

    assert results['bucket'] == bucket_name
    assert results['index'] == index_name
    assert results['model'] == model_id
    assert results['contentType'] == content_type
    assert results['embeddingDimensions'] == dimension


@pytest.mark.asyncio
async def test_embed_and_store_image_files_with_wildcard():
    """Test embed_and_store_file tool with local *.webp files in a local directory."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'image-vector-index'
    file = './tests/data/image/*.webp'

    model_id = IMAGE_EMBEDDING_MODELS[0]
    content_type = 'image'

    test_embed_and_store_file_request = EmbedAndStoreFileRequest(
        vectorBucketName=bucket_name,
        indexName=index_name,
        modality=content_type,
        modelId=model_id,
        file=file,
    )

    results = await embed_and_store_file(test_embed_and_store_file_request)
    processed_results = process_stdout_results(results)

    assert processed_results['status'] == 'success'
    assert processed_results['pattern'] == file
    assert processed_results['bucket'] == bucket_name
    assert processed_results['index'] == index_name
    assert len(processed_results['Keys']) == 2


@pytest.mark.asyncio
async def test_embed_and_store_s3_file():
    """Test embed_and_store_file tool with .md file stored in an S3 directory."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'text-vector-index'
    file = 's3://s3-bucket-for-mcp-server-test/text/README.md'
    content_type = 'text'
    dimension = 1024

    test_embed_and_store_file_request = EmbedAndStoreFileRequest(
        vectorBucketName=bucket_name, indexName=index_name, file=file
    )

    results = await embed_and_store_file(test_embed_and_store_file_request)

    assert results['bucket'] == bucket_name
    assert results['index'] == index_name
    assert results['contentType'] == content_type
    assert results['embeddingDimensions'] == dimension


@pytest.mark.asyncio
async def test_embed_and_store_s3_files_with_wildcard():
    """Test embed_and_store_file tool with wildcard pattern for files stored in an S3 directory."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'text-vector-index'
    file = 's3://s3-bucket-for-mcp-server-test/text/*'

    test_embed_and_store_file_request = EmbedAndStoreFileRequest(
        vectorBucketName=bucket_name, indexName=index_name, file=file
    )

    results = await embed_and_store_file(test_embed_and_store_file_request)
    processed_results = process_stdout_results(results)

    assert processed_results['status'] == 'success'
    assert processed_results['pattern'] == file
    assert processed_results['bucket'] == bucket_name
    assert processed_results['index'] == index_name
    assert len(processed_results['Keys']) == 3
