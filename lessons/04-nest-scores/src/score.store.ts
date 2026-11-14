import {Inject, Injectable, OnModuleDestroy} from '@nestjs/common';
import {mkdirSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {DatabaseSync} from 'node:sqlite';

export interface ScoreRow {id: number; player: string; points: number; created_at: string}

@Injectable()
export class ScoreStore implements OnModuleDestroy {
  private database: DatabaseSync;

  constructor(@Inject('DATABASE_PATH') path: string) {
    const filename = resolve(path);
    mkdirSync(dirname(filename), {recursive: true});
    this.database = new DatabaseSync(filename);
    this.database.exec(`CREATE TABLE IF NOT EXISTS score (
      id INTEGER PRIMARY KEY, player TEXT NOT NULL,
      points INTEGER NOT NULL, created_at TEXT NOT NULL
    )`);
  }

  list(): ScoreRow[] {
    return this.database.prepare('SELECT * FROM score ORDER BY points DESC, id ASC LIMIT 10').all() as unknown as ScoreRow[];
  }

  create(player: string, points: number): ScoreRow {
    const result = this.database.prepare('INSERT INTO score (player, points, created_at) VALUES (?, ?, ?)')
      .run(player, points, new Date().toISOString());
    return this.database.prepare('SELECT * FROM score WHERE id = ?').get(result.lastInsertRowid) as unknown as ScoreRow;
  }

  onModuleDestroy() { this.database.close(); }
}
