import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { FileInput } from '../../src/components/FileInput';

vi.mock('../../src/services/apiClient', () => ({
  extractFile: vi.fn().mockResolvedValue({ text: 'from file', source_type: 'txt' }),
}));

describe('FileInput', () => {
  it('uploads a valid TXT file and returns extracted text', async () => {
    const onExtracted = vi.fn();
    render(<FileInput disabled={false} onExtracted={onExtracted} />);
    const input = screen.getByLabelText(/upload a txt or pdf file/i);
    const file = new File(['from file'], 'notes.txt', { type: 'text/plain' });
    fireEvent.change(input, { target: { files: [file] } });
    expect(await screen.findByText('notes.txt')).toBeInTheDocument();
    expect(onExtracted).toHaveBeenCalledWith({ text: 'from file', source_type: 'txt' });
  });

  it('rejects unsupported file types before uploading', () => {
    render(<FileInput disabled={false} onExtracted={vi.fn()} />);
    const input = screen.getByLabelText(/upload a txt or pdf file/i);
    const file = new File(['data'], 'data.docx', { type: 'application/octet-stream' });
    fireEvent.change(input, { target: { files: [file] } });
    expect(screen.getByRole('alert')).toHaveTextContent('Choose a TXT or PDF file.');
  });
});