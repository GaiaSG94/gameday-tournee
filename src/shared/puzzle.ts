export type Stop = { name: string; row: number; col: number };

export type TourPuzzle = {
  day: string;
  depot: Stop;
  stops: Stop[];
  grid: number;
  optimalLength: number;
};

const STOP_NAMES = ['bakery', 'library', 'florist', 'post', 'atelier', 'school'];

export const dayKeyUTC = (now: Date = new Date()): string => now.toISOString().slice(0, 10);

export const dailySeed = (day: string): number => {
  let hash = 2166136261;
  const input = 'tournee:' + day;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
};

export const mulberry32 = (seed: number): (() => number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

export const distance = (a: Stop, b: Stop): number =>
  Math.abs(a.row - b.row) + Math.abs(a.col - b.col);

export const routeLength = (depot: Stop, stops: Stop[], order: number[]): number => {
  let total = 0;
  let current = depot;
  for (const index of order) {
    const next = stops[index];
    if (!next) continue;
    total += distance(current, next);
    current = next;
  }
  return total + distance(current, depot);
};

export const optimalRoute = (depot: Stop, stops: Stop[]): { order: number[]; length: number } => {
  const n = stops.length;
  let best: number[] = [];
  let bestLength = Number.MAX_SAFE_INTEGER;
  const order: number[] = [];
  const used = new Set<number>();
  const walk = (): void => {
    if (order.length === n) {
      const length = routeLength(depot, stops, order);
      if (length < bestLength) {
        bestLength = length;
        best = [...order];
      }
      return;
    }
    for (let i = 0; i < n; i++) {
      if (used.has(i)) continue;
      used.add(i);
      order.push(i);
      walk();
      order.pop();
      used.delete(i);
    }
  };
  walk();
  return { order: best, length: bestLength };
};

export const generateTour = (day: string): TourPuzzle => {
  const rand = mulberry32(dailySeed(day));
  const grid = 8;
  const cells = Array.from({ length: grid * grid }, (_, i) => i).sort(() => rand() - 0.5);
  const depot: Stop = { name: 'depot', row: 0, col: 0 };
  const names = [...STOP_NAMES].sort(() => rand() - 0.5);
  const stops = names.map((name, i) => {
    const cell = cells[i] ?? 0;
    return { name, row: Math.floor(cell / grid), col: cell % grid };
  });
  const { length } = optimalRoute(depot, stops);
  return { day, depot, stops, grid, optimalLength: length };
};

export const routeScore = (puzzle: TourPuzzle, order: number[]): number => {
  const length = routeLength(puzzle.depot, puzzle.stops, order);
  return Math.round((puzzle.optimalLength / length) * 100);
};
