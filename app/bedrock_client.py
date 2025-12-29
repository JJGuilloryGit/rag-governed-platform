import boto3
from botocore.config import Config
from .config import settings

def invoke_bedrock(prompt: str) -> str:
    """Invoke Bedrock text model.

    This uses the Bedrock Runtime API. The payload format varies by model provider.
    For interview demos, keep it simple and adjust the body for your selected model.
    """
    client = boto3.client("bedrock-runtime", region_name=settings.region, config=Config(retries={"max_attempts": 3}))

    # Minimal Anthropic-style payload (adjust if you choose a different model provider)
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 600,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
    }
    resp = client.invoke_model(modelId=settings.bedrock_model_id, body=json_bytes(body))
    data = resp["body"].read()
    return parse_text(data)

def json_bytes(obj):
    import json
    return json.dumps(obj).encode("utf-8")

def parse_text(raw_bytes: bytes) -> str:
    import json
    payload = json.loads(raw_bytes.decode("utf-8"))
    # Anthropic response shape (may differ by model)
    try:
        return payload["content"][0]["text"]
    except Exception:
        return str(payload)
