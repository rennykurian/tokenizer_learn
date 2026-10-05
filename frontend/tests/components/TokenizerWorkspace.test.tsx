import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { TokenizerWorkspace } from '../../src/components/TokenizerWorkspace';

vi.mock('../../src/services/apiClient', () => ({
  listEncodings: vi.fn().mockResolvedValue(['cl100k_base']),
  tokenize: vi.fn().mockResolvedValue({
    mode: 'custom', encoding: null,
    tokens: [{ index: 0, token_id: 0, text: 'hello', details: {}, is_new: true }],
    statistics: { character_count: 5, word_count: 1, token_count: 1, tokens_per_word: 1, tokens_per_character: 0.2 },
    vocabulary: [{ token_id: 0, token: 'hello', frequency: 1, status: 'new' }],
  }),
}));

describe('TokenizerWorkspace', () => {
  beforeEach(() => vi.clearAllMocks());

  it('submits entered text and shows tokens and statistics', async () => {
    render(<TokenizerWorkspace />);
    fireEvent.change(screen.getByLabelText(/text to tokenize/i), { target: { value: 'hello' } });
    fireEvent.click(screen.getByLabelText('Custom'));
    fireEvent.click(screen.getByRole('button', { name: /tokenize/i }));
    expect(await screen.findByText('hello')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/tokens per character/i)).toBeInTheDocument());
  });
});