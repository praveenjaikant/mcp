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

"""Tests for the MCP tools for S3 Vector Index operations."""

import pytest
from awslabs.s3_vectors_mcp_server.models import (
    CreateIndexRequest,
    GetIndexRequest,
    ListIndexesRequest,
)
from awslabs.s3_vectors_mcp_server.server import create_index, get_index, list_indexes


# Tests
@pytest.mark.asyncio
async def test_create_index():
    """Test create_index resource."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'text-vector-index'
    dimension = 1024

    create_index_request = CreateIndexRequest(
        vectorBucketName=bucket_name, indexName=index_name, dimension=dimension
    )

    results = await create_index(create_index_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200


@pytest.mark.asyncio
async def test_get_index():
    """Test get_index resource."""
    bucket_name = 'test-final-vector-bucket'
    index_name = 'text-vector-index'
    data_type = 'float32'
    dimension = 1024
    distance_metric = 'cosine'

    get_index_request = GetIndexRequest(vectorBucketName=bucket_name, indexName=index_name)

    results = await get_index(get_index_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200
    assert results['index']['vectorBucketName'] == bucket_name
    assert results['index']['indexName'] == index_name
    assert results['index']['dataType'] == data_type
    assert results['index']['dimension'] == dimension
    assert results['index']['distanceMetric'] == distance_metric


@pytest.mark.asyncio
async def test_list_indexes():
    """Test list_indexes resource."""
    bucket_name = 'test-final-vector-bucket'

    list_indexes_request = ListIndexesRequest(
        vectorBucketName=bucket_name,
    )

    results = await list_indexes(list_indexes_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200
    assert len(results['indexes']) >= 1  # at least one index exists
    assert (
        results['indexes'][0]['vectorBucketName'] == bucket_name
    )  # index exists under the bucket
