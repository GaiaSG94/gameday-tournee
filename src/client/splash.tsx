import './index.css';

import { context, requestExpandedMode } from '@devvit/web/client';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

export const Splash = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-3 bg-[#f5efe3] px-6 text-center text-[#3b3227]">
      <div className="text-3xl">🚚</div>
      <h1 className="text-3xl font-black tracking-[0.25em] text-[#c2410c]">TOURNEE</h1>
      <p className="max-w-[240px] text-[13px] leading-snug text-[#6f6152]">
        Six stops, one van, one shift. Shortest route wins. Hi {context.username ?? 'driver'}.
      </p>
      <button
        onClick={(e) => requestExpandedMode(e.nativeEvent, 'game')}
        className="mt-2 rounded-full bg-[#c2410c] px-8 py-2.5 text-sm font-black uppercase tracking-widest text-white transition-transform active:scale-[0.98]"
      >
        Start the round
      </button>
    </div>
  );
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Splash />
  </StrictMode>
);
