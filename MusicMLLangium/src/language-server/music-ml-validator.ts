import { ValidationAcceptor, ValidationChecks } from 'langium';
import {MusicMlAstType, MusicPiece} from './generated/ast';
import type { MusicMlServices } from './music-ml-module';

/**
 * Register custom validation checks.
 */
export function registerValidationChecks(services: MusicMlServices) {
  const registry = services.validation.ValidationRegistry;
  const validator = services.validation.MusicMlValidator;
  const checks: ValidationChecks<MusicMlAstType> = {
    MusicPiece: validator.checkMusicPieceName
  };
  registry.register(checks, validator);
}

/**
 * Implementation of custom validations.
 */
export class MusicMlValidator {

  checkMusicPieceName(musicPiece: MusicPiece, accept: ValidationAcceptor): void {
    if (musicPiece.name) {
      const firstChar = musicPiece.name.substring(0, 1);
      if (firstChar.toUpperCase() !== firstChar) {
        accept('warning', 'App name should start with a capital.', {node: musicPiece, property: 'name'});
      }
    }
  }
}