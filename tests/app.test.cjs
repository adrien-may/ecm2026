const assert = require('node:assert/strict');
const {test} = require('node:test');
const {createApplication} = require('../dist/app');
test('health returns a useful response', async () => {
  const app = await createApplication();
  await app.listen(0, '127.0.0.1');
  try {
    const response = await fetch(`${await app.getUrl()}/health`);
    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), {status: 'ok'});
  } finally { await app.close(); }
});
