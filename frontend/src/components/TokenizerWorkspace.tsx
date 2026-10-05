import { useEffect, useState } from 'react';
import { ApiError, listEncodings, resetVocabulary, tokenize } from '../services/apiClient';
import type { ExtractedDocument, TokenizationResponse, TokenizerMode, VocabularyEntry } from '../types/api';
import { FileInput } from './FileInput';
import { TokenResults } from './TokenResults';
import { VocabularyPanel } from './VocabularyPanel';

export function TokenizerWorkspace() {
  const [text, setText] = useState('');
  const [mode, setMode] = useState<TokenizerMode>('tiktoken');
  const [encodings, setEncodings] = useState<string[]>([]);
  const [encoding, setEncoding] = useState('');
  const [result, setResult] = useState<TokenizationResponse | null>(null);
  const [vocabulary, setVocabulary] = useState<VocabularyEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    void listEncodings().then((values) => {
      if (!active) return;
      setEncodings(values);
      setEncoding((current) => current || values[0] || '');
    }).catch((reason: unknown) => {
      if (active) setError(reason instanceof ApiError ? reason.message : 'Unable to load supported encodings.');
    });
    return () => { active = false; };
  }, []);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    if (!text.trim()) {
      setError('Enter non-whitespace text to tokenize.');
      return;
    }
    setLoading(true);
    try {
      const next = await tokenize({ text, mode, ...(mode === 'tiktoken' ? { encoding } : {}) });
      setResult(next);
      if (mode === 'custom') setVocabulary(next.vocabulary);
    } catch (reason) {
      setError(reason instanceof ApiError ? reason.message : 'Tokenization failed. Please retry.');
    } finally {
      setLoading(false);
    }
  }

  async function handleExtracted(document: ExtractedDocument) {
    setText(document.text);
    setResult(null);
    setError('');
  }

  async function handleReset() {
    setError('');
    try {
      setVocabulary(await resetVocabulary());
      setResult(null);
    } catch (reason) {
      setError(reason instanceof ApiError ? reason.message : 'Vocabulary could not be reset.');
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Token Lab home"><span className="brand-mark">T</span><span>token<span className="brand-accent">lab</span></span></a>
        <span className="topbar-note"><span className="pulse-dot" /> Backend analysis active</span>
      </header>
      <div className="workspace" id="top">
        <section className="input-section" aria-labelledby="page-title">
          <div className="intro-row">
            <div><p className="eyebrow">Tokenizer workbench <span>01 / 03</span></p><h1 id="page-title">See text<br /><em>in pieces.</em></h1></div>
            <p className="intro-copy">Explore how text becomes tokens. Choose an encoding, inspect each token, and compare the vocabulary as it grows.</p>
          </div>
          <form onSubmit={submit}>
            <label className="field-label" htmlFor="text-input">Text to tokenize</label>
            <textarea id="text-input" value={text} onChange={(event) => setText(event.target.value)} placeholder="Type or paste something to explore…" rows={7} disabled={loading} />
            <div className="input-meta"><FileInput disabled={loading} onExtracted={handleExtracted} /></div>
            <div className="controls-row">
              <fieldset className="mode-picker" disabled={loading}>
                <legend>Tokenizer</legend>
                <label><input type="radio" name="mode" value="tiktoken" checked={mode === 'tiktoken'} onChange={() => setMode('tiktoken')} /><span>Tiktoken</span></label>
                <label><input type="radio" name="mode" value="custom" checked={mode === 'custom'} onChange={() => setMode('custom')} /><span>Custom</span></label>
              </fieldset>
              {mode === 'tiktoken' && <label className="encoding-control">Encoding<select aria-label="Tiktoken encoding" value={encoding} onChange={(event) => setEncoding(event.target.value)} disabled={loading || encodings.length === 0}>{encodings.map((item) => <option key={item} value={item}>{item}</option>)}</select></label>}
              <button className="button button-primary" type="submit" disabled={loading || (mode === 'tiktoken' && !encoding)}>{loading ? 'Analyzing…' : 'Tokenize  ↗'}</button>
            </div>
          </form>
          {error && <p className="error-banner" role="alert">{error}</p>}
        </section>
        {result ? <TokenResults result={result} /> : <section className="waiting-state" aria-live="polite"><span className="waiting-glyph">⌁</span><span>Your token map will appear here</span></section>}
        <VocabularyPanel entries={vocabulary} disabled={loading} onReset={() => void handleReset()} />
      </div>
      <footer><span>Token Lab</span><span>Tokenization happens on the backend</span><span>01 — Explore</span></footer>
    </main>
  );
}