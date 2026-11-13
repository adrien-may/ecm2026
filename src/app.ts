import 'reflect-metadata';
import {Controller, Get, Module} from '@nestjs/common';
import {NestFactory} from '@nestjs/core';

@Controller('health')
class HealthController {
  @Get()
  health() { return {status: 'ok'}; }
}
@Module({controllers: [HealthController]})
class AppModule {}
export async function createApplication() {
  return NestFactory.create(AppModule, {logger: false});
}
