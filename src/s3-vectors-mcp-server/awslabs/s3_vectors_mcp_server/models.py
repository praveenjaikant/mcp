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

"""Pydantic models for the S3 Vectors MCP server.

This module defines the data models used for request and response validation
in the S3 Vectors MCP server tools.
"""

import os
import re
from awslabs.s3_vectors_mcp_server.consts import (
    AWS_S3_BUCKET_ENCRYPTION_CONFIGURATION,
    IMAGE_EMBEDDING_MODELS,
    IMAGE_FILE_EXTENSIONS,
    MODALITIES,
    OUTPUT_FORMATS,
    TEXT_EMBEDDING_MODELS,
    TEXT_FILE_EXTENSIONS,
    VALID_S3_KMS_ARN,
    VECTOR_BUCKET_ARN_PATTERN,
    VECTOR_BUCKET_NAME_PATTERN,
    VECTOR_INDEX_NAME_PATTERN,
)
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any, Dict, List, Literal, Optional


# All Helper Classes

# class MetadataConfiguration(BaseModel):
#     nonFilterableMetadataKeys: Optional[List[str]] = Field(
#         description='Non-filterable metadata keys allow you to enrich vectors with additional context during storage and retrieval.',
#         default=['S3VECTORS-EMBED-SRC-CONTENT', 'S3VECTORS-EMBED-SRC-LOCATION']
#     )


class VectorData(BaseModel):
    """Vector data - each element is of type float32."""

    float32: List[float]


class QueryVector(BaseModel):
    """Vector data - each element is of type float32."""

    float32: VectorData


class InputVector(BaseModel):
    """Input Vector data data structure."""

    key: str
    data: VectorData
    metadata: Optional[Dict[str, Any]] = None


class Pagination(BaseModel):
    """Pagination token container."""

    next_token: Optional[str] = Field(default=None, alias='nextToken')


###### S3 Vector Bucket Classes


class CreateVectorBucketRequest(BaseModel):
    """Request model for create_vector_bucket."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket to create.', pattern=VECTOR_BUCKET_NAME_PATTERN
    )

    encryptionConfiguration: Dict[str, Any] = Field(
        description=(
            'The encryption configuration for the vector bucket. '
            'By default, if you don’t specify, all new vectors in Amazon S3 vector buckets '
            'use server-side encryption with Amazon S3 managed keys (SSE-S3), specifically AES256.'
        ),
        default_factory=lambda: AWS_S3_BUCKET_ENCRYPTION_CONFIGURATION,
    )

    @model_validator(mode='before')
    def _validate_encryption(cls, values: Any) -> Dict[str, Any]:
        """Ensuring that S3 Vector Bucket encryption params are either AES256 or KMS + KMS ARN."""
        # Default to AES256 if not provided / falsy
        if not values:
            return AWS_S3_BUCKET_ENCRYPTION_CONFIGURATION

        if not isinstance(values, dict):
            raise TypeError('encryptionConfiguration must be a dict')

        # Ensure sseType is present and valid
        sse = values.get('sseType', 'AES256')
        if sse not in ('AES256', 'aws:kms'):
            raise ValueError("encryptionConfiguration.sseType must be 'AES256' or 'aws:kms'")
        values['sseType'] = sse  # normalize if missing

        # Require kmsKeyArn when aws:kms is selected
        if sse == 'aws:kms':
            if not values.get('kmsKeyArn'):
                raise ValueError(
                    "encryptionConfiguration.kmsKeyArn is required when sseType is 'aws:kms'"
                )

            if not re.match(VALID_S3_KMS_ARN, values.get('kmsKeyArn')):
                raise ValueError(
                    f'encryptionConfiguration.kmsKeyArn is required to match {VALID_S3_KMS_ARN}'
                )

        return values


class GetVectorBucketRequest(BaseModel):
    """Request model for get_vector_bucket."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket to retrieve information about.',
        pattern=VECTOR_BUCKET_NAME_PATTERN,
    )

    vectorBucketArn: Optional[str] = Field(
        description='The ARN of the vector bucket to retrieve information about.',
        pattern=VECTOR_BUCKET_ARN_PATTERN,
        default=None,
    )


class ListVectorBucketRequest(BaseModel):
    """Request model for list_vector_bucket."""

    maxResults: Optional[int] = Field(
        description='The maximum number of vector buckets to return.', default=None
    )
    nextToken: Optional[Pagination] = Field(
        description='Pagination token from a previous response, to retrieve the next page.',
        default=None,
    )
    prefix: Optional[str] = Field(
        description='Limit results to vector buckets whose names begin with this prefix.',
        default=None,
    )


###### S3 Vector Index Classes


class CreateIndexRequest(BaseModel):
    """Request model for create_index."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket to create the vector index in.',
        pattern=VECTOR_BUCKET_NAME_PATTERN,
    )

    vectorBucketArn: Optional[str] = Field(
        description='The ARN of the vector bucket to create the vector index in.',
        pattern=VECTOR_BUCKET_ARN_PATTERN,
        default=None,
    )

    indexName: str = Field(
        description='The name of the vector index to create.', pattern=VECTOR_INDEX_NAME_PATTERN
    )
    dimension: int = Field(
        description='The dimensions of the vectors to be inserted into the vector index.',
        ge=1,
        le=4096,
    )

    dataType: Optional[str] = Field(
        description='The data type of the vectors to be inserted into the vector index. Defaults to float32',
        default='float32',
    )

    distanceMetric: Optional[str] = Field(
        description='Distance metric specifies how similarity between vectors is calculated. '
        "When creating vector embeddings, choose your embedding model's recommended distance metric for more accurate results."
        'cosine – Measures the cosine of the angle between vectors. Best for normalized vectors and when direction matters more than magnitude.'
        'euclidean – Measures the straight-line distance between vectors. Best when both direction and magnitude are important.',
        default='cosine',
    )

    metadataConfiguration: Optional[Dict] = Field(
        description="The metadata configuration for the vector index. Provide a list of nonFilterableMetadataKeys. Defaults to ['S3VECTORS-EMBED-SRC-CONTENT', 'S3VECTORS-EMBED-SRC-LOCATION']",
        default={
            'nonFilterableMetadataKeys': [
                'S3VECTORS-EMBED-SRC-CONTENT',
                'S3VECTORS-EMBED-SRC-LOCATION',
            ]
        },
    )

    @field_validator('indexName')
    def check_length(cls, v: str) -> str:
        """Ensuring that index name is between 3 and 63 characters long."""
        if not (3 <= len(v) <= 63):
            raise ValueError('indexName must be between 3 and 63 characters long')
        return v


class GetIndexRequest(BaseModel):
    """Request model for get_index."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket that contains the vector index.',
        pattern=VECTOR_BUCKET_NAME_PATTERN,
    )

    indexName: str = Field(
        description='The name of the vector index.',
        pattern=VECTOR_INDEX_NAME_PATTERN,
    )

    # indexArn: Optional[str] = Field(
    #     description='The ARN of the vector index.', pattern=VECTOR_INDEX_ARN_PATTERN
    # )

    @field_validator('indexName')
    def check_length(cls, v: str) -> str:
        """Ensuring that index name is between 3 and 63 characters long."""
        if not (3 <= len(v) <= 63):
            raise ValueError('indexName must be between 3 and 63 characters long')
        return v


class ListIndexesRequest(BaseModel):
    """Request model for list_indexes."""

    vectorBucketName: str = Field(
        description=' The name of the vector bucket that contains the vector indexes.',
        pattern=VECTOR_BUCKET_NAME_PATTERN,
    )

    vectorBucketArn: Optional[str] = Field(
        description='The ARN of the vector bucket that contains the vector indexes.',
        pattern=VECTOR_BUCKET_ARN_PATTERN,
        default=None,
    )

    maxResults: Optional[int] = Field(
        description='The maximum number of items to be returned in the response.', default=None
    )

    nextToken: Optional[Pagination] = Field(
        default=None,
        description='Pagination token from a previous response, to retrieve the next page.',
    )

    prefix: Optional[str] = Field(
        default=None,
        description='Limits the response to vector indexes that begin with the specified prefix.',
    )


###### S3 Vectors Classes


class ListVectorsRequest(BaseModel):
    """Request model for list_vectors."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket.', pattern=VECTOR_BUCKET_NAME_PATTERN
    )

    indexName: str = Field(
        description='Name of the vector index', pattern=VECTOR_INDEX_NAME_PATTERN
    )

    # indexArn: Optional[str] = Field(
    #     description="ARN of the vector index",
    #     pattern=VECTOR_INDEX_ARN_PATTERN
    # )

    maxResults: Optional[int] = Field(
        description='Maximum number of vectors to return on a page (default 500 if not specified).'
    )

    nextToken: Optional[Pagination] = Field(description='Pagination token from a previous request')

    segmentCount: Optional[int] = Field(
        None,
        description=(
            'Total number of segments for parallel listing; must specify along with segmentIndex'
        ),
    )

    segmentIndex: Optional[int] = Field(
        None,
        description=('Index of the current segment (0-based); must specify with segmentCount'),
    )

    returnData: Optional[bool] = Field(
        None,
        description='If true, include vector data in the response (requires GetVectors permission)',
    )
    returnMetadata: Optional[bool] = Field(
        None,
        description='If true, include vector metadata in the response (requires GetVectors permission)',
    )

    @field_validator('indexName')
    def check_length(cls, v: str) -> str:
        """Ensuring that index name is between 3 and 63 characters long."""
        if not (3 <= len(v) <= 63):
            raise ValueError('indexName must be between 3 and 63 characters long')
        return v


class EmbedAndStoreTextRequest(BaseModel):
    """Request model for s3vectors-embed put with --text-value requests."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket.', pattern=VECTOR_BUCKET_NAME_PATTERN
    )

    indexName: str = Field(
        description='Name of the vector index', pattern=VECTOR_INDEX_NAME_PATTERN
    )

    modelId: Literal[tuple(TEXT_EMBEDDING_MODELS)] = Field(
        description='Model ID to be used for embedding', default=TEXT_EMBEDDING_MODELS[0]
    )

    textValue: str = Field(description='input text to be validated')

    @field_validator('indexName')
    def check_length(cls, v: str) -> str:
        """Ensuring that index name is between 3 and 63 characters long."""
        if not (3 <= len(v) <= 63):
            raise ValueError('indexName must be between 3 and 63 characters long')
        return v


class EmbedAndStoreFileRequest(BaseModel):
    """Request model for s3vectors-embed put with --text requests."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket.', pattern=VECTOR_BUCKET_NAME_PATTERN
    )

    indexName: str = Field(
        description='Name of the vector index', pattern=VECTOR_INDEX_NAME_PATTERN
    )

    modelId: Literal[tuple(TEXT_EMBEDDING_MODELS + IMAGE_EMBEDDING_MODELS)] = Field(
        description='Model ID to be used for embedding', default=TEXT_EMBEDDING_MODELS[0]
    )

    file: str = Field(description='local file that needs to get embedded and stored')

    modality: Literal[tuple(MODALITIES)] = Field(
        description='the modality of the file(s)', default=MODALITIES[0]
    )

    @field_validator('indexName')
    def check_length(cls, v: str) -> str:
        """Ensuring that index name is between 3 and 63 characters long."""
        if not (3 <= len(v) <= 63):
            raise ValueError('indexName must be between 3 and 63 characters long')
        return v

    @model_validator(mode='before')
    def validate_model_for_file_type(cls, values):
        """Ensuring that files being indexed are in-line with embedding model being used."""
        file_path = values.get('file')
        model_id = values.get('modelId')

        if not file_path or not model_id:
            return values  # Let Pydantic handle missing fields

        ext = os.path.splitext(file_path)[1].lower()

        if ext in TEXT_FILE_EXTENSIONS:
            if model_id not in TEXT_EMBEDDING_MODELS:
                raise ValueError(
                    f"Model ID '{model_id}' is not valid for text file type '{ext}'. Must be one of {TEXT_EMBEDDING_MODELS}."
                )
        elif ext in IMAGE_FILE_EXTENSIONS:
            if model_id not in IMAGE_EMBEDDING_MODELS:
                raise ValueError(
                    f"Model ID '{model_id}' is not valid for image file type '{ext}'. Must be one of {IMAGE_EMBEDDING_MODELS}."
                )
        else:
            raise ValueError(
                f"Unsupported file extension '{ext}'. Supported text types: {TEXT_FILE_EXTENSIONS}. Image types: {IMAGE_FILE_EXTENSIONS}."
            )

        return values


class EmbedAndStoreS3ObjectsRequest(BaseModel):
    """Request model for s3vectors-embed put with --text requests with S3 URIs."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket.', pattern=VECTOR_BUCKET_NAME_PATTERN
    )

    indexName: str = Field(
        description='Name of the vector index', pattern=VECTOR_INDEX_NAME_PATTERN
    )

    modelId: Literal[tuple(TEXT_EMBEDDING_MODELS + IMAGE_EMBEDDING_MODELS)] = Field(
        description='Model ID to be used for embedding', default=TEXT_EMBEDDING_MODELS[0]
    )

    s3_path: str = Field(description='S3 file that needs to get embedded and stored')

    modality: Literal[tuple(MODALITIES)] = Field(description='the modality of the file(s)')

    @field_validator('indexName')
    def check_length(cls, v: str) -> str:
        """Ensuring that index name is between 3 and 63 characters long."""
        if not (3 <= len(v) <= 63):
            raise ValueError('indexName must be between 3 and 63 characters long')
        return v

    # @model_validator(mode='before')
    # def validate_model_for_file_type(cls, values):
    #     s3_path = values.get('s3_path')
    #     model_id = values.get('modelId')
    #
    #     if not s3_path or not model_id:
    #         return values  # Let Pydantic handle missing fields
    #
    #     ext = os.path.splitext(s3_path)[1].lower()
    #
    #     if ext in TEXT_FILE_EXTENSIONS:
    #         if model_id not in TEXT_EMBEDDING_MODELS:
    #             raise ValueError(
    #                 f"Model ID '{model_id}' is not valid for text file type '{ext}'. Must be one of {TEXT_EMBEDDING_MODELS}.")
    #     elif ext in IMAGE_FILE_EXTENSIONS:
    #         if model_id not in IMAGE_EMBEDDING_MODELS:
    #             raise ValueError(
    #                 f"Model ID '{model_id}' is not valid for image file type '{ext}'. Must be one of {IMAGE_EMBEDDING_MODELS}.")
    #     else:
    #         raise ValueError(
    #             f"Unsupported file extension '{ext}'. Supported text types: {TEXT_FILE_EXTENSIONS}. Image types: {IMAGE_FILE_EXTENSIONS}.")
    #
    #     return values


class EmbedAndQueryTextRequest(BaseModel):
    """Request model for s3vectors-embed query requests."""

    vectorBucketName: str = Field(
        description='The name of the vector bucket that contains the vector index.',
        pattern=VECTOR_BUCKET_NAME_PATTERN,
    )

    indexName: str = Field(
        description='The name of the vector index that you want to query.',
        pattern=VECTOR_INDEX_NAME_PATTERN,
    )

    modelId: str = Field(
        description='Model ID to be used for embedding', default=TEXT_EMBEDDING_MODELS[0]
    )

    queryInput: str = Field(description='The query string.')

    # Optional args

    topK: Optional[str] = Field(
        description='The number of results to return for each query.', default='5'
    )

    filter: Optional[Dict[str, Any]] = Field(
        default=None, description='Metadata filter to apply during the query.'
    )

    returnMetadata: Optional[bool] = Field(
        default=False,
        description='Indicates whether to include metadata in the response. The default value is false.',
    )

    returnDistance: Optional[bool] = Field(
        default=False,
        description='Indicates whether to include metadata in the response. The default value is false.',
    )

    output: Optional[Literal[tuple(OUTPUT_FORMATS)]] = Field(
        description='Output format, json or table', default=OUTPUT_FORMATS[0]
    )

    @field_validator('indexName')
    def check_length(cls, v: str) -> str:
        """Ensuring that index name is between 3 and 63 characters long."""
        if not (3 <= len(v) <= 63):
            raise ValueError('indexName must be between 3 and 63 characters long')
        return v
