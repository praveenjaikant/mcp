import ast
from pathlib import Path


def test_all_tools_defined():
    server_path = Path(__file__).resolve().parents[1] / 'awslabs' / 's3_vectors_mcp_server' / 'server.py'
    source = server_path.read_text()
    tree = ast.parse(source)
    tools = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                if (
                    isinstance(dec, ast.Call)
                    and isinstance(dec.func, ast.Attribute)
                    and dec.func.attr == 'tool'
                ):
                    tools.append(node.name)
    expected = {
        'list_vector_buckets',
        'create_vector_bucket',
        'get_vector_bucket',
        'list_indexes',
        'create_index',
        'get_index',
        'list_vectors',
        'embed_and_store_text',
        'embed_and_store_file',
        'embed_and_store_s3_objects',
        'embed_and_query_text',
        'embed_and_query_file',
    }
    assert expected.issubset(set(tools)), tools
