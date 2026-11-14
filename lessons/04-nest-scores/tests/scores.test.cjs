const assert = require('node:assert/strict');
const {test} = require('node:test');
const {mkdtemp, rm} = require('node:fs/promises');
const {tmpdir} = require('node:os');
const {join} = require('node:path');
const {createApplication} = require('../dist/app.js');

async function setup(t) {
  const folder = await mkdtemp(join(tmpdir(), 'ecm-scores-'));
  const filename = join(folder, 'test.sqlite');
  let app = await createApplication(filename);
  await app.listen(0, '127.0.0.1');
  let base = await app.getUrl();
  t.after(async () => { await app.close(); await rm(folder, {recursive: true}); });
  return {
    async request(method = 'GET', data) {
      return fetch(`${base}/scores/`, {method, ...(data === undefined ? {} : {
        headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data),
      })});
    },
    async restart() {
      await app.close();
      app = await createApplication(filename);
      await app.listen(0, '127.0.0.1');
      base = await app.getUrl();
    },
  };
}

test('POST creates a normalized score and GET reads it', async t => {
  const api = await setup(t);
  const response = await api.request('POST', {player: ' Samira ', points: 60});
  assert.equal(response.status, 201);
  const score = await response.json();
  assert.equal(score.player, 'Samira');
  assert.equal(score.points, 60);
  assert.equal(typeof score.id, 'number');
  assert.ok(!Number.isNaN(Date.parse(score.created_at)));
  assert.deepEqual(await (await api.request()).json(), [score]);
});

test('invalid data and unexpected fields do not create rows', async t => {
  const api = await setup(t);
  for (const data of [
    {player: ' ', points: 1}, {player: 'x'.repeat(25), points: 1},
    {player: 'A', points: -1}, {player: 'A', points: 91},
    {player: 'A', points: '60'}, {player: 'A', points: true},
    {player: 'A', points: 1.5}, {player: 'A', points: 1, id: 7},
  ]) assert.equal((await api.request('POST', data)).status, 400);
  assert.deepEqual(await (await api.request()).json(), []);
});

test('leaderboard is descending, limited, and stable for ties', async t => {
  const api = await setup(t);
  await api.request('POST', {player: 'First', points: 50});
  await api.request('POST', {player: 'Second', points: 50});
  for (let points = 0; points < 12; points++) await api.request('POST', {player: 'Other', points});
  const rows = await (await api.request()).json();
  assert.equal(rows.length, 10);
  assert.deepEqual(rows.slice(0, 2).map(row => row.player), ['First', 'Second']);
  assert.deepEqual(rows.map(row => row.points), [50, 50, 11, 10, 9, 8, 7, 6, 5, 4]);
});

test('scores survive an application restart', async t => {
  const api = await setup(t);
  await api.request('POST', {player: 'A', points: 30});
  await api.restart();
  assert.equal((await (await api.request()).json())[0].points, 30);
});
