import './index.css';

import { useCallback, useEffect, useState } from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import type { Stop } from '../shared/puzzle';

type Init = {
  day: string;
  username: string;
  streak: number;
  solvedToday: boolean;
  startedAt: number;
  depot: Stop;
  stops: Stop[];
  grid: number;
};

type Result = { won: boolean; score: number; streak: number; optimal: number };

const App = () => {
  const [init, setInit] = useState<Init | null>(null);
  const [order, setOrder] = useState<number[]>([]);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [seconds, setSeconds] = useState(0);

  const load = useCallback(async () => {
    try {
      const res = await fetch('/api/init');
      const data = await res.json();
      if (data.status === 'error') throw new Error(data.message);
      setInit(data);
      setOrder([]);
      setResult(null);
      setSeconds(0);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'load failed');
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    const timer = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  const tap = (index: number) => {
    setOrder((current) => (current.includes(index) ? current : [...current, index]));
  };

  const undo = () => setOrder((current) => current.slice(0, -1));

  const submit = async () => {
    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order, startedAt: Date.now() - seconds * 1000 }),
      });
      const data = await res.json();
      if (data.status === 'error') throw new Error(data.message);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'submit failed');
    }
  };

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#f5efe3] text-[#3b3227]">
        <p>{error}</p>
      </div>
    );
  }
  if (!init) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#f5efe3] text-[#9a8a70]">
        <p className="animate-pulse">Loading the van…</p>
      </div>
    );
  }

  const clock = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  const cell = 34;

  return (
    <div className="flex min-h-screen flex-col items-center gap-4 bg-[#f5efe3] px-4 py-6 text-[#3b3227]">
      <header className="flex w-full max-w-md items-center justify-between">
        <h1 className="text-xl font-black tracking-[0.25em] text-[#c2410c]">TOURNEE</h1>
        <div className="text-sm font-semibold text-[#9a8a70]">
          <span className="mr-3">{clock}</span>
          <span>🔥 {result ? result.streak : init.streak}</span>
        </div>
      </header>
      <p className="max-w-md text-center text-[13px] leading-snug text-[#6f6152]">
        Six stops, one van, one shift. Tap the stops in the order you will drive them, then
        send the route. The shortest route wins the day.
      </p>
      <div
        className="relative rounded-xl border-2 border-[#d8c9ae] bg-[#efe5d1]"
        style={{ width: init.grid * cell + 8, height: init.grid * cell + 8 }}
      >
        <span
          className="absolute flex h-6 w-6 items-center justify-center rounded-full bg-[#3b3227] text-[11px] font-black text-[#f5efe3]"
          style={{ top: init.depot.row * cell + 4, left: init.depot.col * cell + 4 }}
        >
          D
        </span>
        {init.stops.map((stop, i) => {
          const step = order.indexOf(i);
          return (
            <button
              key={stop.name}
              onClick={() => tap(i)}
              className={`absolute flex h-6 w-6 items-center justify-center rounded-full border-2 text-[11px] font-black ${
                step >= 0
                  ? 'border-[#c2410c] bg-[#c2410c] text-white'
                  : 'border-[#3b3227] bg-[#f5efe3] text-[#3b3227]'
              }`}
              style={{ top: stop.row * cell + 4, left: stop.col * cell + 4 }}
              aria-label={stop.name}
            >
              {step >= 0 ? step + 1 : '·'}
            </button>
          );
        })}
      </div>
      <ul className="w-full max-w-md rounded-xl border-2 border-[#d8c9ae] bg-[#efe5d1] p-4 text-[13px]">
        {order.length === 0 ? (
          <li className="text-[#9a8a70]">No stop selected yet.</li>
        ) : (
          order.map((stop, i) => (
            <li key={stop} className="font-bold">
              {i + 1}. {init.stops[stop]?.name ?? ''}
            </li>
          ))
        )}
      </ul>
      {!result ? (
        <div className="flex w-full max-w-md gap-2">
          <button
            onClick={undo}
            disabled={order.length === 0}
            className="w-28 rounded-full border-2 border-[#c2410c] py-3 text-sm font-black uppercase tracking-widest text-[#c2410c] disabled:opacity-40"
          >
            Undo
          </button>
          <button
            onClick={() => void submit()}
            disabled={order.length < init.stops.length}
            className="flex-1 rounded-full bg-[#c2410c] py-3 text-base font-black uppercase tracking-widest text-white transition-transform active:scale-[0.98] disabled:opacity-40"
          >
            Send route ({order.length}/{init.stops.length})
          </button>
        </div>
      ) : (
        <div className="flex w-full max-w-md flex-col items-center gap-3 rounded-xl border-2 border-[#d8c9ae] bg-[#efe5d1] p-5 text-center">
          <p className="text-2xl font-black tracking-widest">
            {result.won ? 'PERFECT ROUTE' : `ROUTE ${result.score}%`}
          </p>
          <p className="text-sm text-[#6f6152]">
            {result.won
              ? `Shortest possible route in ${clock} — streak 🔥 ${result.streak}.`
              : `The best route today is ${result.optimal} steps. Try a shorter one tomorrow.`}
          </p>
          <button
            onClick={() => setResult(null)}
            className="rounded-full border-2 border-[#c2410c] px-6 py-2 text-sm font-bold uppercase tracking-widest text-[#c2410c]"
          >
            Back to the map
          </button>
        </div>
      )}
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
