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
"""MCP server exposing AWS S3 Vectors tools."""

from __future__ import annotations

import importlib
from typing import Any, Dict, Optional

try:
    from mcp.server.fastmcp import FastMCP, Context
except Exception:  # pragma: no cover - optional dependency
    class _StubMCP:
        """Fallback MCP class when fastmcp is unavailable."""

        def tool(self, *_args: Any, **_kwargs: Any):  # noqa: D401 - simple passthrough
            def decorator(func):
                return func

            return decorator

        def run(self) -> None:  # pragma: no cover - runtime only
            raise RuntimeError("fastmcp is required to run the server")

    FastMCP = _StubMCP  # type: ignore[assignment]
    Context = Any  # type: ignore[assignment]

from .consts import DEFAULT_REGION
from . import __version__

INSTRUCTIONS = """Interact with the AWS S3 Vectors service."""

mcp = FastMCP("awslabs-s3-vectors-mcp-server", instructions=INSTRUCTIONS)


def _client(region: Optional[str] = None):
    """Return an S3 Vectors boto3 client."""
    boto3 = importlib.import_module("boto3")  # type: ignore[import]
    return boto3.client("s3vectors", region_name=region or DEFAULT_REGION)


@mcp.tool()
def list_vector_buckets(ctx: Context, next_token: Optional[str] = None) -> Dict[str, Any]:
    """List vector buckets with optional pagination."""
    client = _client()
    params: Dict[str, Any] = {}
    if next_token:
        params["nextToken"] = next_token
    return client.list_vector_buckets(**params)


@mcp.tool()
def create_vector_bucket(ctx: Context, bucket_name: str, kms_key_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new vector bucket."""
    client = _client()
    params: Dict[str, Any] = {"bucketName": bucket_name}
    if kms_key_id:
        params["kmsKeyId"] = kms_key_id
    return client.create_vector_bucket(**params)


@mcp.tool()
def get_vector_bucket(ctx: Context, bucket_name: str) -> Dict[str, Any]:
    """Retrieve vector bucket metadata."""
    client = _client()
    return client.get_vector_bucket(bucketName=bucket_name)


@mcp.tool()
def list_indexes(ctx: Context, bucket_name: str, next_token: Optional[str] = None) -> Dict[str, Any]:
    """List indexes for a given bucket."""
    client = _client()
    params: Dict[str, Any] = {"bucketName": bucket_name}
    if next_token:
        params["nextToken"] = next_token
    return client.list_indexes(**params)


@mcp.tool()
def create_index(
    ctx: Context,
    bucket_name: str,
    index_name: str,
    dimensions: int,
    similarity: str = "COSINE",
    filterable_metadata: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """Create a vector index in a bucket."""
    client = _client()
    params: Dict[str, Any] = {
        "bucketName": bucket_name,
        "indexName": index_name,
        "dimensions": dimensions,
        "similarity": similarity,
    }
    if filterable_metadata:
        params["filterableMetadata"] = filterable_metadata
    return client.create_index(**params)


@mcp.tool()
def get_index(ctx: Context, bucket_name: str, index_name: str) -> Dict[str, Any]:
    """Get index configuration and statistics."""
    client = _client()
    return client.get_index(bucketName=bucket_name, indexName=index_name)


@mcp.tool()
def list_vectors(
    ctx: Context,
    bucket_name: str,
    index_name: str,
    include_data: bool = False,
    include_metadata: bool = False,
    next_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List vectors stored in an index."""
    client = _client()
    params: Dict[str, Any] = {
        "bucketName": bucket_name,
        "indexName": index_name,
        "includeData": include_data,
        "includeMetadata": include_metadata,
    }
    if next_token:
        params["nextToken"] = next_token
    return client.list_vectors(**params)


@mcp.tool()
def embed_and_store_text(
    ctx: Context,
    bucket_name: str,
    index_name: str,
    text: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Generate embeddings from text and store them in an index."""
    client = _client()
    params: Dict[str, Any] = {
        "bucketName": bucket_name,
        "indexName": index_name,
        "text": text,
    }
    if metadata:
        params["metadata"] = metadata
    return client.embed_and_store_text(**params)


@mcp.tool()
def embed_and_store_file(
    ctx: Context,
    bucket_name: str,
    index_name: str,
    file_path: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Embed a local file and store the vector."""
    client = _client()
    params: Dict[str, Any] = {
        "bucketName": bucket_name,
        "indexName": index_name,
        "filePath": file_path,
    }
    if metadata:
        params["metadata"] = metadata
    return client.embed_and_store_file(**params)


@mcp.tool()
def embed_and_store_s3_objects(
    ctx: Context,
    bucket_name: str,
    index_name: str,
    s3_uri_prefix: str,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Embed S3 objects and store vectors in batch."""
    client = _client()
    params: Dict[str, Any] = {
        "bucketName": bucket_name,
        "indexName": index_name,
        "s3UriPrefix": s3_uri_prefix,
    }
    if metadata:
        params["metadata"] = metadata
    return client.embed_and_store_s3_objects(**params)


@mcp.tool()
def embed_and_query_text(
    ctx: Context,
    bucket_name: str,
    index_name: str,
    text: str,
    top_k: int = 5,
) -> Dict[str, Any]:
    """Query an index using natural language text."""
    client = _client()
    return client.embed_and_query_text(
        bucketName=bucket_name, indexName=index_name, text=text, topK=top_k
    )


@mcp.tool()
def embed_and_query_file(
    ctx: Context,
    bucket_name: str,
    index_name: str,
    file_path: str,
    top_k: int = 5,
) -> Dict[str, Any]:
    """Query an index using a file's content."""
    client = _client()
    return client.embed_and_query_file(
        bucketName=bucket_name, indexName=index_name, filePath=file_path, topK=top_k
    )


def main() -> None:  # pragma: no cover - CLI entry point
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
