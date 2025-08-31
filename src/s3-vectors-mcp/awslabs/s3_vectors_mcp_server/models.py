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
"""Pydantic models for the S3 Vectors MCP server."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination token container."""

    next_token: Optional[str] = Field(default=None, alias="nextToken")


class VectorBucket(BaseModel):
    """Vector bucket metadata."""

    name: str = Field(..., alias="name")


class ListVectorBucketsResponse(BaseModel):
    """Response model for list_vector_buckets."""

    buckets: List[VectorBucket] = Field(default_factory=list, alias="buckets")
    next_token: Optional[str] = Field(default=None, alias="nextToken")


class CreateVectorBucketRequest(BaseModel):
    """Request model for create_vector_bucket."""

    bucket_name: str = Field(..., alias="bucketName")
    kms_key_id: Optional[str] = Field(default=None, alias="kmsKeyId")


class GetVectorBucketRequest(BaseModel):
    """Request model for get_vector_bucket."""

    bucket_name: str = Field(..., alias="bucketName")


class ListIndexesRequest(BaseModel):
    """Request model for list_indexes."""

    bucket_name: str = Field(..., alias="bucketName")
    next_token: Optional[str] = Field(default=None, alias="nextToken")


class CreateIndexRequest(BaseModel):
    """Request model for create_index."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")
    dimensions: int = Field(..., alias="dimensions")
    similarity: str = Field(default="COSINE", alias="similarity")
    filterable_metadata: Optional[List[str]] = Field(default=None, alias="filterableMetadata")


class GetIndexRequest(BaseModel):
    """Request model for get_index."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")


class ListVectorsRequest(BaseModel):
    """Request model for list_vectors."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")
    include_data: bool = Field(default=False, alias="includeData")
    include_metadata: bool = Field(default=False, alias="includeMetadata")
    next_token: Optional[str] = Field(default=None, alias="nextToken")


class EmbedAndStoreTextRequest(BaseModel):
    """Request model for embed_and_store_text."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")
    text: str
    metadata: Optional[Dict[str, str]] = None


class EmbedAndStoreFileRequest(BaseModel):
    """Request model for embed_and_store_file."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")
    file_path: str = Field(..., alias="filePath")
    metadata: Optional[Dict[str, str]] = None


class EmbedAndStoreS3ObjectsRequest(BaseModel):
    """Request model for embed_and_store_s3_objects."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")
    s3_uri_prefix: str = Field(..., alias="s3UriPrefix")
    metadata: Optional[Dict[str, str]] = None


class EmbedAndQueryTextRequest(BaseModel):
    """Request model for embed_and_query_text."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")
    text: str
    top_k: int = Field(default=5, alias="topK")


class EmbedAndQueryFileRequest(BaseModel):
    """Request model for embed_and_query_file."""

    bucket_name: str = Field(..., alias="bucketName")
    index_name: str = Field(..., alias="indexName")
    file_path: str = Field(..., alias="filePath")
    top_k: int = Field(default=5, alias="topK")
