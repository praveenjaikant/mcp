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

"""Constants for the S3 Vectors MCP server.

This module defines constants used throughout the Finch MCP server.
"""

# Server name
SERVER_NAME = 's3vectors_mcp_server'

# Bucket name pattern
VECTOR_BUCKET_NAME_PATTERN = r'[a-z0-9][a-z0-9-]{1,61}[a-z0-9]'
"""
Regex pattern for validating S3 bucket names.
Valid bucket names must:
- Be between 3 and 63 characters long
- Start and end with a letter or number
- Contain only lowercase letters, numbers, and hyphens
- Not contain consecutive hyphens
"""

VECTOR_BUCKET_ARN_PATTERN = r'^arn:aws:s3vector:[a-z0-9-]+:\d{12}:bucket/[a-zA-Z0-9.\-_]{3,63}$'
"""
Regex pattern for validating S3 bucket ARNs.
Format: arn:aws[-a-z0-9]*:[a-z0-9]+:[-a-z0-9]*:[0-9]{12}:bucket/[bucket-name]
Example: arn:aws:s3:::my-bucket
"""

# Vector Index ARN Pattern
VECTOR_INDEX_ARN_PATTERN = r'^arn:aws:s3vector:[a-z0-9-]+:\d{12}:bucket/[a-z0-9.-]{3,63}/index/(?=.{3,63}$)[a-z0-9](?:[a-z0-9.-]*[a-z0-9])$'

# Vector Index Name Pattern
VECTOR_INDEX_NAME_PATTERN = '^[a-z0-9](?:[a-z0-9.-]{1,61}[a-z0-9])?$'

# AWS region pattern
REGION_PATTERN = r'^[a-zA-Z0-9][a-zA-Z0-9-_]*$'

# AWS S3 Vector Buckets Supported Server-Side Encryption Types
VALID_S3_SSE_TYPES = ['AES256', 'aws:kms']

# AWS S3 Vector Bucket Default encryption configuration
AWS_S3_BUCKET_ENCRYPTION_CONFIGURATION = {'sseType': 'AES256'}

# AWS S3 Vector Bucket KMS ARN Regex Pattern

VALID_S3_KMS_ARN = r'^arn:aws:kms:[a-z0-9-]+:\d{12}:key/[0-9a-fA-F-]{36}$'

# AWS S3 Vector Index Supported Distance Metrics
VALID_DISTANCE_METRICS = ['euclidean', 'cosine']

# AWS Bedrock Compatible Models from s3vectors-embed-cli

TEXT_EMBEDDING_MODELS = [
    'amazon.titan-embed-text-v2:0',
    'amazon.titan-embed-text-v1',
    'cohere.embed-english-v3',
    'cohere.embed-multilingual-v3',
]

IMAGE_EMBEDDING_MODELS = ['amazon.titan-embed-image-v1']

# text and image file extensions
TEXT_FILE_EXTENSIONS = {'.txt', '.pdf', '.doc', '.docx', '.md'}
IMAGE_FILE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

# allowed modalities
MODALITIES = ['text', 'image']

# allowed output formats
OUTPUT_FORMATS = ['json', 'table']

# escape characters for removal
ESCAPE_CHARS = r'[\x00-\x1f\x7f]'

# max bytes allowed in non-filterable metadata config
MAX_LENGTH = 2048
