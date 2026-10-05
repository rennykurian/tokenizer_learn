import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { VocabularyPanel } from '../../src/components/VocabularyPanel';

describe('VocabularyPanel', () => {
  it('shows IDs, token, frequency, status, and supports reset', () => {
    const onReset = vi.fn();
    render(<VocabularyPanel entries={[
      { token_id: 0, token: 'hello', frequency: 2, status: 'new' },
    ]} disabled={false} onReset={onReset} />);

    expect(screen.getByRole('cell', { name: '0' })).toBeInTheDocument();
    expect(screen.getByText('hello')).toBeInTheDocument();
    expect(screen.getByRole('cell', { name: '2' })).toBeInTheDocument();
    expect(screen.getByText('New')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reset vocabulary' }));
    expect(onReset).toHaveBeenCalledOnce();
  });
});