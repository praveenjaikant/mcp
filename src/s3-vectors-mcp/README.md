We propose contributing the AWS S3 Vectors MCP Server to AWS Labs. This server enables AI applications and tools to interact with AWS S3 Vectors service using natural language for vector storage, embedding generation, and semantic search operations. The server provides a secure interface for managing vector buckets, indexes, and performing similarity queries while integrating with Amazon Bedrock for embedding generation.

The MCP server implements 12 core tools covering vector operations from bucket management to semantic search, with security-first principles including read-only default mode and intentional exclusion of delete operations.

Use case
Retrieval-Augmented Generation (RAG) and Knowledge Management

Create searchable knowledge bases from documents and enterprise content
Enable AI applications to answer questions using domain-specific information
Support natural language queries over large document collections
Intelligent Content Processing

Automatically categorize and organize content based on semantic similarity
Batch process S3 objects for vector embedding and automated indexing
Detect duplicate or similar content across large datasets
Image Similarity and Visual Search

Store and query image embeddings for visual similarity search
Enable content-based image retrieval systems
Support visual duplicate detection and organization
Multi-modal AI Applications

Combine text and image embeddings in unified search experiences
Support cross-modal similarity queries (text-to-image, image-to-text)
Enable complex AI workflows involving multiple content types
With the S3 Vectors MCP Server, users can have conversations like:

User: "create a new vector bucket s3b-mcp-test, index s3i-mcp-test with 1024 dimensions and S3VECTORS-EMBED-SRC-CONTENT as non filterable metadata."
AI Assistant: "Successfully created vector bucket s3b-mcp-test and vector index s3i-mcp-test"

User: "Find images similar to this image s3://my-bucket/image1.png"
AI Assistant: "Found 5 similar images to this image"

Proposal
What We're Building
A Python-based MCP server that exposes 12 tools for AI assistants:

Bucket Operations

list_vector_buckets - Lists all vector buckets with pagination and filtering
create_vector_bucket - Creates new vector storage containers with encryption options
get_vector_bucket - Retrieves bucket metadata and configuration
Index Operations

list_indexes - Browse indexes within buckets with filtering capabilities
create_index - Configure indexes with specific dimensions and similarity metrics
get_index - Access index configuration and statistics
Vector Operations

list_vectors - Lists vectors in an index with optional data and metadata
embed_and_store_text - Generate embeddings from text using Bedrock models
embed_and_store_file - Process local files for embedding generation and storage
embed_and_store_s3_objects - Batch process S3 objects with parallel processing
Query Operations

embed_and_query_text - Query vector indexes using natural language
embed_and_query_file - Use file content as query input for similarity search
Technical Approach
Uses boto3 for AWS API interactions and s3vectors-embed-cli for reliable operations
Implements MCP protocol via FastMCP framework
Supports standard AWS authentication (IAM roles, credentials)
Configurable via command-line flags (--allow-write, --aws-profile, --aws-region)
Includes comprehensive error handling and structured logging
Supports Amazon Bedrock embedding models: Titan Text v1/v2, Cohere English/Multilingual, Titan Image
Integration
Works with any MCP-compatible AI assistant:

Amazon Q Developer
Kiro
Claude Desktop
GitHub Copilot
Custom AI applications
Out of scope
Destructive Delete Operations

Vector bucket deletion through MCP interface
Vector index deletion through MCP interface
Individual vector deletion through MCP interface
Rationale: These operations are intentionally excluded for safety and must be performed via AWS CLI
Potential challenges
Embedding Model Consistency
Challenge: Different Bedrock models produce embeddings with varying dimensions
Mitigation: Strict validation of model-index dimension compatibility and clear documentation

Large-Scale Batch Processing
Challenge: Processing thousands of S3 objects efficiently without overwhelming services
Mitigation: Intelligent batching with exponential backoff and memory-efficient streaming

AWS Service Limits
Challenge: S3 Vectors service has limits on buckets, indexes, and vectors per account
Mitigation: Proactive quota monitoring and clear documentation of service limits

Cost Management
Challenge: Vector storage and Bedrock embedding costs can scale rapidly
Mitigation: Cost estimation guidance and batch processing optimization

Security and Access Control
Challenge: Balancing ease of use with security requirements
Mitigation: Principle of least privilege by default, comprehensive IAM policy templates

Dependencies and Integrations
Core Dependencies:

AWS SDK for Python (Boto3) >= 1.34.0
FastMCP >= 1.11.0
Pydantic >= 2.10.6
s3vectors-embed-cli >= 0.1.0
AWS Services Integration:

AWS S3 Vectors (primary vector storage)
Amazon Bedrock (embedding generation)
AWS IAM (authentication and authorization)
Amazon S3 (source data access for batch processing)
