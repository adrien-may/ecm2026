import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {createApi, jsonBody} from './api.js';
import './style.css';

const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:5001';
const request = createApi(baseUrl);

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [reload, setReload] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError('');
    request('/tasks/', {signal: controller.signal})
      .then(setTasks)
      .catch(error => { if (error.name !== 'AbortError') setError(error.message); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [reload]);

  async function mutate(action) {
    setBusy(true);
    setError('');
    try { await action(); }
    catch (error) { setError(error.message); }
    finally { setBusy(false); }
  }

  function add(event) {
    event.preventDefault();
    if (!title.trim()) return;
    mutate(async () => {
      const task = await request('/tasks/', jsonBody('POST', {title}));
      setTasks(current => [...current, task]);
      setTitle('');
    });
  }

  function toggle(task) {
    mutate(async () => {
      const updated = await request(`/tasks/${task.id}`, jsonBody('PATCH', {done: !task.done}));
      setTasks(current => current.map(item => item.id === task.id ? updated : item));
    });
  }

  function remove(task) {
    mutate(async () => {
      await request(`/tasks/${task.id}`, {method: 'DELETE'});
      setTasks(current => current.filter(item => item.id !== task.id));
    });
  }

  return <main>
    <p className="eyebrow">ECM · JOUR 1 → JOUR 2</p>
    <h1>Une chose à la fois.</h1>
    <p className="intro">Le même client, deux backends. Vos tâches restent enregistrées dans le backend sélectionné.</p>
    <p className="endpoint">API <code>{baseUrl}</code></p>
    <form onSubmit={add}>
      <label htmlFor="title">Nouvelle tâche</label>
      <div className="input-row">
        <input id="title" value={title} onChange={e => setTitle(e.target.value)} maxLength={255} placeholder="Que voulez-vous faire ?" disabled={busy || loading} />
        <button disabled={busy || loading || !title.trim()}>Ajouter</button>
      </div>
    </form>
    {error && <div role="alert" className="error">{error}</div>}
    {loading ? <p role="status">Chargement…</p> : <>
      <div className="list-heading"><h2>Mes tâches <span>{tasks.length}</span></h2><button className="secondary" disabled={busy} onClick={() => setReload(x => x + 1)}>Recharger</button></div>
      {tasks.length === 0 && !error && <p className="empty">La liste est vide. Ajoutez votre première tâche.</p>}
      <ul>{tasks.map(task => <li key={task.id}>
        <label className={task.done ? 'done' : ''}><input type="checkbox" checked={task.done} disabled={busy} onChange={() => toggle(task)} />{task.title}</label>
        <button className="secondary" disabled={busy} aria-label={`Supprimer ${task.title}`} onClick={() => remove(task)}>Supprimer</button>
      </li>)}</ul>
    </>}
    <footer>Créer · terminer · supprimer · recharger</footer>
  </main>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);
