import { describe, expect, it, vi } from 'vitest';
import { ApiError, tokenize } from '../../src/services/apiClient';

describe('tokenize API client', () => {
  it('returns decoded successful responses', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({ tokens: [] }) }));
    await expect(tokenize({ text: 'hello', mode: 'custom' })).resolves.toEqual({ tokens: [] });
  });

  it('raises a readable error for API failures', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ error: { code: 'INVALID_INPUT', message: 'Enter text.' } }),
    }));
    await expect(tokenize({ text: '', mode: 'custom' })).rejects.toBeInstanceOf(ApiError);
  });
});