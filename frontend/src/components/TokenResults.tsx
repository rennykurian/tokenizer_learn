import type { TokenizationResponse } from '../types/api';

interface TokenResultsProps {
  result: TokenizationResponse;
}

const metrics = [
  ['Characters', 'character_count'],
  ['Words', 'word_count'],
  ['Tokens', 'token_count'],
  ['Tokens per word', 'tokens_per_word'],
  ['Tokens per character', 'tokens_per_character'],
] as const;

export function TokenResults({ result }: TokenResultsProps) {
  return (
    <section className="results-section" aria-labelledby="results-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Analysis</p>
          <h2 id="results-title">Token breakdown</h2>
        </div>
        <span className="result-mode">{result.mode === 'tiktoken' ? result.encoding : 'Custom Tokenizer'}</span>
      </div>
      <div className="metrics-grid">
        {metrics.map(([label, key]) => (
          <div className="metric" key={key}>
            <span>{label}</span>
            <strong>{result.statistics[key]}</strong>
          </div>
        ))}
      </div>
      <div className="token-table-wrap">
        <table className="token-table">
          <thead><tr><th>Index</th><th>ID</th><th>Token</th><th>Details</th></tr></thead>
          <tbody>
            {result.tokens.map((token) => (
              <tr key={`${token.index}-${token.token_id}`}>
                <td className="mono muted">{token.index}</td>
                <td className="mono">{token.token_id}</td>
                <td><code className="token-chip">{token.text || '∅'}</code></td>
                <td className="detail-cell">
                  {token.is_new && <span className="status status-new">New</span>}
                  {Object.entries(token.details).map(([key, value]) => <span key={key}>{key}: {String(value)}</span>)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}