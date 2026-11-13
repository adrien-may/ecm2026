import {createApplication} from './app';

async function main() {
  const app = await createApplication();
  app.enableShutdownHooks();
  await app.listen(8002, '127.0.0.1');
  console.log('Scores API: http://127.0.0.1:8002/scores/');
}

main().catch(error => { console.error(error); process.exitCode = 1; });
