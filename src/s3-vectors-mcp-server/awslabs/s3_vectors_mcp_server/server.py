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

"""S3 Vectors MCP Server main module.

This module provides the MCP server implementation for S3 Vectors operations.

Note: The tools provided by this MCP server are intended for development and prototyping
purposes only and are not meant for production use cases.
"""

import subprocess
from awslabs.s3_vectors_mcp_server.consts import SERVER_NAME
from awslabs.s3_vectors_mcp_server.helpers import (
    get_s3_vectors_client,
    get_s3vectors_cli_global_config,
    get_s3vectors_query_optional_config,
)
from awslabs.s3_vectors_mcp_server.models import (
    CreateIndexRequest,
    CreateVectorBucketRequest,
    EmbedAndQueryTextRequest,
    EmbedAndStoreFileRequest,
    EmbedAndStoreS3ObjectsRequest,
    EmbedAndStoreTextRequest,
    GetIndexRequest,
    GetVectorBucketRequest,
    ListIndexesRequest,
    ListVectorBucketRequest,
    ListVectorsRequest,
)
from loguru import logger
from mcp.server.fastmcp import FastMCP


# Initialize S3 Vectors Client
s3v = get_s3_vectors_client()

# Initialize s3-vectors-embed-cli global config
S3_VECTORS_GLOBAL_CONFIG = get_s3vectors_cli_global_config()

# Initialize the MCP server
mcp = FastMCP(SERVER_NAME)
enable_aws_resource_write = False

###### S3 Vector Bucket Tools


@mcp.tool()
async def create_vector_bucket(create_vector_bucket_request: CreateVectorBucketRequest):
    """Create an S3 Vectors Bucket.

    Note: You must have the s3vectors:CreateVectorBucket permission to use this operation.

    Returns:
        Result: {}

    """
    logger.info('tool-name: create_vector_bucket')

    return s3v.create_vector_bucket(**create_vector_bucket_request.dict(exclude_none=True))


@mcp.tool()
async def list_vector_buckets(list_vector_bucket_request: ListVectorBucketRequest):
    """Returns a list of all the vector buckets that are owned by the authenticated sender of the request.

    Note: You must have the s3vectors:ListVectorBucket permission to use this operation.

    Returns:
        Result:
            {
                'nextToken': 'string',
                'vectorBuckets': [
                    {
                        'vectorBucketName': 'string',
                        'vectorBucketArn': 'string',
                        'creationTime': datetime(2015, 1, 1)
                    },
                ]
            }


    """
    logger.info('tool-name: list_vector_buckets')

    return s3v.list_vector_buckets(**list_vector_bucket_request.dict(exclude_none=True))


@mcp.tool()
async def get_vector_bucket(get_vector_bucket_request: GetVectorBucketRequest):
    """Returns vector bucket attributes. To specify the bucket, you must use either the vector bucket name or the vector bucket Amazon Resource Name (ARN). Note: You must have the s3vectors:GetVectorBucket permission to use this operation.

    Returns:
        Result:
            {
                'vectorBucket': {
                    'vectorBucketName': 'string',
                    'vectorBucketArn': 'string',
                    'creationTime': datetime(2015, 1, 1),
                    'encryptionConfiguration': {
                        'sseType': 'AES256'|'aws:kms',
                        'kmsKeyArn': 'string'
                    }
                }
            }
    """
    logger.info('tool-name: get_vector_bucket')

    return s3v.get_vector_bucket(**get_vector_bucket_request.dict(exclude_none=True))


###### S3 Vector Index Tools
@mcp.tool()
async def create_index(create_index_request: CreateIndexRequest):
    """Creates a vector index within a vector bucket. To specify the vector bucket, you must use either the vector bucket name or the vector bucket Amazon Resource Name (ARN). Note: You must have the s3vectors:CreateIndex permission to use this operation.

    Returns:
        Result:
            {}
    """
    logger.info('tool-name: create_index')

    return s3v.create_index(**create_index_request.dict(exclude_none=True))


@mcp.tool()
async def get_index(get_index_request: GetIndexRequest):
    """Returns vector index attributes. To specify the vector index, you can either use both the vector bucket name and the vector index name, or use the vector index Amazon Resource Name (ARN). Note: You must have the s3vectors:GetIndex permission to use this operation.

    Returns:
        Result:
            {
                'index': {
                    'vectorBucketName': 'string',
                    'indexName': 'string',
                    'indexArn': 'string',
                    'creationTime': datetime(2015, 1, 1),
                    'dataType': 'float32',
                    'dimension': 123,
                    'distanceMetric': 'euclidean'|'cosine',
                    'metadataConfiguration': {
                        'nonFilterableMetadataKeys': [
                            'string',
                        ]
                    }
                }
            }
    """
    logger.info('tool-name: get_index')

    return s3v.get_index(**get_index_request.dict(exclude_none=True))


@mcp.tool()
async def list_indexes(list_indexes_request: ListIndexesRequest):
    """Returns vector index attributes. To specify the vector index, you can either use both the vector bucket name and the vector index name, or use the vector index Amazon Resource Name (ARN). Note: You must have the s3vectors:GetIndex permission to use this operation.

    Returns:
        Result:
            {
                'index': {
                    'vectorBucketName': 'string',
                    'indexName': 'string',
                    'indexArn': 'string',
                    'creationTime': datetime(2015, 1, 1),
                    'dataType': 'float32',
                    'dimension': 123,
                    'distanceMetric': 'euclidean'|'cosine',
                    'metadataConfiguration': {
                        'nonFilterableMetadataKeys': [
                            'string',
                        ]
                    }
                }
            }
    """
    logger.info('tool-name: list_indexes')

    return s3v.list_indexes(**list_indexes_request.dict(exclude_none=True))


###### S3 Vector Operations Tools


@mcp.tool()
async def list_vectors(list_vectors_request: ListVectorsRequest):
    """List vectors in the specified vector index. To specify the vector index, you can either use both the vector bucket name and the vector index name, or use the vector index Amazon Resource Name (ARN).

    Note: You must have the s3vectors:ListVectors permission to use this operation. Additional permissions are required based on the request parameters you specify:

    * With only s3vectors:ListVectors permission, you can list vector keys when returnData and returnMetadata are both set to false or not specified.
    * If you set returnData or returnMetadata to true, you must have both s3vectors:ListVectors and s3vectors:GetVectors permissions.
    The request fails with a 403 Forbidden error if you request vector data or metadata without the s3vectors:GetVectors permission.

    Returns:
        Result:
            {
                'nextToken': 'string',
                'vectors': [
                    {
                        'key': 'string',
                        'data': {
                            'float32': [
                                    ...,
                            ]
                        },
                        'metadata': {...}|[...]|123|123.4|'string'|True|None
                     },
                ]
            }
    """
    logger.info('tool-name: list_vectors')

    return s3v.list_vectors(**list_vectors_request.dict(exclude_none=True))


@mcp.tool()
async def embed_and_store_text(embed_and_store_text_request: EmbedAndStoreTextRequest):
    """Generate embeddings from text input using Bedrock models using s3vectors-embed-cli.

    Example usage:
    s3vectors-embed put \
    --vector-bucket-name my-bucket \
    --index-name my-index \
    --model-id amazon.titan-embed-text-v2:0 \
    --text-value "Hello, world!".
    """
    args = [
        '--vector-bucket-name',
        embed_and_store_text_request.vectorBucketName,
        '--index-name',
        embed_and_store_text_request.indexName,
        '--model-id',
        embed_and_store_text_request.modelId,
        '--text-value',
        embed_and_store_text_request.textValue,
    ]

    command = ['s3vectors-embed'] + S3_VECTORS_GLOBAL_CONFIG + ['put'] + args

    response = subprocess.run(command, capture_output=True)

    return eval(response.stdout)


@mcp.tool()
async def embed_and_store_file(embed_and_store_file_request: EmbedAndStoreFileRequest):
    """Generate embeddings from an attached local file or multiple local files under a directory with wildcards using Bedrock models using s3vectors-embed-cli.

    Example usages:

    1. Process local text files

    s3vectors-embed [S3_VECTORS_GLOBAL_CONFIG] put \
    --vector-bucket-name my-bucket \
    --index-name my-index \
    --model-id amazon.titan-embed-text-v2:0 \
    --text "./documents/sample.txt"

    2. Process image files using a local file path
    s3vectors-embed [S3_VECTORS_GLOBAL_CONFIG] put \
    --vector-bucket-name my-bucket \
    --index-name my-index \
    --model-id amazon.titan-embed-image-v1 \
    --image "./images/photo.jpg"

    3. Process files from a local file path using wildcard characters
    s3vectors-embed [S3_VECTORS_GLOBAL_CONFIG] put \
    --vector-bucket-name my-bucket \
    --index-name my-index \
    --model-id amazon.titan-embed-text-v2:0 \
    --text "./documents/*.txt"
    """
    args = [
        '--vector-bucket-name',
        embed_and_store_file_request.vectorBucketName,
        '--index-name',
        embed_and_store_file_request.indexName,
        '--model-id',
        embed_and_store_file_request.modelId,
        f'--{embed_and_store_file_request.modality}',
        f'{embed_and_store_file_request.file}',
    ]

    command = ['s3vectors-embed'] + S3_VECTORS_GLOBAL_CONFIG + ['put'] + args

    response = subprocess.run(command, capture_output=True)

    try:
        return eval(response.stdout)  # works well for single-file and raw text value embedding
    except SyntaxError:
        return str(response.stdout.decode())  # works well for wildcard embedding tasks


@mcp.tool()
async def embed_and_store_s3_objects(
    embed_and_store_s3_objects_request: EmbedAndStoreS3ObjectsRequest,
):
    """Generate embeddings from an S3 file or multiple S3 files under a directory with wildcards using Bedrock models using s3vectors-embed-cli.

    Example usages:

    1. Process files from an S3 general purpose bucket using wildcard characters
    s3vectors-embed [S3_VECTORS_GLOBAL_CONFIG] put \
    --vector-bucket-name my-bucket \
    --index-name my-index \
    --model-id amazon.titan-embed-text-v2:0 \
    --text "s3://bucket/path/*"

    2. Process individual file from an S3 general purpose bucket
    s3vectors-embed [S3_VECTORS_GLOBAL_CONFIG] put \
    --vector-bucket-name my-bucket \
    --index-name my-index \
    --model-id amazon.titan-embed-text-v2:0 \
    --text "s3://my-bucket/sample.txt"
    """
    args = [
        '--vector-bucket-name',
        embed_and_store_s3_objects_request.vectorBucketName,
        '--index-name',
        embed_and_store_s3_objects_request.indexName,
        '--model-id',
        embed_and_store_s3_objects_request.modelId,
        f'--{embed_and_store_s3_objects_request.modality}',
        embed_and_store_s3_objects_request.s3_path,
    ]

    command = ['s3vectors-embed'] + S3_VECTORS_GLOBAL_CONFIG + ['put'] + args

    response = subprocess.run(command, capture_output=True)

    return response.stdout.decode()


###### S3 Vector Query Tools


@mcp.tool()
async def embed_and_query(embed_and_query_text_request: EmbedAndQueryTextRequest):
    """Generate similar results from vectors stored under an S3 vector index using Bedrock models using s3vectors-embed-cli.

    Example usages:

    1. Query with raw text
    s3vectors-embed [S3_VECTORS_GLOBAL_CONFIG] query \
        --vector-bucket-name my-bucket \
        --index-name my-index \
        --model-id amazon.titan-embed-text-v2:0 \
        --query-input "query text" \
        --k 10

    2. Query with local file as input
    s3vectors-embed [S3_VECTORS_GLOBAL_CONFIG] query \
        --vector-bucket-name my-bucket \
        --index-name my-index \
        --model-id amazon.titan-embed-text-v2:0 \
        --query-input "./query.txt" \
        --k 5
    --output table

    3. Query (image-to-image search) using S3 object as input
    s3vectors-embed query \
        --vector-bucket-name my-bucket \
        --index-name my-index \
        --model-id amazon.titan-embed-text-v2:0 \
        --query-input "s3://my-bucket/image.jpeg" \
        --k 3
    """
    s3_vectors_query_optional_config = get_s3vectors_query_optional_config(
        embed_and_query_text_request
    )

    args = [
        '--vector-bucket-name',
        embed_and_query_text_request.vectorBucketName,
        '--index-name',
        embed_and_query_text_request.indexName,
        '--model-id',
        embed_and_query_text_request.modelId,
        '--query-input',
        embed_and_query_text_request.queryInput,
    ]

    response = subprocess.run(
        ['s3vectors-embed']
        + S3_VECTORS_GLOBAL_CONFIG
        + ['query']
        + args
        + s3_vectors_query_optional_config,
        capture_output=True,
    )

    return response.stdout.decode()


def main():
    """Run the S3 Vectors MCP server."""
    logger.info('Starting S3 Vectors MCP server.')

    mcp.run(transport='stdio')


if __name__ == '__main__':  # pragma: no cover
    # parser = argparse.ArgumentParser(description='Run the S3 Vectors MCP server')
    #
    # parser.add_argument(
    #     '--profile',
    #     help='AWS profile to be used when connecting to AWS services',
    # )
    #
    # parser.add_argument(
    #     '--region',
    #     help='AWS region to be used when connecting to AWS services',
    # )
    #
    # parser.add_argument(
    #     '--debug',
    #     action='store_true',
    #     help='Enable debug mode with detailed logging for troubleshooting',
    # )
    #
    # args = parser.parse_args()
    #
    # # Set disable file logging from command line if provided
    # if args.debug:
    #     os.environ['DEBUG_FLAG'] = 'true'
    #
    # if args.profile:
    #     os.environ['AWS_PROFILE'] = args.profile
    #
    # if args.region:
    #     os.environ['AWS_REGION'] = args.region

    # Run MCP Server
    main()

    # AWS_REGION, AWS_PROFILE, DEBUG_FLAG, FASTMCP_LOG_LEVEL
