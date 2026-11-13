import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {mountGame} from './canvas.js';
import {createApi, jsonBody} from './api.js';
import './style.css';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001';
const request = createApi(apiUrl);

function App() {
  const canvas = useRef(null);
  const game = useRef(null);
  const [state, setState] = useState(null);
  const [player, setPlayer] = useState('');
  const [scores, setScores] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    game.current = mountGame(canvas.current, setState);
    return () => { game.current.destroy(); game.current = null; };
  }, []);

  async function loadScores(signal) {
    setLoading(true);
    try {
      const rows = await request('/scores/', {signal});
      setScores(rows);
      setError('');
    } catch (error) {
      if (error.name !== 'AbortError') setError(error.message);
    } finally {
      if (!signal?.aborted) setLoading(false);
    }
  }

  useEffect(() => {
    const controller = new AbortController();
    loadScores(controller.signal);
    return () => controller.abort();
  }, []);

  async function save(event) {
    event.preventDefault();
    if (!state || state.status === 'playing' || saved || saving) return;
    setSaving(true);
    setError('');
    try {
      await request('/scores/', jsonBody('POST', {player, points: state.score}));
      setSaved(true);
      await loadScores();
    } catch (error) { setError(`${error.message} Rechargez le classement avant de réessayer.`); }
    finally { setSaving(false); }
  }

  function restart() {
    setSaved(false);
    setError('');
    game.current.restart();
  }

  const finished = state && state.status !== 'playing';
  return <main>
    <p className="eyebrow">ECM · PROJET DE RÉFÉRENCE</p>
    <h1>Six cibles. Une partie.</h1>
    <p>30 secondes. Flèches pour bouger, espace pour tirer. Cliquez dans le jeu pour activer le clavier.</p>
    <div className="game-layout"><section aria-label="Le jeu">
      <canvas ref={canvas} width="640" height="400" tabIndex="0" aria-label="Jeu de tir : flèches gauche et droite, espace pour tirer." />
      <div className="controls">
        {['left', 'fire', 'right'].map((key, i) => <button key={key}
          onPointerDown={event => {event.currentTarget.setPointerCapture(event.pointerId); game.current.setInput(key, true);}}
          onPointerUp={() => game.current.setInput(key, false)} onPointerCancel={() => game.current.setInput(key, false)}>
          {['← Gauche', 'Tirer', 'Droite →'][i]}</button>)}
        <button onClick={() => game.current.pause()}>Pause</button>
        <button onClick={() => game.current.resume()}>Reprendre</button>
        <button onClick={restart} disabled={saving}>Rejouer</button>
      </div>
      <p className="hint">Une perte de focus met le jeu en pause. Reprendre le relance. 10 points par cible, puis un bonus de temps à la victoire.</p>
      <p role="status">{finished ? `${state.status === 'won' ? 'Victoire' : 'Partie terminée'} : ${state.score} points.` : 'Partie en cours.'}</p>
      {finished && <form onSubmit={save}>
        <label htmlFor="player">Votre pseudo</label>
        <div className="input-row"><input id="player" maxLength={24} value={player} onChange={event => setPlayer(event.target.value)} disabled={saving || saved} required />
        <button disabled={!player.trim() || saving || saved}>{saved ? 'Score enregistré' : saving ? 'Enregistrement…' : 'Enregistrer mon score'}</button></div>
      </form>}
    </section><aside>
      <div className="list-heading"><h2>Top 10</h2><button className="secondary" disabled={saving || loading} onClick={() => loadScores()}>Recharger</button></div>
      {loading ? <p>Chargement…</p> : scores.length === 0 ? <p>Aucun score pour le moment.</p> : <ol>{scores.map(score => <li key={score.id}><span>{score.player}</span><strong>{score.points}</strong></li>)}</ol>}
      <p className="hint">Ce classement de démonstration accepte les scores déclarés par le client.</p>
    </aside></div>
    {error && <p role="alert" className="error">{error}</p>}
    <footer>Backend : <code>{apiUrl}</code></footer>
  </main>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);
