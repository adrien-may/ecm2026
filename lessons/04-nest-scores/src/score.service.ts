import {Injectable} from '@nestjs/common';
import {CreateScoreDto} from './score.dto';
import {ScoreStore} from './score.store';

@Injectable()
export class ScoresService {
  constructor(private readonly store: ScoreStore) {}
  list() { return this.store.list(); }
  create(data: CreateScoreDto) { return this.store.create(data.player, data.points); }
}
