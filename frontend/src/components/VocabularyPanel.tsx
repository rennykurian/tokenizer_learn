import type { VocabularyEntry } from '../types/api';

interface VocabularyPanelProps {
  entries: VocabularyEntry[];
  disabled: boolean;
  onReset: () => void;
}

export function VocabularyPanel({ entries, disabled, onReset }: VocabularyPanelProps) {
  return (
    <section className="vocabulary-section" aria-labelledby="vocabulary-title">
      <div className="section-heading">
        <div><p className="eyebrow">Custom mode</p><h2 id="vocabulary-title">Vocabulary</h2></div>
        <button className="button button-quiet" type="button" disabled={disabled || entries.length === 0} onClick={onReset}>
          Reset vocabulary
        </button>
      </div>
      {entries.length === 0 ? (
        <p className="empty-note">Custom tokens appear here after analysis.</p>
      ) : (
        <div className="token-table-wrap">
          <table className="token-table vocabulary-table">
            <thead><tr><th>ID</th><th>Token</th><th>Frequency</th><th>Status</th></tr></thead>
            <tbody>
              {entries.map((entry) => (
                <tr key={entry.token_id}>
                  <td className="mono muted">{entry.token_id}</td>
                  <td><code className="token-chip">{entry.token}</code></td>
                  <td>{entry.frequency}</td>
                  <td><span className={`status status-${entry.status}`}>{entry.status === 'new' ? 'New' : 'Existing'}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}