import {Body, Controller, Get, Post} from '@nestjs/common';
import {CreateScoreDto} from './score.dto';
import {ScoresService} from './score.service';

@Controller('scores')
export class ScoresController {
  constructor(private readonly scores: ScoresService) {}

  @Get()
  list() { return this.scores.list(); }

  @Post()
  create(@Body() data: CreateScoreDto) { return this.scores.create(data); }
}
