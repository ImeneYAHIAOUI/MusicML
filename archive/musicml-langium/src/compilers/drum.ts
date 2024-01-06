
export function compileDrum(drumNote: string): string {
    const note =
        drumNote === "bd"
            ? "C2"
            : drumNote === "sd"
                ? "E2"
                : drumNote === "ch"
                    ? "F#2"
                    : drumNote === "oh"
                        ? "A#2"
                        : drumNote === "rc"
                            ? "F2"
                            : "D#2";
    return note;
}