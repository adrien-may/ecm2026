import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {mountGame} from './canvas.js';
import {createApi} from './api.js';
import './style.css';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001';
const request = createApi(apiUrl);

function App() {
  const canvas = useRef(null);
  const game = useRef(null);
  const [state, setState] = useState(null);
  const [scores, setScores] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

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

  function restart() {
    setError('');
    game.current.restart();
  }

  const finished = state && state.status !== 'playing';
  return <main>
    <p className="eyebrow">ECM · MON PROJET ECM</p>
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
        <button onClick={restart}>Rejouer</button>
      </div>
      <p className="hint">Une perte de focus met le jeu en pause. Reprendre le relance. 10 points par cible, puis un bonus de temps à la victoire.</p>
      <p role="status">{finished ? `${state.status === 'won' ? 'Victoire' : 'Partie terminée'} : ${state.score} points.` : 'Partie en cours.'}</p>

    </section><aside>
      <div className="list-heading"><h2>Top 10</h2><button className="secondary" disabled={loading} onClick={() => loadScores()}>Recharger</button></div>
      {loading ? <p>Chargement…</p> : scores.length === 0 ? <p>Aucun score pour le moment.</p> : <ol>{scores.map(score => <li key={score.id}><span>{score.player}</span><strong>{score.points}</strong></li>)}</ol>}
      <p className="hint">Ce classement de démonstration accepte les scores déclarés par le client.</p>
    </aside></div>
    {error && <p role="alert" className="error">{error}</p>}
    <footer>Backend : <code>{apiUrl}</code></footer>
  </main>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);
