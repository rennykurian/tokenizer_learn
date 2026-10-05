import tiktoken

from app.schemas.tokenization import TokenResult


class TiktokenService:
    def list_encodings(self) -> list[str]:
        return sorted(tiktoken.list_encoding_names())

    def tokenize(self, text: str, encoding_name: str) -> list[TokenResult]:
        if encoding_name not in tiktoken.list_encoding_names():
            raise ValueError(f"Unsupported Tiktoken encoding: {encoding_name}")
        encoding = tiktoken.get_encoding(encoding_name)
        token_ids = encoding.encode(text)
        results: list[TokenResult] = []
        for index, token_id in enumerate(token_ids):
            token_bytes = encoding.decode_single_token_bytes(token_id)
            results.append(
                TokenResult(
                    index=index,
                    token_id=token_id,
                    text=encoding.decode([token_id]),
                    details={
                        "byte_length": len(token_bytes),
                        "token_bytes_hex": token_bytes.hex(),
                    },
                )
            )
        return results
