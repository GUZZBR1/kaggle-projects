# Kaggriculture v23 attribution

Apache-2.0 public sources:
- thomastschinkel: five production schedules and public-state routing.
  https://www.kaggle.com/code/thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing
- yhay81: readable tape runtime, sell-lead and budget/terminal guard ideas.
  https://www.kaggle.com/code/yhay81/fieldbook-commit-for-three-days
- tetsutani: weed repair, room guard, sale clamp and dead-stock ideas.
  https://www.kaggle.com/code/tetsutani/shape-the-shop-work-the-pasture-kaggriculture
- destbreso/nikital7: offline C++ simulator; not shipped in the agent.
  https://github.com/destbreso/kaggriculture-cppsim

Local v23 changes: audited Python chassis, corrected sell-lead accounting,
sequential BUY/SELL stock accounting, preserved empty market slots,
per-seat public-state routing and exception fallbacks.
The Apache-2.0 license is embedded in main.py.

Local evaluation: top 106W/14L, opp 145W/5L, reactive arena 104W/4L.
Live Kaggle rating >=2800 has not yet been verified.
