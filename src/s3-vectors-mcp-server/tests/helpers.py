def process_stdout_results(stdout_string: str):
    """Parse out dictionary from stdout results from s3vector-embed-cli commands."""
    idx = stdout_string.find('{')
    return eval(stdout_string[idx:])
