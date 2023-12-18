"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MusicMlValidator = exports.registerValidationChecks = void 0;
/**
 * Register custom validation checks.
 */
function registerValidationChecks(services) {
    const registry = services.validation.ValidationRegistry;
    const validator = services.validation.MusicMlValidator;
    const checks = {
        MusicPiece: validator.checkMusicPieceName
    };
    registry.register(checks, validator);
}
exports.registerValidationChecks = registerValidationChecks;
/**
 * Implementation of custom validations.
 */
class MusicMlValidator {
    checkMusicPieceName(musicPiece, accept) {
        if (musicPiece.name) {
            const firstChar = musicPiece.name.substring(0, 1);
            if (firstChar.toUpperCase() !== firstChar) {
                accept('warning', 'App name should start with a capital.', { node: musicPiece, property: 'name' });
            }
        }
    }
}
exports.MusicMlValidator = MusicMlValidator;
//# sourceMappingURL=music-ml-validator.js.map