import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { VocabularyPanel } from '../../src/components/VocabularyPanel';

describe('workspace accessibility', () => {
  it('labels vocabulary columns and does not rely on color for entry status', () => {
    render(<VocabularyPanel entries={[
      { token_id: 1, token: 'fresh', frequency: 1, status: 'new' },
      { token_id: 0, token: 'known', frequency: 3, status: 'existing' },
    ]} disabled={false} onReset={vi.fn()} />);

    expect(screen.getByRole('columnheader', { name: 'Status' })).toBeInTheDocument();
    expect(screen.getByText('New')).toBeInTheDocument();
    expect(screen.getByText('Existing')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Reset vocabulary' })).toBeEnabled();
  });
});