import type {
  ApiErrorPayload,
  ExtractedDocument,
  TokenizationRequest,
  TokenizationResponse,
  VocabularyEntry,
} from '../types/api';

const baseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api/v1';

export class ApiError extends Error {
  constructor(message: string, readonly code = 'REQUEST_FAILED') {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}`, init);
  } catch {
    throw new ApiError('Could not reach the tokenizer service. Check your connection and retry.', 'NETWORK_ERROR');
  }
  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const error = payload as ApiErrorPayload | null;
    throw new ApiError(error?.error?.message ?? 'The request could not be completed.', error?.error?.code);
  }
  return payload as T;
}

export function tokenize(input: TokenizationRequest): Promise<TokenizationResponse> {
  return request('/tokenize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
}

export function listEncodings(): Promise<string[]> {
  return request('/encodings');
}

export function extractFile(file: File): Promise<ExtractedDocument> {
  const body = new FormData();
  body.append('file', file);
  return request('/files/extract', { method: 'POST', body });
}

export function getVocabulary(): Promise<VocabularyEntry[]> {
  return request('/vocabulary');
}

export function resetVocabulary(): Promise<VocabularyEntry[]> {
  return request('/vocabulary', { method: 'DELETE' });
}