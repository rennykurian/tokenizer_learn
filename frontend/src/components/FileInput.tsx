import { useRef, useState } from 'react';
import { ApiError, extractFile } from '../services/apiClient';
import type { ExtractedDocument } from '../types/api';

interface FileInputProps {
  disabled: boolean;
  onExtracted: (document: ExtractedDocument) => void;
}

export function FileInput({ disabled, onExtracted }: FileInputProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fileName, setFileName] = useState('');

  async function selectFile(file?: File) {
    if (!file) return;
    setError('');
    setFileName(file.name);
    if (!/\.(txt|pdf)$/i.test(file.name)) {
      setError('Choose a TXT or PDF file.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('The file exceeds the 10 MiB limit.');
      return;
    }
    setLoading(true);
    try {
      onExtracted(await extractFile(file));
    } catch (reason) {
      setError(reason instanceof ApiError ? reason.message : 'The file could not be processed.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="file-control">
      <input
        ref={inputRef}
        className="visually-hidden"
        type="file"
        accept=".txt,.pdf,text/plain,application/pdf"
        aria-label="Upload a TXT or PDF file"
        disabled={disabled || loading}
        onChange={(event) => void selectFile(event.target.files?.[0])}
      />
      <button className="button button-quiet" type="button" disabled={disabled || loading} onClick={() => inputRef.current?.click()}>
        {loading ? 'Extracting…' : '↑  Upload file'}
      </button>
      <span className="file-hint">TXT / PDF · 10 MiB max</span>
      {fileName && !error && <span className="file-name">{fileName}</span>}
      {error && <p className="inline-error" role="alert">{error}</p>}
    </div>
  );
}