import 'reflect-metadata';
import {Module, ValidationPipe} from '@nestjs/common';
import {NestFactory} from '@nestjs/core';
import {ScoresController} from './score.controller';
import {ScoresService} from './score.service';
import {ScoreStore} from './score.store';

@Module({controllers: [ScoresController], providers: [ScoresService, ScoreStore]})
class AppModule {}

export async function createApplication(databasePath = 'instance/nest-scores.sqlite') {
  const app = await NestFactory.create({
    module: AppModule,
    providers: [{provide: 'DATABASE_PATH', useValue: databasePath}],
  }, {logger: false});
  app.useGlobalPipes(new ValidationPipe({
    transform: true, whitelist: true, forbidNonWhitelisted: true,
  }));
  app.enableCors({
    origin: ['http://localhost:5175', 'http://127.0.0.1:5175'],
    methods: ['GET', 'POST'], allowedHeaders: ['Content-Type'],
  });
  return app;
}
