// The three lines of work shown on the Lab page (/blog).
// A post joins one with `direction: <id>` in its frontmatter; posts without it are listed under "Earlier projects".
// Text and covers for each direction live in src/data/directions.ts.
export const DIRECTION_IDS = ['lidar', 'earth-observation', 'data-systems'] as const;
export type DirectionId = (typeof DIRECTION_IDS)[number];
