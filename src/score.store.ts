import {Injectable} from '@nestjs/common';
export interface ScoreRow {id: number; player: string; points: number; created_at: string}
@Injectable()
export class ScoreStore {
  private rows: ScoreRow[] = [];
  list() { return [...this.rows].sort((a, b) => b.points - a.points || a.id - b.id).slice(0, 10); }
  create(player: string, points: number) {
    const row = {id: this.rows.length + 1, player, points, created_at: new Date().toISOString()};
    this.rows.push(row);
    return row;
  }
}
