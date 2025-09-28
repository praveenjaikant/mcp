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

"""Helper functions for the S3 Vectors MCP server."""

import boto3
import os
from awslabs.s3_vectors_mcp_server.models import EmbedAndQueryTextRequest
from loguru import logger


# Configure Loguru logging
# logger.remove()
# logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

# Global client cache
_s3_vectors_client = None
_s3_vectors_global_config = []
_s3_vectors_query_optional_config = []


def get_s3_vectors_client():
    """Get S3 Vectors client with proper session management and caching.

    Returns:
        boto3.client: Configured S3 Vectors client (cached after first call)
    """
    global _s3_vectors_client

    if _s3_vectors_client is None:
        try:
            # Read environment variables dynamically
            aws_region = os.environ.get('AWS_REGION', 'us-east-1')
            aws_profile = os.environ.get('AWS_PROFILE')

            if aws_profile:
                _s3_vectors_client = boto3.Session(
                    profile_name=aws_profile, region_name=aws_region
                ).client('s3vectors')
            else:
                _s3_vectors_client = boto3.Session(region_name=aws_region).client('s3vectors')
        except Exception as e:
            logger.error(f'Error creating S3 Vectors client: {str(e)}')
            raise

    return _s3_vectors_client


def get_s3vectors_cli_global_config():
    """Get s3-vectors-embed-cli global config based on environment variables.

    Returns:
        list: containing elements pertaining to global options for s3vectors-embed-cli
    """
    global _s3_vectors_global_config

    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    aws_profile = os.environ.get('AWS_PROFILE')
    debug_flag = os.environ.get('DEBUG_FLAG', 0)

    if debug_flag != 0:
        _s3_vectors_global_config += ['--debug']

    if aws_profile:
        _s3_vectors_global_config += ['--profile', aws_profile]

    if aws_region:
        _s3_vectors_global_config += ['--region', aws_region]

    return _s3_vectors_global_config


def get_s3vectors_query_optional_config(embed_and_query_text_request: EmbedAndQueryTextRequest):
    """Get optional configuration for ```s3vectors-embed query``` based on incoming request.

    Returns:
        list: containing argument name and value for optional args to be used in embed_and_query_text_request.

    """
    global _s3_vectors_query_optional_config

    if embed_and_query_text_request.topK:
        _s3_vectors_query_optional_config += ['--k', embed_and_query_text_request.topK]

    if embed_and_query_text_request.filter:
        _s3_vectors_query_optional_config += ['--filter', embed_and_query_text_request.filter]

    if embed_and_query_text_request.returnMetadata:
        _s3_vectors_query_optional_config += ['--return-metadata']

    if embed_and_query_text_request.returnDistance:
        _s3_vectors_query_optional_config += ['--return-distance']

    if embed_and_query_text_request.output:
        _s3_vectors_query_optional_config += ['--output', embed_and_query_text_request.output]

    return _s3_vectors_query_optional_config
