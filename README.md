# Tournee

A daily routing puzzle for Reddit, built on [Devvit Web](https://developers.reddit.com/).

Six stops scattered on an 8x8 street grid, one van, one shift. Tap the stops in the
order you will drive them; the route is scored against the shortest possible
tour (manhattan distance, return to the depot). A perfect route extends your
streak.

## How to play

1. Tap stops in the order you will visit them (Undo to step back).
2. Tap Send route.
3. A perfect (shortest) route gives 100% and extends the streak.

One delivery round per day, the same for everyone; the optimal route is computed
server-side (720 permutations) and streaks are stored per user in Redis.

## Stack

- React 19 + Tailwind 4 + Vite (client inside a Reddit post)
- Hono server on Devvit (`/api/init`, `/api/submit`), Redis persistence
- Deterministic daily generation (UTC seed), unit-tested

## Development

```bash
npm install
npm run dev
npm test
npm run type-check
npm run build
```

## Submission (Reddit's Game of the Day Hackathon)

- App listing: `developers.reddit.com/apps/gameday-tournee` (private until judging ends)
- Demo post: public test subreddit, post running the game
