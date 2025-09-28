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

"""Tests for the MCP tools for S3 Vector Bucket operations."""

import pytest
from awslabs.s3_vectors_mcp_server.consts import AWS_S3_BUCKET_ENCRYPTION_CONFIGURATION
from awslabs.s3_vectors_mcp_server.models import (
    CreateVectorBucketRequest,
    GetVectorBucketRequest,
    ListVectorBucketRequest,
)
from awslabs.s3_vectors_mcp_server.server import (
    create_vector_bucket,
    get_vector_bucket,
    list_vector_buckets,
)


# s3-vectors-mcp-server-vector-bucket


# Tests
@pytest.mark.asyncio
async def test_create_vector_bucket():
    """Test create_vector_bucket tool."""
    bucket_name = 'test-final-vector-bucket'

    create_vector_bucket_request = CreateVectorBucketRequest(vectorBucketName=bucket_name)

    results = await create_vector_bucket(create_vector_bucket_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200


@pytest.mark.asyncio
async def test_get_vector_bucket():
    """Test get_vector_bucket tool."""
    bucket_name = 'test-final-vector-bucket'

    get_vector_bucket_request = GetVectorBucketRequest(vectorBucketName=bucket_name)

    results = await get_vector_bucket(get_vector_bucket_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200
    assert results['vectorBucket']['vectorBucketName'] == bucket_name
    assert (
        results['vectorBucket']['encryptionConfiguration']
        == AWS_S3_BUCKET_ENCRYPTION_CONFIGURATION
    )


@pytest.mark.asyncio
async def test_list_vector_buckets():
    """Test get_vector_buckets tool."""
    list_vector_buckets_request = ListVectorBucketRequest()

    results = await list_vector_buckets(list_vector_buckets_request)

    assert results['ResponseMetadata']['HTTPStatusCode'] == 200
    assert (len(results['vectorBuckets'])) > 0  # at least one vector bucket exists
    assert (
        results['vectorBuckets'][0]['vectorBucketName'] == 'my-new-s3-vector-bucket'
    )  # verify bucket name
