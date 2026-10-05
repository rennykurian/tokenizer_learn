export type TokenizerMode = 'tiktoken' | 'custom';

export interface TokenizationRequest {
  text: string;
  mode: TokenizerMode;
  encoding?: string;
}

export interface TokenResult {
  index: number;
  token_id: number;
  text: string;
  details: Record<string, string | number | boolean | null>;
  is_new: boolean;
}

export interface TokenStatistics {
  character_count: number;
  word_count: number;
  token_count: number;
  tokens_per_word: number;
  tokens_per_character: number;
}

export interface VocabularyEntry {
  token_id: number;
  token: string;
  frequency: number;
  status: 'new' | 'existing';
}

export interface TokenizationResponse {
  mode: TokenizerMode;
  encoding: string | null;
  tokens: TokenResult[];
  statistics: TokenStatistics;
  vocabulary: VocabularyEntry[];
}

export interface ExtractedDocument {
  text: string;
  source_type: 'txt' | 'pdf';
}

export interface ApiErrorPayload {
  error: { code: string; message: string };
}