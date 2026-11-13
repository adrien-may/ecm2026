import {Transform} from 'class-transformer';
import {IsInt, IsString, Length, Max, Min} from 'class-validator';

export class CreateScoreDto {
  @Transform(({value}) => typeof value === 'string' ? value.trim() : value)
  @IsString()
  @Length(1, 24)
  player!: string;

  @IsInt()
  @Min(0)
  @Max(90)
  points!: number;
}
