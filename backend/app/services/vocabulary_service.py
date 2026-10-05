from dataclasses import dataclass
from threading import RLock

from app.schemas.tokenization import TokenStatus, VocabularyEntry


@dataclass(frozen=True)
class VocabularyToken:
    token_id: int
    is_new: bool


class VocabularyService:
    """Process-local vocabulary. It is intentionally reset when the process restarts."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._entries: dict[str, tuple[int, int]] = {}

    def assign(self, tokens: list[str]) -> tuple[list[VocabularyToken], list[VocabularyEntry]]:
        with self._lock:
            staged = self._entries.copy()
            next_id = max((token_id for token_id, _ in staged.values()), default=-1) + 1
            newly_seen: set[str] = set()
            assigned: list[VocabularyToken] = []
            for token in tokens:
                entry = staged.get(token)
                if entry is None:
                    entry = (next_id, 0)
                    next_id += 1
                    newly_seen.add(token)
                staged[token] = (entry[0], entry[1] + 1)
                assigned.append(VocabularyToken(entry[0], token in newly_seen))
            self._entries = staged
            snapshot = self._snapshot(newly_seen)
            return assigned, snapshot

    def snapshot(self) -> list[VocabularyEntry]:
        with self._lock:
            return self._snapshot(set())

    def reset(self) -> list[VocabularyEntry]:
        with self._lock:
            self._entries.clear()
            return []

    def _snapshot(self, newly_seen: set[str]) -> list[VocabularyEntry]:
        return [
            VocabularyEntry(
                token_id=token_id,
                token=token,
                frequency=frequency,
                status=TokenStatus.NEW if token in newly_seen else TokenStatus.EXISTING,
            )
            for token, (token_id, frequency) in sorted(
                self._entries.items(), key=lambda item: item[1][0]
            )
        ]
