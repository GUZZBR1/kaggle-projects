# Public opponent registry

This repository keeps a small, pinned set of external Kaggriculture opponents
for robust family-level comparison.

| ID | Family | Version | Commit | License | main.py SHA256 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| `cok_v10` | `public_adaptive_livestock_routes` | `v10` | `7ef67eac458cd9ecd13786063e2e581fbe7403ec` | Apache-2.0 | `1c7335f698692f1c7bac34913a9ededc0f736dfb2b51346a4fa59098ab471d01` | https://github.com/COK-ZhangZiliang/Kaggriculture |
| `seyamalam_v21` | `route_market_recovery` | `v21` | `8b8c421eb10634c756583ce10c75189f50c83a72` | MIT | `0cd14b653102d276c4f902fa3b8c6bd81d869b8ab64c422cb881b9d2346ec639` | https://github.com/Seyamalam/Kaggriculture |
| `lonespear_v11` | `standing_on_work_livestock` | `v11` | `774b26093ccf4246525517d48420349b841b6e50` | MIT | `eb5b5f59a8ec2d40b77cc99d4ffe3b932136fdcf9f6b6e168726b7f07ab47cb0` | https://github.com/lonespear/kaggriculture |

Captured on 2026-09-07. All three snapshots are compatible with the pinned
`kaggle-environments==1.32.7` interpreter used by this repository.

For `cok_v10`, the upstream/pre-normalization hash retained in the manifest is
`56831f3c43c9727d90016b7a7a8d4eb51d1a4c08c1120d58f061d9176e8bc109`.

The intended use is comparative evaluation only; they are not promoted as the
project's own strategy.

## Public Kaggle notebooks

Added 2026-09-08 so the ladder round-robin in `docs/LADDER_META.md` is reproducible.
These are agents published in public competition notebooks, extracted verbatim from the
notebook cell that writes `main.py`. The hosts have stated that public notebooks and
public replays are fair use for building and informing a submission (forum topics
#737788 and #738837). They are benchmark opponents only.

| ID | Family | Version | Kernel | main.py SHA256 |
| --- | --- | --- | --- | --- |
| `thomas_t95` | `public_state_schedule_portfolio` | `v5/2` | [thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing](https://www.kaggle.com/code/thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing) | `8241246765098c50223d897739cb32076b71a303284d2e5e1c5f0fb495bb5a97` |
| `thomas_t93` | `public_state_schedule_portfolio` | `v6day` | [thomastschinkel/kaggriculture-93-8-win-rate-public-state-router](https://www.kaggle.com/code/thomastschinkel/kaggriculture-93-8-win-rate-public-state-router) | `b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522` |
| `kaitofukami_v48` | `fast_route_early_floor` | `v48` | [kaitofukami/40-40-early-floor-39-46-top-10-v48-fast-routes](https://www.kaggle.com/code/kaitofukami/40-40-early-floor-39-46-top-10-v48-fast-routes) | `dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a` |
| `boatlee_v16` | `premium_market_lead` | `V16-RC5` | [boatlee/v16-rc5-high-score-8c-4s-premium-market-lead](https://www.kaggle.com/code/boatlee/v16-rc5-high-score-8c-4s-premium-market-lead) | `f029fa0cb66a9eb509afbe44e3f59b800332d0419db91607183410e4089c4d19` |
| `boatlee_v21` | `public_state_route_portfolio` | `V21-R1` | [boatlee/v21-r1-public-state-route-portfolio](https://www.kaggle.com/code/boatlee/v21-r1-public-state-route-portfolio) | `c6f96a8521dc9aa369b6f27e5b36b9d481e5c1688f50c8ca215c3bb53f1f9eb8` |
| `yhay_router_0908` | `native_solver_tape_router` | `0908` | [yhay81/shop-router-0908](https://www.kaggle.com/code/yhay81/shop-router-0908) | `66585d1a5dbfe11c946a3c400278592f860342bc4a8f5e5f87f2a9293348984b` |

`yhay_router_0908` is a bundle, not a single file: `main.py` plus `observation.py`,
`model.json` and `actions.json`, extracted verbatim from the base64 `tar.gz` the
notebook writes. Per-file hashes are in its manifest, together with the SHA-256 of the
notebook blob itself. Its four tapes are the output of the author's own native policy,
not a harvest of someone else's replay, which is what `docs/YHAY_ROUTER_FINDING.md`
measures.

## Varredura de 2026-09-08 (issue #35)

Adicionados pela varredura descrita em `docs/PANEL_REFRESH.md`: notebooks públicos cujo
time do autor está acima de 2 300 no leaderboard e cujo agente é extraível verbatim.
Extração por `scripts/pin_notebook_agent.py`, rating em `opponents/ratings.json`.

| ID | Family | Kernel | main.py SHA256 |
| --- | --- | --- | --- |
| `aberatozer_d5e3` | `reactive_chassis_over_public_tapes` | [ahmedberatozer/notebookd5e3d21fa6](https://www.kaggle.com/code/ahmedberatozer/notebookd5e3d21fa6) | `d5e3ab887e3385db76d06a96b8b2a16648fc59354b679f2faed626847b6ec7d9` |
| `yamakawanin_king_v4e` | `adaptive_public_state_multi_route` | [yamakawanin/king-v4e-rc4](https://www.kaggle.com/code/yamakawanin/king-v4e-rc4) | `26ffba5273e4432dbc4ec822d5a65b09d3e9f1473c3ce813c528812eeb45779d` |
| `lynnsakurai_v4` | `farming_score_shop_selection` | [lynnsakurai/farming-score-v4-a-better-shop](https://www.kaggle.com/code/lynnsakurai/farming-score-v4-a-better-shop) | `1590394cf30c8989a3e1cfdb027d89b5ccd97c2fb4cdc14959a15555b2b2361a` |
| `reyhanksatria_v1` | `adaptive_shop_guard` | [reyhanksatria/strong-adaptive-agent-v1](https://www.kaggle.com/code/reyhanksatria/strong-adaptive-agent-v1) | `6c0fe2d59557b2874b8df35245e36723f80662b624ac8fd5e3060596830f58f9` |
