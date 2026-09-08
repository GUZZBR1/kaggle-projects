# SPDX-License-Identifier: Apache-2.0
# v23 modifications: public production router, audited Python chassis, and build tooling.
# Credits: thomastschinkel, yhay81, tetsutani; offline simulator: destbreso/nikital7.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent


# Donor stream: thomastschinkel (Apache-2.0); runtime ideas: yhay81;
# offline engine: destbreso/nikital7 kagsim (Apache-2.0). See v23 attribution.
import base64
import json
import zlib

_PAYLOAD = json.loads(zlib.decompress(base64.b85decode('c-rK>+pZ+XvLyB|eC~(Jd#2uclQrDLaI*<sv@jYF8%NR+1`tLN&dl3D|E}(}GHX>un46hLR+9%3U${_R7mvuexSN}s|Br9}*MIqM|N71U^q>F7H~+`K{M&#1*MIx`=Qlrp{Povw{`m0CfBBdH>wo`mpI`X==YRc|fBQfG^}m1q`#*p4x8MKMKY#w^(|5mr``b4kzIplk_2cLNcf%il{68P=zvQP+zx?+1_*;Ix{`lkj$JakTynXSn*XwuhFE3wS{`(KVT)%Pu`0^befBNAcAHRJ0x1V0V`OsG{|N8gq_2)1DP+0tO{q?tdgFjEi58wXB-+$h}>C5-*Z+Rcx-Aj*eW~1%&FTa2P?Q7r6e*E$Gzy9|74?lkQ&(BZpx8J`^h4IMx?aSvLEqi+nKjGpL{p0%Mr=P%Be*W>}Pru#%{b5jrjrW6l`;o^Xfsudy@^7zrit!j%Fvhi-{*S+1e<_~){SV;>4{ZPTqdWH#uxm1BxLz%9zxx5saPc_qhVu4@W9<N}9nP<Z_pP(f_WOfA9!b5^9D7G#?`S;r_uu*tUk3FsTlLi1_H;{a&)aMD{8gvY^<#A^Rgd)c{K<?KpK{Cwo2Of~eett<nAo>>J<X1N4$$%fW)w5#SkVJ3dh;QcH!6CFcPGpKZ|?`o{d3Je#S5_e(tOmsKU{FKpa)++X1#!JClvU?>aThZzVgGU-(9>%S@g7NuKqeZ&HJ0~7u@S)k?)OX^L@r{UmH*6-7D2E{z-HAW@T=uZ?C{9y!~6t6h3~I%+s^J|8BCLYj^Mm``Xg63PK1O59k$gEth-k&4WFyA|2=(g4+ljV8vJOx8>b8-|kOzBEJ12`M&y+B(CH8_tt)G`MsZh{PFtjZ~y!c*I$17;m05Tm(sC<|4yAN^oi8zc6dP1Pu|w!ub+OeuaW(}y!-Hb090MERqVTerEo@$cVSyk*fRnjyq*i=@!ZaYcT<tSlrqk^j&Ex+8EnZfe!t${kN*=F-FLry`uXw9zwOR5XXo9hpK%mF`DCv*(7z+&{(Vo~b6tb~KN;8JMLhT09?zf8N2~xgtHaPmFCP)m=@01<5GSTSto@+b^H(aE<&UIi0Allug9Lmp`i(kHswbGlo|cXEBv<w%V>vacAR1vXn)H*=y_qnVtXc4|PAytwpZq>Go6J}_c;E}(c~i9?^7oIw{LjkbdO~kc2s|o+PRN->rrs=k%36K@g$IAQ2zK=@V>o2nvISoA!?_O^#BKiJbA;E!h!a;elKz;D;&!w=esGwgo#j7!^o0x@)(Ff)T87)n0zA3yiLYQRoUiJ74DEnO($`1<CjR;DxG>hepq-DDdy}|<Y^MhORsQt(4b<kBc-JyGI$K;GZub3^Vtl)Or6B7;cBKV8$Jb$f3_15XJ9tBLS(YOA)WIZ?DNH?f<bT4MGY)C-)Pd*2Jc=gIjk#IX&z}8ifNHckEkkfP)xX5NX6U;NrtcyF;sf$~e`N8}$qiq6n`o`qo=6bc`v5z1bRW@|WRjt9a6SOSlK%th3EjTwhI(31dV{Cc^1WsX?Sa!%j40uPO{ZKi<as^5{CSps`GgV+e?I#2HJqZ*_sZ`#uq{CLKy!%piU0MtUp~J4?fT0v{|Wq7J^Ak&&*mqjJytNBlqcrin&4W{-_D4OaQaWdZ|JUd+$%Dvzy--6CN6eVJ0LvimUA9}-&w93hboj=@wZh{U7x1`ruWwZ5XH0J_Brn9DJW-5={?RVMFQ#22Yb%*LO#M%Zfo!Rp7p5C4Fiw^$oHL?fAT{&uPFii09Sr$hm|<?DEZ#^SL5)<pNe=*&rG(}-q+ZUdr{|4Z_YZY_-uy`(1pCQlzz$w-%qm7-IL%L;KAc7_2lnlU6RCCCm+}o{XXPYR(DcM)<trOo<(29=pjH7Gl_+0y55OByDxCJ1IWvCgq%3#>@*hr5a8B1O3+v1CyRohME2E8I)O3hiywS9a9}|`(^)d0exxjJh!;jKhe|4bkpCPl#%q2=ayK_U^LjHgV6`N5wI<tRU(fk!QY2P6ROpvto*{S4z&X$-+^^d2OpN&}5xmRgd?JhK_;-DPuAMz<8Oa+w_u8qg-j;N3UEALe8{&Kp!hS%JkB!&cvM#Wze^S1O{3IMRsFSOH6p@eZU$xyK@a1=O`|M{7$L8hJryt)6zcfc4jXb1(2y@;eiJJjw!Z<q#_ka6*<9$~bfPeq#)34XNcfEf%g=?6vSzlB&`8#@#6Y{>9jJFEIYHKiy{P=0gepsOcQMGbx_hzf5?oXlbvDTJ>QZ+EyES_*7qPI$yZ$G`>%5a6%wJ;B#ftlinFPAzZ*wTAo8a%u^C_0C=H!%m~nbkLSynb7gfoELrFjYMi7uw%{^;7c4$^$1AT(rW|hB^Bdd<;1BIcB;1O%(amgcukD2|kdY{;939gaa4{G6RaBfUS=I*^%~AC%<&y>*8)z@~aUv(cfS^sd}ow$_%T5Lzti?crUBzEGmw9qwjlm%ftu3Jr8I^&Las~OHGdv9-F<R;Bwf3pBtEG`vH4Lxm(8k;2-zT415`ekV$$V56Gx+R$;wC8+%b<YhVfu&2w)*LuUqhGI81V^D{lSyWsY3w?9Jo{~0NT_g}&H!tIUkf2c6vd6D<MFNj>c=wtY089|%C&iN2kg;W(a5D+-xn5W_R6B(6Y<|x4=_{<5jhvtKb)$!jLh9ZiHS;WuanA9;_v=tbzaIRW`rJdQYa@Vk7c4`L!X#j+KgeN@C5#?U4#_R_Z(!yDzb7ArKnzOhb@4eVX-b@+KfQ`Eb(h~k_OR*iPvi0`^Sf4DwZ(9iLN6;iS=qRzs6vRjb?rO+sQ4U8uv1e0hb;uW!+ny$E0Ro_Rhv@c7=<9q{399-J0A~0<=?Ty_=`=LPTy2TD31tsQAL>tzBa0N&u?3}DK{zFmC)w|YfBf*{fBfddjN=bVFvExI<CpSl<+gU--rx1rR053J$YGTN#htBO%+yJcd-JXe3ZSTLN~TStbubd_0G59o!Q0%?Tq;fDG{p8`ZGoRSZ-_f>cEX@mgasCvJ13=nVwVL~kvWnBM))WvBiVV5wj~KmNy6yq1FsxzTZ#?Q0xhLU#$QifsQhs<sLqTYpIbKt>5o^ZOxTmuaOamGLJ#3dxwEdBJe{x9;Yic~_b!4$ZOPX5<rtR%<9m{6_as^1Vy$_caFEJV=Yjt?f#b(AjSOt3L6%j39_6LM5$WN|a39e1@NBiJtA#W12|F#t6ej&bDqNsv3O7Vra5W{XN<9RXkf3CMgzk?NjFO3R0tIl&ce?H?xi;Rb{@Fw)bftY;CDa|3b6a`P52q=|u-r=%hTry<Sp)`Afn-@4;zo8V@$|vVz!Q0Sa;Mksv^S(ym#EHv*1z{2hScG5Lroq?Op2^0FiG$jQ{53-=B+jR+5A_Y0%DPNY4)8bJTj%|Lr8M=S170@vO?vU+m+<b5;X0Od?=Fawq(PJm^_!Ur%4R(Qid1@@+pi%gTfvfCq9z-S4Om7H5OT41r9v@J|Er+Wl2p3?tO5_=uwXOTTS(-?QtceWZHQZQe;qPjlKpk9%*sVHA<{GF>@SbsTt6KJd$wV;c~C5JK$>f7nxs7L>7M-sfo>iiXlV2xkff^ewBMG%jJGJVIw8{0V7Ctjh~QY<cB%}RP#yas>K#c7usW$I;ulE)0rCy=5PzESdvw4?7>oQ!r<DP{zw#ow*<otHf1}n2J!JzV&JE=UeeOMGIu7(#$H|E&_t2W4dX;u4{z1!B(2;1tB&b24F-~avildJi=g>Ep@;^31fGg?*>k};e}9pep=t_th*VOL&Cz?Ax{B1CbIvZ3#R95uG*IKExy|Z(mW9-j25)0bTu0%MxfVk4ge&3-;Ad~fID<LHjG4Rl;|(|RGkJ<==I`GODR#hKi)nuU0rXl_N?ds3Eah>uDUGGrCKrT7m@_aM?HN9Fg4`;Q(inQzXTbCK!sFUw#m|?x7<J7G)fe&?a`eoG77k!gdi6dNmJqE0*WJrpJx(Z}g{J<8V324WtTClLsA@2OpR^WV3Sa(@b-uSM{i+o=-ho6Q7FBeK+8$Ow+48X1b!4{l1wnKuXz{d%5-BEdWfLFR36Bk%y84AR3XW+Ykx`5VPzz%czA*xe;40bNv4X<;h)6GEOhU8onENS8k<b|fNmK{}L1zX-KF&stvtMCDHD%wL+hF$UlvCYDxP)tlKN{MAJD>-HNI>0az6Wdz27|516^fn{MXMa9Ai>z-s)XuwM+0qpGUUU3Wd|D}htzPca31SNl|+2AIF~096iZbqmr(2ok^gEQLwlBngufi<xE(Gaqht?R=DHXQfbdYj(T!5rhCS{)vO*S|=jViOk##9Pr<f;Z?}lOz&Ib7C=Vb%aN&Rh9FBeokG$kpmh8G~0)Uf<xV6(B%*xqky*-?52mjP*=W)McmrJ|*?#5M>Of*QeXsh~{R+)~^su2z2%(*}eW@?c^;*g)d9sp}Whkme0WfCV)*&@EJX`YaPBKL|UNz2u|bDWA(a(xWaBp0H|f-mvh@0mMq<t;z>h(_+$Znz<@kKvw7=#y0_4cd2Gftd(Zi&k}FYY)>Uxt<{$Dp`-%M+^7#Jm+g`44@JZPYYN4S?1%+ZR?gF>GJK)pyI30R8c9ercq<dw#x4=HCyU3xHT@DjA?aiSL@9k`locvT>3j$HN!FDl9(9@`v;74W8A}LaN?-$|$il73>V{lWgq1E@#UBm%c)<+5hB^0!>JC;HDQ|h(9dI5O)qNk6n)Ky|ZGsN3WG)!$8Tl|Kf=(+q68wF*l<U=0?yWwdp^#~ocxG)SsL6y4knXRb78ZR{iq_*7U?NbhK6YsG$H;8fuTaK-3z60K8O$(_$eim;ZZA69AEyO3%@L^IzQ`l>6UKU?*U^hpK~vvF&w@r6LD_z=pjy(Z*!SC5(X3e;N`Q}(re<3Tw!>P}j?{c+_6V>DIOoyfgl9DYJup?AIx)=>>j)%lsy(rn5lHV)B8YM2)SLogLt;(G$!A9aURuiPDe4eWC+(k>hd)~<@zj2@BTlJre{mpqvX;QeuV>Ay(L;-ZN#a3$7?^Foz?DmNOF};Ob6cT;<A}<>m|lNlejGvQ(t&fCr|0gKIJ+nre6fqySP#z-eyjmUP{Br|-`6!FU^(WsnPu~>wS~w;8zwjUT(w5lY^jC#i>l#&j+`kj)&Ycql$v!WNX-a>5HFljY7&5j4q{y`JTF>R#Zob;IHiw=pi*#CFvs3-wo^)FEYV4ew(Iqmm>St<#P9N6AKE@bmYBJEy>X?@wjSx%yrcnHWdvP@w-}Qqljj^+T2u~&U0QYe?dz{Gs&s<bF)?G?C>S6C8*(nBPhe-LEzO0NIFlZlEF7)>Xqi8uuG1EN8o}=oXhp(+e|`25IJ^+c3OU@9YB1<mVxu7ZLNwNSXSh0=uGQXY+(7xwqB#0oCO{Cp!4VXh1FAdUS@U=QSY@^-<3521q(TkmW!GhOrD*@TIVZw^xM(k)%^D9Obv419-litka1%4{?sB?w5Xk~EVO3&N<Z)*s55t;e-5EqC|HWN2=-)HeCt--h8or*<mWvhw+WAzH9D(j&fb~*s&bG0L1=M6P`6aR{6F`><z+u6Ov+FOh+!BHetY<FJxO(EkQ=J67s)$rCHGAbTJ$A`~fLp5tVI}!-FcXwonx#mehFfWvgQ*)P6Fa%gn!stc7h?SEDN8RD{8NJNVK~{yF<=txqPd%ohqbjxCl$hUDO$*|Ms2+A>2(NC%k5)WEEPl}8jh<SpIDJhLh}@@7yKAph;~`^2_AR89ooqra9!LByig^ylf0p7%G>+YMHdC(L4bGt{`;cH{LNYJ;u(m-@t{uKQT$<pucRpnoC#&GNCva<(gfh#`$=a$T%pi)E^!HAT_%7;3Be|Lr&vMbxd7Kk@4;z}AOGXf`s{%E#_0Ec+{SQd4_q(=Q3S__Kq&Qy8D9IaJk%1)T{Fk+MHFX$4Bf8}v~;>8g+9k=wClmZ@&<UycRzeD*uhFsgJUJ6>Bk-Bm0IYQZ|Bu*w-NwInCi87!wF+2Tj$0=WF51bRMLF)$wANKQ&)=^-b|V5;l|u7eozM5<JBa)6|x?^Jy;!NavYj{PAD+ilPtDb{%DH3!0z)>GA%`9ez-+h1{AFzn06}&M-Q5`L>1hH_b-ATU=Eqc6fgBup*?OXQ&508vNiw%dz2nC%ev^uHuE!CjED$q<&Kc|=wAcK`{3_wEi8XLn}(tCFd{#~4?$hdHEHq#ggx4+7&(1`^zHbkV<l_Cr-YFyp%o+mlmJ+W7x(?Kb}yQ@R*Qan8fbD!%oQ3?IC>fc!E#sH;rN<wNW{v+6EHs!d@pZ;EajSUt3zr1xaKrY^PHYIzv!~nQ?Mpg1?{4h0_{4%xk*;<h34J~z#OYK;O>w6*vQu!z)Io7>sMuQtnkGtC~noDNuXVcv|k!IBlr56Rk^?z2hHRwsN^N%q|*6DjgYGbl4Va^;A0t-Z#bvbcRS&LXg*jYAPr0$0uVMRjV2;6N{YyU!4}MWINxSdQaJN4I0RWw)iowUz)j3OXcqQjoQrH1SQSQe`L{)q0qA5m2xdHusCQ&a)|<4C%EPi0k4g}m42qD|qlu)jR1F5lN{ouH`!liV1wa{kUj3?7K*7S>!n~&GHGK(E9hMQKq56{sq?-Z7Z1!iSXpJg?(yFhk!7t;|&Ly9DPxp_^q3_1zl}&+h%1#lD(_)6Q$yEQ-QID;W{9ms?)O9l`H#woP|3(P8#K6P{g8JU&ikrJcT3i-Ufx<dblkhcP?ZC2xeEU&w#*Y*k3xpvpg11ZjrsoQVd43JQbG&Gv6>RY#6b`H>vP|r{j#6!0(GDhgqQ8Z^Znsd=rR4}!V_IA+1IEPOn(#Kib9%jR;e2OQ-gx%-?VuWS&;_h9D8Yd{O3C9gXi$7hCArQN>)@!<_t;D^kyZr{mMTWupYb9hDbr`D)d)$G`?<jfgj(PkWr{3HM7t>PP%kA0;cUzyL9;WLBY?vMxz0~0lY{vs27)36P>mFwBK0)T<2faRC|AUVFF6BM1{$o|dVX`k>q)iQDlEK51!l!&V6Hfh%=s>Q{P6^#51gE|DihOnL4QMYCqc;P;;UiszgRko$xLCW=h9w?qCBHo6a$I>*eR=)@)W_vpcurB{G^B)w>J_+f16?JOBenXsu8uk3`%TVB`zTpwIS-7K`wes%8>Yk$JZD$O~SnMz8u`x4iltEr}h4)Q82wzNktCW@93*ab%hg@4Z^~t-n}BB0GbRu|DNJ1P@$%%MqaUG+f?znz7=pnTYIs=zInB0dCu>KbP`>w!_Y~l3T4Xz-r{bqWQQJxs0dW+njhM|S6DPR&O8rwP+N2*mH5D`XyE@S>7U165SoVx(o3fFk54WK)1V@TU4jSC&D@mNo`j{EKnhw?%N+yXdd_QIJG=r}c+TkAj2a$p%=7AZv{o-(>vnz=ESLm6^M#UA__64CCrm!N2{T4lxKpK-*p-}$mNVDaJ7sO2Os;0j(eQGm1>FIS4xPl7qyu-KcOSgE>*}MyA{o`*ZwVWC{b0n#!xEnc5YN#9|6rlcBCc@`2@pi%I-?3L99^M8(C6G)Kg5V<Ds@J}<ut0(u|`2jQ<!Ym@WK?ifoic3zMh)<Khu!rr2fcXfzufBBP=eqD`qmZh75kQ0-y{sP8#u>5A9%x)7YYR^%$`)d=iZfuxTL$Ck+izCQpiFw(=@yc`Z$b=1}Pt!-FE+rb22u6y8|TH<(J1D78MGCnd|4#!vZ912lUiBTvk<U{ZFDFh+J^AYBhaXR=upsc5#P!I%oH+BgHD5YGwcjV+u4`v_Z`hGlIh%K%g*oQ(k2S@Z~`bSe+qcmcs;N6Q#xbp%xBGx;<=l<cJkm#4z7k&xommro4U7n^ZDe~CbdPC!&Xgsql|rC>v|+_ktGab230gipU9Qn9Ke;%cmbDtW075U?;aD#m_Uv8Tm!M*j%G;aEBB>d3<AypFDuax~9trSqx|lKA}iIP!$E?NUrBUcqW6dCeaY+`an-ND*u4CK)o6Y=IEgVX5I(a$N$-Y69bo`*X%pRl&^oh)L1thq-M}9VF)Kz~xpGc7*V8s>$oWYZeZ3eIw*Y!aE!o==1mvm6{zZIOk1$_ABE#7Jtc@02Vkn4YwecmP$KPPOzzQNltdZ^hjj@qBKqI52}t9>OgNWURJ*QBI!Z86bGd?NYzsLWpZ6zWk5~qGR5Emj!3;HW1@wdZDhEWDFiJC((C*MEuR36NCwI}q+U(o-zaG*c5fhVWN3ZjU33=dVp+k)=FwpunMD$mx}=bfyWe?6qP{-%RYJeMqFiBSpT&a^`=Dw`rRW**b4@p*bi_&8YJpnyjWhy{*vrkC_-L8Kz0N~Cew&=p)=@xoQVoHXYG*VX>IF|btI+x`za4fcCfdC4C1vL7l+fr(dr3fFv+KBFCSzg^7m0~{52{kqUS{J^)n0VfcATEeprdS|Go>(ws({NMBSYk|q*grbi{}X58Lm3>KTm{B4tu95qM!vkl6l)e>%l69ky>fp8(4W$d=JMZUI{YQUk~|cxtLM6oiXv781`_~Qv&`@*FTZK)47_0?3ATijReFYulUvYT&DwshGyeR8o>MJ5pi+DHBP9VWG#0T*D}I0X<7~!j*AD;Scok`I?AgLMT%L-nuI_C;C1}t?0P3IDR76GT1-MQ(_klM_CbPo>RjcPJmJ&#h5HwA?p}1k*V*lX-GxYjS)^LYK+hlP&|gHpsMoyUoXmAvs>Ml!Cg?C$+}NzqMCB}2E$<0HDX)@4pEO(8O~6@I^;~OmwrX=tRo28sp`Q?!<UnXWSDkX(yfph_j8^4^kPX6EDL04ooesk41WB2avD@@o`8508P^eTALx+6jnInT;6J}6UJ_|`FR>k7USB41)9gZ99i#iQlTTDA~u?GTf*c8u4C4E6ZVMg{2TESJ1%Axhnxn4kOg)3eUmyn85BVgI(cvf-aX2{wBc#FpN__Y6jMj<EG!*RJe41>?qS4H%j7_xadRMzKHb^45^PT?JJF(Iy>VY7B*CSy#IjY#&Ep8HH6H&Ob*2t}kQ)K>3MK?3#IPr&AJj!RYD(q*E0N*AGS3R&ZN=`2#BjyeU<4btX^Jd;Q0G_;heGaV<|z?_9(*@5<d__PO=SoQL$qM7+C_a{%hb;V2MHuh68i4u3eBFU#5nqrR{GnK7U&o&tg4lA)KoE$4HE;Tq~-5-A7$qHYP6T<|&aSTx{{nRYCRu8LvV&0T#y$#e{GSTjuiO#(6)WEHiyvxITajuxC>yW7v#{6Iw07+v(On#ahL3(BJGm|%wJ4yTr@)NPrGcJxKjm|wCEtlm(WnkLrKD3LXf})(mle2%Qt_0;X)X{gnXG`glCsKcaAp|vI@I?JFi)-@ck*$9uxId_oatt5Q(&YN>@~~(p`hdB%F(lMC(fw>Q(}z{B)z5(Zp@78j6HkGS5Ij)_1zi_)dit}OKT}4<C&lHV{j8rOom?L_06?coyK<zgWIxjG$)i2>3FNd-pm%+nxykb<m8JC<N`{DyW4YIlsYObjno4*8sY_Ed*=nj3sEdAx_nslTkkt!j8WWE3QC(g9+_QH=q-YH1SGp=uw3xDd$ftyd7${Ej=}p3SG_CryEkT)$c;;$H7ld63DR7p&h=NH=n|$3&L!*%=taxrY<0Wy>xj3nw+d0QeBWRUqBOc5gKm-<shOlK!Z#t86Bo{nNIgu$5Y&(StXVksq$|hBUyzMOU3d80`sn+Bfnk8?to@o&1;MIxp6qcrPN>gsz-+|{Uu@OcnXoyS6MTC_{7~PD~7X&L!3dxcy={@9isvH49u#T;1i$-Z`+ttGW0k284(Z-4Bj;w#=s;nF2cMN<Z`qrFU87JcK7jr0#w640tSxd*|E4AAGyncT9^raGNwd9az4XSWl!BoMaf^~L96`<!_B6`mD44ek@bQ~SDI(bP-rl?qn)LND>&ET}Rt5TIre9-Q_(;(&&=;0+LGQv8(dY}PYfl(9A$q`3BidOmY16cEE81|EBoBsutcT|PPo#hmNB^20!tBNV()c+PBBaiC3tHYXVp&$iWAF#mKW@dWOAj*QBAa+k_ziYB`e+?9>cA~;r{Z2)Cs6)kLR<w`qaID~}jX+3vjs>hNfoNt$!uRWV&0LMJ%@PU5sfIIJj7cT%xZbzE#8E|v(;ym{>uKOTmVTeRGwZxXqV&yc=H*t^@}QM!`KOAot5_T_dkY^!JKXPb9_+^oMujWn7=}0XZ7s#CMUN=HG|zEoI#21PM2DJ|xN#R$m^0g(ZFjpN#C}G@gm#re2mu(V#Q0LAJ4_}8X|ftDXB~o{uwY0J4_0Mwu8k&@D$9e@&G1-ug6jxB9*$2bP0Q5!1HBuD64g&4emJSIWI>`VFqgoR(nOtFQTV}OSSnw0_=_nzy8U;ri<r%V^5r}hWRyR=kY>t4Z5kvK0<Gl`7n0sps8f=q5Yz`JYwX32b5nOZD}+Gw`|5Mm?*o+xCF;c?55&_wy<Fp+@={hA=Q;b0GaIPF+Eq)fOPO_dHET9NBHP=TLp2VA^1|ZJ+Jl!_QR?0}E2d$^%L1vIiUQ2!Y_Jx=#LQ}L(tW<Oo{h}fsO|#yye7Kl<NBD4Th1a*N;_A4sG4Vw=J~m6*)8jIg*&2BrKdEK<<uEj+{bAeIU(m}kApPrCFM{QN;$2aE}Fa14qrsZEdVqv(UzqdQWwAO(7CxrPJ{2{h2seiD{Mfgii8^apL4B5dc5*{LuTDJY%q`q1L3*obNQGV8)UKV{<bIVI&i0OidBe-wd(Wv8!XSJF>$GK5}wlp<`jRX{^RK=$QlcB{%O6ad~xAH(`iWl-qgF{@JK&?%~GbIV+!ZIKq2~=*XMQJN|r8p8f#oi0eG*8;-51}4EOdD3Vr28(Ci)oBUz?40;_{&Qm?=A6vfO)s*9#nL_c&^mGyOWXguL1PI#cA;BnTeVL$`Gr+wzWqlyeK$W%}7I+Mj+!w;q)jmz>^{0_4`g*iI)F7n2Zq5J!6HTchT{n^{=ZH;XyNdi+QS2&fR|I>5I$><Z#2FEH@UIu%qV3bt}d+M3$D)!Q_5t8!ZEMB46G?soG)8$Knvz|N-lNqDPoO8;YFOht~LFH!DoU|x-WsVJ2vch&*8%aa_+t(_F7f_+15z?L8L{vg*4+Q!3-o^5kZP>Ai{|N~>S{CH*HK(|Wbv;FDUs9>}c@3ce0_DyiW1MFcyz8^{G%^ymXL>@TrbmI>>8or1@=jN*PtzPZD#iO2uS_G;m}!Wrh%R}aNB}-LML3WFBl}Xr#qIPIdS+{;7nfw|6ze7oJ=dHj!w#(&#Bojf)BDdHza85^ef~zVPDD!@LpAEQL^CJY*6Z45laEGlSFdP#`O4<7h|uI;&X11mm|E3#=NXaUJ64$6(NT5eeaSC&=Y$|d_8}P5SmbtFBjqL}swK!TZ*quUj6?VdJC3{Qj^CSamglwdiduA*1$SQLS?N|RZS{3x4}wQc*(s_6*SY>yU@6;71#}!VF(TRFTUY6b2op@<SzQ?aDJO3_Q>ngHL$=;`r&?-LnkNH3bB`V+7SO_{{RmX{{@l|Cbt0_HCc3CXVb}9hCn(IdM{w*e#@=WVButj(*EoZRVS^8PWSxjqYj1h+Koc8{M*nS5nS(XJrQ%4kv|Ro0863JK-TX`hg2VL8tK&qAuqLHLFAlDD>I3QGLCj=#N9G7USTkdzr};G$WN+!w>ngNSzpja11#^NiYoWQLDZu-(Az*C5*^aMFE{3{ntxuVD6>%s%$q@tJ^y+l7N(L`nqeWz-t?;F}C#0xTCk+-_)^`1MUgxkBUJa_BYv)KPaNtLAHW|u@=Bi_CLj)u%$q9CF&Wps8>Z$UiYANWb>xa$$t$b7ah~4mmypR0&cfWl4S!dgM4`6C7b+GzeL(X@2`^{>;)^euYdoz2-MQPj34B#`r|66SR+aG*}2H-m8Ev=&{mg9@w)YgZT70TDsMSilVAHVlWkLen|T89gNDtL(TRr8qyU<rsxPRFKVIkYwapuX30ejj=#itO=Z8-)8WE>G_=Ynuq{r7$d4=RDK9!Ef}+NM;Fj3Rx^7*u)}UO34MY$)H}GNr7uwoH9-jXlCQO5ZmO%PpVM`vj&x3zD-2P8X&&s_AB2Moa%3zz(S40LkQn`J#mRp@L$|)D9zolD%9p+%ywA!-LxcL+FG50h8&On7KcGEumAm#AeUL8(TgnCdyZ7Cj?OsPoP9{1iVRv54UV_FZDGrgI*baP_2;Y*Ff}(Lz)u&E(sQh;LtgST(GQ!UL1<GM)YY#an&IW^Z^6%PXrF)W|NfW%{=fZ~fBig^|M5-t<u|)={OSS8BdPE{;ZQf&>jT;M^6ig$vtNexc_@>*8*ue%9eg$`l6NrfdNpoN@DSfu$)mvmYoy9<A<XX8h{cvHiN2KoFob4be|c?Y3)a0zUm_n;_HPZA;%?)nil29SPGn$R5ef|Sy4Y8XO050qLKt^n;15nVPZZ0d?V|OQdwmf6`0=OjZs*0vpMLnq$Jf;2->=u7-_XC;adxg8?QQG4eS_AN4O{^Ecy6ZkxW@nZeYnf&{T(baYJ0`gyIUgO4u~c6UWYa?`GOn^Qt)r$H`a&B^mupu?e`yk{O+Hh*XM7)#}Yy1n}h^mT>YFlSf&ZnkL!hT&%t_l4>Ft+uj=>H)^o3R&PpzdNGL1lj2A5O`CC-2kI-3Ta|hhaXpMjwTiu+x$3!D_-mqsTpSI2Ru&Kt8rz2iZ&U|sVXPuNq2iXT<aoy+&o#1rJ=FS%3<S?5fl^^cIxi8O)dM<oHo?;5E&dGv*#^-RbQ8R#l$TEOx8jJBoTXi1K>;~}Io1W~XGEVjF|3<@NsW;k1)9t-59FK2Sj}N3WSvsU@ZdW`o1Y5isvbfnfFgGMjw;Iab>7c#ZvYHN1+L^yE91MK?@qFg*bqt%E|ATHniA05O^Z*3h9Q$uSy}X|p%O$6|9r@10$dlhtug|4(1)_YBU@YMee!I^%e?@Jd%95KRf(1W3v}(MBKc(tvs75KUaBS?k)MiF}`9i1wzw9Fc`xqxNM!$%i<*zxG!t9$R5{D<E?n9e>gXf?IHy}Tw7F$v$Xf8(W^{Q_9w6AtI7QPVSx%p)>GUdUq7HvM~gW<5J-0Ah==L}<*?rzeKnTP=cU_=LfdVrvKEs&}z$<ocI)fcZ8^|qf5ZbdJirE$b=#^6$SJqV15ErK5(Q;`-GZ6snrQ3w`K$|U;(huhK=kaA{cwkt4e(jZM^8tB2g_#M+IFENNZNT=<1LRK?Fa6A;$Jp4p=rB@p^yT?);ATi;aB85`_@^(?9Pm00>jmg>Qw=Ul}yG6y<zH_&pUoJIp0s_Bh6FpxI8}jlsgSd2I{*?7iG*c)%!&MG!wCjmTLBj{$uhXpse>Dih`!_{XhVS3Wp0b7~%@&r_fjAF0kY_NcwA?nkq6sQ8Q9z&@OZ!=x1NhpOw!o3KPUXD}?TY?a^VSBgY<<cLsRUQU?$x5rt~IYZf`w02`L)!~vsoIi1L!Xoch%nA696D;DVRQ$7#ofObY~Sk*isQKWksKcSNnRq<dlhZP>C0rDQcM3!A=#hSe4O1V)`SP#nDzAq3cv0y_8w-NN0E>YK0b0b{Z{Kaq~NrG11=Lpt(`&0W3mLnaXQ6H5kQL<6_6@EFP;@Bk;e&Sg9Z*gb#jogLw+MG@YY`ivf&l;CGd6Eb4fU6)43ptDBDNyUU3g<)zJOz0g;CI=`r%1YTh8gaSCl+9O)-?`<;PZ0*~c{L-gfN7uCkR<VD|<T04lL0MYwUXZ+U`|Y6Pl+wswZ5)M-Ams~4>R^vecxj*%vKO3B#{!t#s$8e&wGlqpO_^y2pdkSn%wDwo3>2a7mSi*J(d%TR`u`wLzEsD72tp8{_T8G`UjtW!sMVtC<%0YP*2Ct?y&`Gqx}kezOpSfiM)Vh7r_<(j+C3%fJ*Ru9jRe2g$JD76t3psy6$YH9$%I|s_kuz|vkR!nFF26Ohg#jK=capbnFwGkAigG%DQboEYQosYNpKsjNF0YsWbxUX8sid9Wk;zfLX8QJhq<BiQhj35ckv!eeDan&3C3G{wxZUn8SB~Qm+IDJ0g2Wu%B{V%0isUVDzFM!I9<>Ba8YpxO-EDl%UFfnCt)9xI4G7F6`kUcvMEyaYKBc10}m~M7lnLxU{WKMjK-}>w!@ey#S>Pmo@mDdERK~I1LLMVplUW-flh>=*7U;+9moPeG3z00tU9a;w^5a0Y2{(N+Tw=Nf^Y5WGNCc+8VB4=-sze|tB!zs*q))N<o#Q?gU3rICI8&qdl5d5oy)mS{lRYo7CPe)nRb3zkFoSN|4~;`3$CGq5*U~86rcs#_ZbJ9N|_EEExFV1+AIq8x%5XeTaGiaMmSORXAU06K7`2@2T7*Qoop=5%b*^>ueQz^DI(>l<9`?RujM1j%=BV=$;yX<YB83qs%l=ko4R5a&GpAmKb15ZMp}pFf%nyn6w#pIol0{vNzJ}wKR4-vIuT<%ebvL_V|yFHbg@T(ev#{u)?9vQEhMRx`4~2sF6v!2$tPII4PX)-FrLb?@tGpG1Appb3ibi@cCWVgj9XPTfGr1~L>~Y*3`qGH8<3FMZqF}If{fc;RU={bWAAey0~}CWn%JQ}8xmB($K*&lD^16b-l+OSEtC|5h9`q1sEdSvL&i(2Z?kD8oX}X0rNRl^TtxLjCe=V#xsoP&dlHNA;h5$E8)yBwgl|_D6-IvD<Wl+3Mh1|IBiK>j=#m5*q&%dwgV)@L$c>Q1C$*mOGLGP?5QZSVdxa}nFY@}I;`U4Rv=;IYHGIK#oDhGt8PK%~ShR-cUZYrHkqg^{?B8nGsAj}O%XU^Y7qg+z`(JOH?AuSVxVqxPc<1>%Hnb)d?q@e(Er70T5y2Z<@Tu7@B!<w8!}EBSf*_R#>o|mU<lE;tUlTJ4|DhiG`yuM_gtcfFBfNwV*1WiPM16XqMA?-W)KO<Ef@<g0ZhBm2!W7$%s(8IvjZR)|-0bq6oJK&xuR*Ri2gK|}bytBzm(y}->ZZhsQERV57BfGkY+{id)_QBmWye}BCyQ2gD|=h4)9dm~+6yM?mw};!G_-YJ*u`M-P>S<$U_hgdnz~!huf`6WO=K4M<cbZDJAmgmX+Fn3g?4jiyQG=2XY9Mm%716(yRmdog?}Whcl*ohV`g>NidD$(XwJkkbI;-2EZdnTxU4_|JP`kG56_#`u0yPY$l4;-QIO{J!s-NHyCk{JJ&p=1Y)x=g5_%`16Ovrux+d{z%V_q6K*|g0A%MCA#MC1}WeL4!2JvkB77T<{z>)#SH;Dad2L!piWb5%)lPCMss1XlV6sY19*iIrgb9PIG6!JmzH|UL@YG!aBvo6QtSWebuF{Tjfujh4Wdo_^?K7IiO>~fv;Ymtjq#m`keJxol;)p>+Zylhf&+|h-YOwEgZtXr6?jZ)a&V<%R0;eu4l$l^|**0{UG16(j9C<rgPKAG>$;9rgHQ{>v(XLvvBTvlcs*WZn~e42C!<(fHiorR<gD=TLbDz%}<gZ2q^c!i8gKV3NvDkb3Y$|6_45UQzHFs;;}I6`a~Fk}A8Ytsy?V*?kXS&6gKbeBLwL_-R{$XSqyrc|29F?q8Khk(P$0JMy>;BdL*iym6^hgd6ZU{%*v_duhE`Z3i_h3ohvij{^--w5fMwKi609Y5E>Et{k@hoa4@lmi?JVHRtB$+P~uAHGjyW8K1sJp(or$}BC54+I3-KnIE%F7w%wj(0(2CDl3UsG$&LVP##&k~-9N0(R#9JwjkZA;gkhnsIzf?pE+Xx3<*=@{lSdtZ50}wC!ciZ}xVVvkNd0E_-)acSi8iYFo}b;J(_>KP?#EA}+-A+~9cVlngwh*E%&gVXSF1468af9!5_sjwiTjJ^w0g`OVJ776yjr@VO*+`|VeV70^^Zr=S7GvKKOi8@-<zgr3}VM52IP$vzHJ6@ZrAhfb)vDXp5s2M}bC0s$=2prV6Ji6xx3q)vbzf7C|!)wOI|cf0*IVlbg|Dn{4SI$Yf4NRUn50y=Ec46NzgC5JYL6_K-iH|@m9Z{TCo4E-~fDQ#ImTUdqh8S&rx!}g&;BiFx{5>cFS;18p1tl5W^m4WNZ(xDI+sC!@YJ)6tG(C8sJ&xfoS*`&lwACP*KQQ*xKyqIw=ebZretHQZ}IhSu&z1_njY;!$lfb-L4Ry5!2C6^xk<?)i19lxK8sO=T5)_WhMT_{@RGmuj{c8wZPc)<$%vL%AGV9l}AGTXnuMWo!)4=8VCdOt)Fm#*`#*YRW4Xkwk)L@nXn`Y@c@55cWBj&@p%WGyJv2RtB_(cA5soE6bXjcZ=sGTH|Nnf+EYR{9)gfZ}W#Fey*&uaOJlZgQ*q5Ui-`Kf5+X)Sw~zar+8uQdT9Zw6B&84+m6K=zD9EGRA0w9uk*?j&4yzPu41piR{i5r2EWnP~RX=Ux)lvs|vn-=;|z^wC=KRplLX<U^A7oEn&J5<rMYlo{$cu3PV?p>Aul<KBjrHNtS3Ln6vBbA|nwn&8}Mx%8aWetM-sqf*+>EX6+|%A<@hn(O4ti05ExNOl$M&khPx!!7wSme{@c#&CdOpp?OAPt)9M__aacapRW5#Ovs_E+dcxLLhQw^@)Q(F$kH?9%z9Z28<()&hcH!haG1=TTlCuC)D6P1WeQ47`q*<A>&%1Q3y10*n2#Th%o|T(w;!WH%!kQ&M100koLqL=Y(5jn`Kbs&po@mtXP?P!Sc$Oi9&~>neNH*t8i-kK5x^Qp*yY!LgCzsp8jgXB{Sx0NTVwmO7rQ10myMUi@`G~~J1m<0J1iGloA*5uPpu`3dZnh!Y{_{Wl?Ceo@Q55;$W5YmiD`4aAGTu@qn*Rl5{<TtYRb+NP_-z|3}#<B^Ep==-aq#*zB5a8>@Q0jVN?&Y2(HGmZf*waNn=gpVeQgM2JpCJiMt5-OC-n+mv3!sc;(Zdp_hW54RTL3Y<Rd!>)`50vxr7<2G8kC59^o+haOz~uT>zn+hvQy+eKmAi=o-n;!+`^bFubM6cX*@o!#*wqrwqTG9AyoS>^Zq&{;D=hcyHeVq<j;4LQBo$#Wlsu7}l9@U}(U!>4Mf5QL=+-$qc>%|(K*;YF{CZy6oa$#O6(^LPrI)MIJte3W2vreh)SASQnhAYiF=8B5Fr+<6A&Pj28f#A)_%Ee+b|{(L^Cr<FmK-;4u_v+C-^WOQgn!MCXv{Cd0Gw*nB|0d{;~l<mQT@IV{^{8@brwL+z8>u}hOS<Vk?fxRqNVG>wOt=gb2y7$Sb+ctZJiX<wa1TVtf*rBA+0RP5|QBO+il}x&w(;wLd{l?3hP`nHZJ-!0gKVG&L5+Gw6)wIC-`51-TV<2=XQ0<7*Glt`qwMn^5gb+#4gqG^c9=n#bdVPQh9bKTam+e+`?90wjhi~CG(_%UMdT>W`Y*?pwsLl~bckcb);?|{iga%H>qMGPb6HKC3ow=i>M#ygYn&`#Dn~B$;^y92ID36_oz(UU9*mrGR@-U$pHn+uVPCYqINg4Y-bsdLkKUwFTD#jwqtSDP!YVQmNrW#rzhvTfA2P|^zr&b981}nZeYVfg!91EXshNn6{nQU2G`d{M)5)HoX(M`tz7aPfTnP3`NlJ5T(tBP~yhzNAsSG!QWt{4a2kB{dB#na=^P{3{a`?o}l8go&8qr>}AR#H8UK!c*R&<{7OErgUj6^S1QrQ*cSpsF3#eO{dmIp=R<Kk#x4V6wFz;y!Mw8j6L@R)5yr*7>Vf8`jn&=Rd+I$6?7~U<o=dg(5|H7>W3IyH_8kS6m!W0ByB0)GAWru;mNQ(LLldn;)G{#bzTO+jz;B0mJx&u<p!W!{PLf-E+5|-PeZu4|vuc1=q1CL3?pBW>L&565UaFV)WN>sW;;|xa*(BC^lUMJr{L+g$MgM=Cv0dF^5=>o>#@1BzB6WjMH<q8bJICv&tm1sGdZ`(;syQTl94X;fbdPA9u*hHKyta5!Q#kbK|(Un}TPbsMKX*Cqx&(>MnoYNQ}yKiRQdI*#Yd{o_i@UbxhhHg>#C+V`s8aa!@~#kr9s;y5U>WHaz<<I$K^&xP^Q{aP$I%oZ%@`)YOrngF<WGtyD!>Wo{D+U+{CL{)&gdcsZWTa8^Juwiy+VRoH}iT#=>rm}w2fmd9yqMCB0?uhJ8Ymlm$9Dy2>A9M3eJ(9g4V=yQsDZ*UCQL-TWW_P$2?b+R>Bs!rQ3I>d6dmU2tjbdVrLF)nmKV$+(BE;vn)eV|Ii)O?J5LC@_F+ww!HAtLrBCM)4udrbU%$y-~a(A3&SEIwICHO`%`UJEKhvS}}=ooE0sMg`$Hx>=lLW(C!;y+%GCxSBldWFCoCR}JhOWj+tD0w6m`#R*TASVuuZQ4dJh1>$D<HP*?TD=>9VED4DJP+UPST7yI|OZo$Ij}_Qva#2329_<G2a9$k($^$Au;zTA|cB-byU{VXou5sRM5-%crC)h0b91u}{u+WMEMZOo_?Y<=sg;G(y(UTPgk0J2Vr4C7^;Hvr{feJ;XiaHi`k!%U@f^H6Us4}d~%x;wnd<03lgDcVr66+ZbJ4kmZrgXHTN8QNxev$A7e=m-h4DX(6uriiJVFSzlxT<0vHE*{~Ld66=V<aTfrP5o<yM2pfw5&L`r)_3ve%7UHnt)5K*U{Zp#wzqz?>qNZ1MeN=0w$_j%O&Ml`$(H)EIPE3`cBrn56r@h-wInSI_(P|zx&PjqNdr0X-Ey|_GFl5?d%Rr5OSC^I8FQw&Aj=uWS(Q8t-al;AWB$W4LNW?JJ52y6FA}4!M2wbu*p#|o=m>Y<KY*tqi_8+l<yMPuXK*UK;9+>O!p+VNsLhV?z~qfPohv8>@F&y>m*FJlY5lgf{=+>+sgv4+Y!5@vMjD3mlDb#{nq_9i=$J!eHWzQ5D%cdqPbNjdl~MBOiNjcC^+>awBoKjp=x7`7P4NoxdITl&Lb)`F^T_1dDuQI2@;b-i8BIx)>C*WfXC3g-S|XE9P9~4KhrNIh*o}4G+!T`IJzRblxnLO-A>rzA5$k}1X)^AOw7#z_qbU6yZuU}M71np_OgTNB_$IJO8CcZw#B5Z3bp78cyZwoE!H}2OZ%asn;jXHsh6mS7O-`-C4>E>M^yb1N`EotZ%OAfLdOpQXufT>N~cJMT+P#y0kvFDuX<F|MXHaReJ~RwZPGs7QyO@90Mn&wXm4e95vfaze1)2NcLcc6R5a^F6c@DkM|G2>$`_NZCe3}b@I=gXv30`K`NVK0;}3JYjE%?<nu7UHL6WA6x~MtFg`gjl?vh82#4u*tOSQ^`m;_3$y)bYwrpw~8DYKxz;N%j6cgxl`{v(oX<ux!Zo!A**bwAIy!+&d5fWQ-<5Hs_F-ze;wx=Y5R<Jgl^_Y@OxNXBOBI(OS~l{!v;XO3yiyqG$hv&@t|rIbcu{Swl}ZgM02IJ2>$c*GO9brwY{wb)byprnMCrZypaZSB-ec3ve`Q(+n`tP!SUB}|<HfH8+Y0zEm;BXuwutecxd+vU(-TGL~#@gR|mC*TkZ7e|bw+rNb&%Q0q0N`^<)baw#XAYu+#=aAnNm=@=<@;$^1a7bJae2b}9{ee||52?k?b6ALH)vMOQHBjpOz9Wsz=`fDy!ajst?_fOhydaMAK<`*<$1Y7(8P3N*2ES$!2G?`qk^<rjbP8UFrfZmPV;K`U&a6x)-L1znkf%wn6f5{sCqHdts3A_~ATa&hoUZh#tzMZh&tHYnM8DWDWLRB@$TkXg@w-n=y<fBfOUb-aqh`j+!`>UJdwyzUuuQVQJ=zfvlkqs=FR`B*t{&O--YOL`%b_rYQQwKc%-r=v!-yO>n&+-0MSrGY$Z64lI0N1TZY_o^iJykiuX9L9U*j34$p!;m8K&o4nw-5s_ds+G4zuegGF^11mOb6v3K-i?<nc8hSrEZdfiRFB62+cp*Q!@yNxYH!17SPPgDtUu!HRU<KI(;q(<}9nz#1lLXg6eNReP-@E_qfesjMW@&c2L1%k{E)Mm65sxO%@#MC?GSDWv-`(73-6`aj%sDX1i#MAbB}f_50Er*>6bIsC&Fl$uJYr#%D7Nv6w9$b-E-Js}wKlRrKMg?E(Oji2)>>s72N@>w}18L)A21u7YKk7+OL2q8s0Om}2AdbQUs^}AIWIau%I?FNk78p(9*c5)xHOdghkuMQ$HNu68>TMa246c=@9uDE#+0)B)Vr|yKV%Lxh#8NzN@e~#mErvQ&!jOi<}K6c}qWPh37wS#|qc50|(8eN@qW-(Vb&c5Gl8>L*zNwIKHJ#qXnTt~;s0YH1_w*COEwN*@zHVpEor2$%dd4S<Rs2scR$H!)_Eo2~C)nXS;DIwrE7Xeqr*2Z4o@tv<Cdpt6!@=`y9`SOHbF{E06HoEodl1z2|;|86(hGM-c!6NiJ65vR<{^#D-!9^m5`Nk<+LdlW%ndZUO|5Plks`FSCbh`esM^TuL<uN`(3Dj!1#<)3#<Pn(tDF=pg5khda1`&ri;Yn&@R`(^tIB$DV!&@x;fQckS1?VQ4vk&F*R(&&$?^f4B9%jTxD46fHRFZi3QLfZ()l~2VLC9?Zrfw?INgQZa@r24mJDn*Wk;6iIh|z__yy+!Qoi<}>6v9LC`c+VbI@#5~OSRx5*e|q*oW+cP8+hOFaS$YkHT&7E9U9j&BlmvbYWPg@OgE}qk9i(NwTYxg)QY$wC1h%{m`Fn1brLy-g+dW2s(FTVZnHGY!5Y1tF+#lPuaeB2O4Xu3Erm9$huDH8hTDgAHpZ8ESdB(z3TdPJG&34DsV-(JEaYR+<+{kr75ISwk+}N<i-b5JL2cgZOW#T-fcBYBi<!89(2<X>1c~4Z5JC_s&Bqs-cp;b=cnq?_(qWmz5(j6gHS3U&?EsITsqG5a)`~Cdn+V-I>*y?zraDz7M-6x;<axL%VbePKYlejuxkVqTJG9jD>h#PpRFyOZtP;`8N3>me?5?-D+1+)?9YQ2!4m<uyr`SpI@~K|^RV8l(Ef>a$AR5YFj$)TWW=OPHMa6e`Xmx3hOs+;UBK6|gE^Wt?DAo1w4o-j%{fDhfESDH<2irDUC}2&w;>(9h?QXgh*tMxDtUQz<GPxFR_x|={QvMjxkaB|CYN20jSkm3eyYZvHk|>}c2^?j9jnOv(a=<oa&KJ14_m?Ve58JK`7i3dA8~Pnl{s($FUKgd1y~7Sc)&4~;J72uZ1Lf&@BHrj$?bAv4rwLsmBs*fXQA`O4gyh;yiR&_=%SlBSx6p1s6Xy#LaCK(6!+e;vc=@w+zkGWA-4jU8TxbQ=tN-pSKyZrDAt=Cb6dO4;q!_R1kAe1ntp?NoBoves-^NuyoeM!AYB(!ABCR~AMyJe(^a0W5Hh|Gr)bgDHqEV$A#nKuq|H&9RSr-Rs1cIn+TI55|g>n$duF$Jh_ciubSZwEFUr%*3S4Zfcnxf99&4pqRZFnH!y4qQ1noE*m7W-uLWwSdW)Zop2*|c`@I7Vyrd$IRlckv$s*ZN8H{Qxr(A?4BXDHMbxmxJr_H1_vWd4#!B(W>qC#%mpI!~}Ufp5dWYdW0@`P*j#xKnJ#tE-E0fM9LXsg?I@@%yeu$<LYB9SF?M#DCzZ4-49i$w2xy>oaBcIbr|1NP0&Ig1S(D+7-l~g!bAG3;UVtbw!r)rp`V42pz!)H1cZR+>$QId(E5v4UmaJUsTLo_W4i5|O}6`4)D33242+X#O@4pz^<v^WS^SR}2aF(1U|V<E|59uraVKOvhD<V{Jg0V`X6|L3s*}C(hezqcwx-tH53Q_Kp{;`2iE}}EEq!xL^%E6snV>Cza)zg{bLM_>JqjsCVm7CKMllqA7<Tb0lZB%kfO_M^3Ol_Yob-!pxyR{aJ#B#HW|7v-+SM(<O*rblej6PMkqrm=<hc-4vXpxirjb*&O?Nq(3q_<B86N~R(V$ldkU8q#^U(Qilet*FTadt57H-kjJoN5r&o#)B3tkHAMu}=L^@FX8N;e$Sv2yy<SOWMD)cJWB8&^A%0b;2?Iu+T5UZ8^eHn7P~CAy6lc<lf|A5uZ_<Czo=Z*CIcIZFWJrIP3&`!b)mq2)xKylgaGxZX>K#_$$DuLMlZxX0<nZ7(_Lq1{>~@5BRi#swA?3CY^92LMURJ~dX@+1xHqH@Ut)l8R1Lk}0R#?1`=ibd9-CY+?y(v=c#eP~5+FP*K;LK?5*zur-=3aXT{Wtd25-cQV3D;;K?k&&lewIjO#6tvJ8`7{1eNiq1ZSSt6M?7=w!cdz}H$a+g@mxY+VD6n%MLva}v5R@noltqDrabL*W7Xk|3ItCXO@sF)<>2j=ia!a^~U1(5>JXj5q-Ph+~|Ix5LNKB>AXSxqt*(n^n~{HSVSW!np(7{R(?7}Z7}WG8x{tT#`+E3Z?h>FW%G$n1i#^3-Rvjs}Xo_Sr5*Jamu=I9H@4L6*9W)bA@U1njB=(kMY7(Wb?e)#xK7vw52G@+J(wWo-!gBf5I@>Uo-7aT9zj_{zS~VUmuXBF^t}3~70W+DUylq;^omc)we^cVhBh8;AomEkvZ)79z`~qQjdlD?(jVr|Hr>Z4Eobk*&lvANMg$r~25|*XMk3cL(FD$cQ1_+$iy?+o5)K9{xzf&s}4?t{0XwrcII=P8Cml@7Hpp>j-))qUbd)@-;x5*+}>TIH}TKgMbd@W|>Lf-OSM@z*h0D&Hhmd3^dVE1;jj0K8gCp%IvGamZRt4%*sfYo@~5jqEkvvCsDS90oOdE($kV1vNnNfEgiyzN^nZNU;b?fe(pn2jns(pB+GKsfRPvNM`bfup!aPUi|j^9fi1UR1O2E~c+`iip(Rl(8$ExXCI*=(EU!dFZypFA3)dQ+rPlBr=JGWFpk=VTN+lXF&4~un5a`J%*nD7~(*8I;P?E(m+S71s?Rblu#kDalXLiez;7|-Ivs3*A+?q<9HEtYf(_5C=F5?gZ|Lvam+wVX8_}xFh{j|4>XU()NhRZvhZ8v#2HN#2mzFbPe&i+5bH%lV5>QT*Vp$E~X#wy(3t=)1oOzvlah0Zj8i+^*)eCI+a>Jctj6TK8EPgy2nV|JdsW!KJkh{Tq4BWGH(l3eqvI6zm0G;7x)gz_;Sn5Dg-_HuKfFvZ{_zN%<Ib056EuHQ$lZxx?g2kJUDsJth8xs!GW^*`Aw>X971k7lx&Y<TtXv@FGEEQsUK`r6H%6U!Y0(Sm`%tI!LE05SJ~y4Iy7j1kzj*|N6wHtN7PBmV@^0Z7>(DD5o+ok0%PE%DG<u9x<+Vj3Idf$y%#aocY)a5Xq{y5jq0YzXz%)3_!0!m9TK%DFO|?89m|RYI?Jb5Yp4x3bi1<`_ZR+t9#^0$UqAb!Mx&!L%^PHny#a+rGbx_-ip@AoTL^xnQKk!z)uc+mw({zWu;k->W8h;oC>y7n`el&WqF>3-0o@uobDqguv-*!cEDjyoW}vf3A_PT-bw;dpL^Q<`;2Nc$MqSq61F0s9Q>*B$nKwP%DcbluHvD*JTt0#H~foc;POF2KE_2I92W{qy-48N08Ky&}H|YmqN{m6|!=UIlh8wL)o1LW;LNzq#i#bMKSYUBHN}`Q49R^U0WZLv%frmga-JuT$<t~unK4_)ij|?gQLvdD3w%&p=xB_+UP8+b{xz=0~sJKJCEHC6hm*zVaxc{`~qSumcaLCxly-%aOp130kpZEyQu6Sj{(};+5Ku*S#EIvz|q{^<D3=`61j^M9pX`y=bF4En=^~0zFYoyvF$^LmfxnuVKMl1$R;YiL3xr7eDNr@DjgE{G4E0!$CtE-;n7%aJjOA(J;~_V7mO)d_fWzsU3Pk(wyhT5+{kAmo0n-x(#ynDQ5-K(IYRUgz4Z_8IpMdd@i{-fP%TT5s(_xZa(qNyfBf{*=Z(8XwE&O*^4q6>eEjWG`Reui@5`6=qxa#phth)$oE0_UxDO8xvS3%6KR~n4clAv%^i#hg8+*L=$NK#5{g;30iV8GTzEv<1It)1rT@}N;YJwjKA3MhhWa+x;LP}u1)U<;}>TzKN0jdF-MpM-{1L840f{6FDr(n>xfBW&{Pv6~U=i^U5{Nv;6YW(za_Z|#S-sY{#v&<b0Qc^+cP6RYJ;7@%SGNxgMxiGG(+HUq^eAtPapAMhZwbt_62=x^nKCdbQ>!$JSwF=J#7OV1vB%H|GqklZ5-dH`K_uy~8#|k**o6swcvY769+)Xn)fZ~N&_r^IMacyI8ViB_SiIuyftKBTYB37C$s2)iTh~1*ePXYxTO#!h+TV<BCH1LStNDy^h%iU2PWo+eVlA6M|XX;l$2d(MrS+pPPZo+CGh~!4?+jBCtVBJXW+VPmV%@sUzD4m@aa>0f_Uh>D;xTvm!@b~=}L&wheNPz!!1#6EpH=LY9b$%CnCR~vPhonw%(hSTsbA1q^IC6K&<m&@Ta1O#e7Es{Xdi+we>i$N{h-ulk3&n6{%Y|LO{OjMZ*Pq|rsv^S+L<y)M<Z;!as-pTh&Y|z(THTa@U#t`L;3XhE$J%u3uWC#5m!Zu_UJSwy3UmKbv)5EnFl~fF#ayn!R71J%F;3`p{{p~3s~s>r#a{hRa8mbOPNC)<9%Nnv>rCWymEKKTve3nVW@$_msHEr?mA(kR%=g3XVg<o{e{r=h&XyF=2<~Z-M&BzCLL7-oV*VK?V&CV15?Wrs*&jh^9G%8O_Y>yrSYub&`h>O`%XJs(3xQ8kqZ~$7tZ9NGf>_`k+I)i_72AT3?4iVmXuU=U*+o&f>WtwJa1wPo53|jNd5Jl$EsK#AWY%S+aD6U5w=7(t;BKRNUB`Y9*7sTp6F7<WOrvp3XXYB(Dj5>*5+w~jg0n8iE-kyxD!28&C4B?zBz*tr)2~+v>>txCg(RB>^7Xu<*h`p>5zUQ-Sc+AbDBvoC>w0YkiKsovIpfo>ewXORgg$^?3z7N($&$15Y(J6*^nvd9skfc<w>6I8aXdL>hq4AT#)xORBBvoQm)Hfs;QPqW_EfA!T}>b#^**+-rJo)eEE-Rp;y_7nHNtZ83}5;7=rU#TQ3W|#nYxb*UXZGn=X*BHd3b&mJ%f>21oA(S+-v6f7)ABPV__rVawYaoa)X6EY0wwSVl}c1FrC`_;jR2Yi*X`H2Y1S&XM7yng^C#HN?ljy(7L2}<>2|RCB1@f5xq<d@_W$nZIX1AbVdqOId)*kV@LGM($ufSSWz$6Y)l&$)7Fn~O=OzE_64vvIdZ9HosJv#Ty(!qw(0>)2p%>AyF4}}*B{!A6g;$0M(RFD{tC5l{kkO+mQy0)fNvwLbXTkR;Mw+@vc6VOGeq>Le1}&w3xJH_a<LN&a+$e8^IZBOI0lA`td&=m-gXtJ{B=6%85@7NY>i+w0W;J`YJeypstld-I2aH_NHd}Jzy#?xSV<sQ{_9{obT@SU^V%Q2)fLpI=JMRba_EMZ!}26xV>m%!lfwt`>7gI;BnAxMP=%ZjqcOYMz8PEOP)^HAQ+1|#o7Jb4p@VgtOl3-i?0qC^p^kD>Yr;|f9f~XpGnINzG}Mdf5Wt|xKD3<NjCFL<36icnFU96Q5CSP|F-EL9mG7|uBA8)N@&kaaL`AFY+H}!1x;QRoo;@0h{z$a=zeaTrMJC=L)!v1cX2zgVTADJ>0Pd#1*>2bDI@<uQB2gAS*uv)0&N)0SwjT?Q3)ODkNEU-hlnFw$h*aGd4XcCBi8yK<rtM6tCZ|A3jv+Fw#Kb^@=?5QDIbAVyJ{clW;o;qLSEneO>!MS6j^V1@@xJ5I!#vn$4DeOnH@Z2eq7h7z`Z3I9-<S91xrv$?A9luvXPp?kuTx}$+eb0CTuqOig5?-!O*gRHxCdr=D)>z;{Fw(=a@E1Xgb{Y#Lhd*$qpc92MKNr!HY<3@Zo%akiM3nE<?Vn-xzuQMz1NFvSsmk53yfT$ztjK$#9AHL9!Kwbaos3<*m$wG<x2T&XpfV3RfL@yGG}>7Te?O&R_l}T0@;HdAtYQtO1EDb)}ck@4>?~AT)kZV*q{?HnL?~d-&QmeQSe=u1Pm58SW9ngj6&o~-W%IzY<6c14J(|3m{kKkQqexkritxiS{kayyv8=9s-3BT>~^(OwI!4}>^3+Fo43JN`%id&P+C59BgXsEWnc{3)Y8cSHmJs(C_^n{S`95_jBfTX4dVL#bT&QMmL?5DAuKAJG!T&qDJK?%Ek<-CQ@f1E0$nJpF}&9`%wX+|7v<+Q_B*F5CZnUVo7vlD@`?_#=@eXAfsXfhnSCBjh!pZiPo>E*hwxs|W<*vSl)1#2Y^FK*Ul#N{UYgh-HKPMnR3JxfJVpAd{kd1aZ3+Cg3A=6aoi%os6V!d^c(KHf7Idy3Sl7A1B=|vE9>?=hQM+_E{XcenLyN@vVi)ZYNM~o8YjhZFP|RDB(6s%feHj=@k>wc3=sU)KcA7`>(v#7l@n{I_Deb}9KX{=yPg9R=e?_ec<~zD^E1&od8-4V*8u(&o(4xZyYAq)gQswvF8uluEsl^E082dhTi8D1-?ir=J`o@ytV=ps{EQ~fgB7&|#5h+oliQ{l-OopnR4z#97XO|Z{BRURUMpc@6Y2Y7~FfGKOWy{m~nC-#u<`uhSmHP($9Pm{S6O(c9x(b==4I01hN%|l`dd$&icio^2{*eANw)<8sO_Il9@^5?Ca=>UH0=5+Tsz=7qV2}XEVQq_~&|Tq|v8yVW2-S!}?2$>L&Ml1q1Rdes?N#YFw5xkhN_8&~8%Nb7kg(Q;HX#U5YLA{a6a^1MbpgZ|FOxYFJR6pP3+JEZ6Ol7HZYi1~%}&+f6PSO_dNgSK$F)?{Y1ixLg_nds?!gyQ#Nj0yh>JDla*RA1$WRl8W%1HOk81tshB?*Ku(zCAy`tZnJf^}~1CM4j`Kk|^)uZ3(3DkmB{v&bubrav?#-4H_Up1+jFT2*;k6*5lzg#dd4VoTvFYF9(2Fl9$qIJia=_$_Wt6#fv*4{YzYW7YmI1mQbmA>KguwBsk;=7=6zY%<PY9^U0yq4r3j&tv`_f+354i%7RV)#3=-+r34!oD}>{=UU<S$+2!h|4_Nmcss=ue))?OP#_S`JCUI!AoyfORL~Rc(Vu*uImw0FTZh-`~o0Ykm(EWQ!4BZ^9fIK86B=5RijfpZ>B{WF>}MGF$=C2ShT>Mg7`{Yb$|B_b?lmQ8<(ZQ<(i$v5mYHSk|%x+fMY3-Htz$LHBoi{71eb&oFd<K6A`lm%fiuaVtLBGH!XF=1kI^;(CYV0i9Ao~Uh)KXpZ70mNytNow0EEIsaWUnfD6W~g$Emx!0y~SY2YEvzFSr(n5gI}f)VN<Pj%c>7kjfF-{D5Dk_%(za9r-bMts4JT*R7s?Bk9vOpY-z$C$9l9S5RNX{oV6nv4YCcg9yfs#$ae&bSQ;3^TH(E$`UMHx1A5f>+7MBC)=!li1XZo65}TG9{T&<5`^?<ETyanV%}$VtHOxt>am>>Ef&4fg}sdIg|8M)CSkRN~X)|*1DwJ*u?gsr!ohu*;O)im;Cb(LLjP1wOy57Z@q%!2I1*CykWu93(4;gQE+`SPt7EyieFllrf>!=2!*`rLUuhq+VD0)$?2(Gr{<DXiUATfGNr*Eo1o8#^d~@ZuR*wAMw9IjsQ5hO66QcIA`Z&{7UDIsw)*j+M90*RwmJh5BBuf)>`{QzS%V%^ujFZ@RBo+>qt3>l(m2BooBBCXSg2Ic5^PYkO97A*;Q(MDiwjGTKbY)C;bU3_lfcZ)4z6Qrl?zQUAJ<H8J?zl6k`M!VudXW{$RSxUX<-;|(>YvhURJ?;<?J-hx3OUhm-arDs%9VKmZ>j6m5e?H<P968u<K=9a0V5e631#P*H0gW(%-1(1B_(!Tb2Up1r{>W%s4&fftf1KgwI|v)`H6J>U(HUq|oUty2}s-n2O)MuwCe~yaFk}$|YC#*oeUA%djF!g^<RWhP4suG#TDHkds0gM)K}(tcESoR3tcC#CmsB^eG=M$$Xf`E-|K7DuY_H=JjE*_a7=;r?Iysa#*Lt7mg9!RDN6y9VvP_r8uD2s`_T&3|51V2<%+N!HPC(9T~A`k7SC0yU)64K7>i5>aB{FMuAUPggaVJ!BvWb9Q;&}PbJwdBoTu7*CkdY__npHO&Nn*)IAw!T4R?lTEXb+R!`GOY3My<iKIch5vxUSPZ5cprgI|EBIZkB|8Js#mr&}pr9B3Z(<W660I;ZlzsVJJ0scg87N-p`3fBtB(?(G#q2oopU#};eIjrM!o>uoMVbhy3fOUS8-1p#6klnhg`vQjtAZ5X+Q$pWax#{!e*=tBq6)d$2K2A;7oMtKLqm<Dkx_<R)g4m!!-)dHQXQZ4!eh9o>dyytTHjwg}=3E5Gh}2YWk{z~|g4mn6%f*IZoNA5RfkKu$N%RFVVq8u8V9OB$EuDSgna2&UXGBCf$N<F!8PhU6<215lpQ-s2J&U~cWy}=0HLx*b-<DzRVXmT3US;~(P=t}cXns~|X-|uwXUN^qU;dQ-E7M|B6U}G4SD7TvSbNfR&hNxJxSrAY4ELN09Zkz>w}N&!IFyJeOO$MQZB2<Wq+HoVz8@!Jn(K>>yM68Lj2Hh4Je7zV#eI|d;8=&0vNS6vzWW0@w~tjmtCJtnl?(@`W%Zc|z=vXGPrzG+m9()l4rX1Yh}!Yvv&A|Jiw+%VFv{6kTTzGy(@a4cO2mtq8n$U&?1Pl`RqzVbGf`Z$mTZn=eeN@XHWnUG4aRU{w-YTN0K$^jRu!YNsEpgiFB(meN~>51ujNee46Ik_ta^<Ei8{6fj-hyy9WI!yx4UhkCg7y!f{5A>Ajx`$?&c29Sl`B3ZmF^OBn-b_=d{UN)^BHbwfa!dATvS>z_Xd#+#H<PytW*Ow8?{!kK2}3R~d-vQ95fKbywUBHr1=!r(NvOh;vMOtvd98__)~;{7M+7H$W|>3UCnj&xJyDYo2XM=GpqEfC2NRdrmXfFwfL$YFV+{`k=K$RcbSz59#}38hTeg3CSGtidO)__DUzm3FaTaa34nwn5++3CSt-A`pha<JG(X))lQ7#>G_c<-4IBG1$%#Kn{K8OhVUP7936Lnj85i@B2gz`8s$0>zldipBbRP2s;t;LXvV2H(e3k3{_^QJHM}@pnTygZdzCm>scz~b(#P?{4~@&lZs=+j`$VKSVDf0M6(uVKaRT1ZL&x89H#Hv5L|iS|pW#>msnYIU^?dH;9Q)TUcchOSY(%fhYwi{onBfo*;VDuuz$)u{ET5md)pkYLQ6)DWjj-cOsGj8ha&}PzBpbvULLl@J+a5gm)x+E9yJswHRuE+Zk5U|B?tMsxbdU~f9UjVlKxCvx4NM+div}FRWP)dDQ0V8PpfVlLRnj=`iRGu|aOYli4a~IplX+W`kb6#H+~#UHj^~oMcVYB?RDP+++oyDP&)ukB0>#rT{RLCy2t}~{`n1UJWX}a0MSb}>e=wWTCWgqBh=w*o3%S1e<(l4QyyxN4s9X@$%Tn-FbPZ<08up_YI$z(4c&Qi+r4pGIF}HA@WMwE&WVIYlw2?FYY~UW)Z64bAhbliyFYP*Oem~eN?<hAHWuR?soD}&ZK%~h!vD&lEx|st%D6}71`QoHaRU-P56{5&{uB{;fBV6!yo0!mL9Tt~$Zc0q3j)Pv7=gqkB(n8}8IvH*TskEj1m4q<I>KMm7hc^Eg=cN|Q$OybrMTDNd9{9Il30>vdm>Y|OMH^2IZu!zYyQQ3hA{zreB{nI7l+p0wEWx)qI<|`UEmTt{Kw)y}qA-YX+nyf_f0F89Fq1|U<%x=$BZg*sgwwN>#OgrEDUp|w(DT&ZWb*yX51h2(1TimBX<?h~XvSlvXVUU$OsVMAYeH0l2Vm<l9n59ZJq_n+b33k9VAh>s;3e~tqwSz*(a>?-&X<$AhIW7F7vXcP+~d>C-Ffb91?aqzAzCr9KE$K7=%_txZqYrnmXIk)L)%f*htfQ`U62#&h4s@Cc`dkC*?h0QaI)ybP@hG|8ev$!tC}#+vWXX5#6VJxWh21bja<o+pstEKq-XUxk8aT=nG&(9!Qkp(u)f!~@v*9NUZgN3{g&ZtImHVWo;*4>Vx4TGGA81KBqSv}E?D<|B80B(+15?BhnMKC?Mx11F4=A3=VkiytO6%aXqJ(b&x7D7WN>obz`jN5B*&4i`c-ON!R)tD{AEqesFzZAn+QDKg<v|B#20r~RCx}aTB$lSub14d!Dofjpm~-g*eyl5BUp`ey{Sp7J(w^Wx0mDEpV!=DcZorcXZw3)H`<pQL^QzUV!f2`6lyE*=7YQ4xh5xYTk&OyMjOZwTYxX($*$AcmbIou3UhZQv<|y-(5gMtu#7*&*7B!*u@gxOiS|-;u}2Sf<$AiyZcsMd^|GCt5R}WckeJuaRy@I~fhtmhXbX={vfFgKG(L{Htd+-4;As$vi+bG@<%wWXAFJVr2NsD*yih3)T9Om5l=q+C4bQce&U9v!3y9T2*@}Jh<~JFo0;_gQIHsZx%*zC2K1ql~{=OV!<ScJfb1I;zybPcnxld3~;&zzuHUuiab@C6=!RT@rXh_WTIN4RD+hWpU@?SdM4=QdTko-(XY@;Vx#e%$l;ow(Z>esdaka+{K_I364T$E6O1357)A#s3$&AO#rSpuUpR6YkV=yJI<fIf<e7%8~3+#N8jYiD6KG-0I89YP!X6N2PMqdnnRXJ>S1x#C2o1z}pSoglDhe9HC3wKp4PJ#t}|ODY;=?Fn=P8L-KKL6+)3Fc;y5g%6yK3>ao;+~D7IY++z?l%iZN2JESjFla<HtL`qyG&SG?^05DDz~+zExbFK$v2#-kB<_0(Eb2UIjd-71yFL(nqKFJIwwD4X6nYW}Ff@xUuWo3s{gNv$m@`RBU5Z*(y2?PvEj=I>ud}5#<tB?U6qJ`FOWT*uZ;5*Q)$e}!^s|)oa|tSy2fy33*mm8_xdno^SI|ju`$x;JTUNQEO4MoHzTz-OiQY1-Sc;O>-Nw7o)`P77xV?wW$lD)esC9#0l))Zx*WRf2?&sedzWh`-O7EuRY<3t65;Cc2oU{zjcMcE0-MfN!T0pxOi1caf#uGC#>TzkCg-7J!o)#Mn`u1->e*EdX+w6S&>4$%Od|eNpUhdu#b!Fb?t+T<o`joFh+~_^t!#2zfx_^8bvQV32O^=>w_9J1ZD_FZ=C($+q#RxV0A3m?@n(3yov8pdrMe0;mis#kfMBX0#<0<vG-+%b=yMKP(gTMVA%VCsnLa)^38jZieWMWctyf7cAt#|K5HU=jaVPTwDxjUJ;(^OPXAy|0SzDQsv$)+s7&JK0CRc7gtfk(90pjUN7cSm`UuF#(`8nP7-?b|pOTXbIJvP|v>n99{Y5S5x*JJA0qIyaKLc06WobBWH7@k1RbxM#89kC*&$Hp=E1@b~=}L&wheND$<7%XWr#$gcHZ&x9*-Rb8XClAU{fkZc%ocZxjUBL``=MaXG^VfCfF^c7NRgCyGRLNQ#~a$%P*|N8gq_2+lDs>~JE^>%1$R^Ak<zN?R8%Cotee#~(MZ?acaSi$t*B`{8{s{$B#Gkqzz=o%^LJ@lY3_b)YjeVT9~ZE#don3tv+E#)5LguXz7nf?*0uEkSqO48wzx=+fx-CzysHJsHs+D%)s(8YjeX>?V9&U7Z}<I8+M+%8rS+!xAZb<8en^xOnDjo_XZY4p7UA;ghrDD|8^5&J$5l*E!jA8gS^|7Ph2gHT;VHi=f|ya?->DYx#2ieCNTG&zwK?pf^>U0C29+I)i_728dz*+WT?WBXys7T<UBQXm+aJe`NxE=s7~FQ4ZcUL5@1{lM3!%yrZNPLNHI<auXCSy<l>Yr@#LeH|LdbY`xht()Bir^QEb*5%l_v3w(6%*tZLz5#X;zW?;;*Q*5fk7*wJJYJC-<a52F*h`p>5zPs{gsKi{k>miub-lKNMASd7KYseDjM?iL{Pr$*Y1J)I?>~TE3z7N(shHq6|LyDgkvyOebjKG-8|I|Ht#J&G<H;dAl=bj2Mm)<E=_s<m8y5hB?<41`Ho7|@(ua7QKtAeyY@?m)7ceIpPo3gG^eHvMa`Fsc`S$1x!pCiZZ`OYM>4<BuWZR<h5T_q><SbS*YCXIL0txaE{H8Y_Xg4_MWb@~<=;u>B7FuLZ3xVyO<OU0S(x5NYbV$b{pfw{>E%l=SqEyul19!@!XM7ynb0>@kt&?v%v-ZW<%87`1b^lMOHQLL>AioEj^`B$9N;)HjsT?~n<gp|AMOSVzvO8H(uDllbsBXvCuZc`El6tLSZ*t_)YH%Gl?z!lGof`BCfX%?JI^>o-j3Cfi*F;5CQIQjK$DXPj)32&IT1qV6D?p=rY|m2t_URuVfBW=)mT#8?k;m#2KIrD*EX~?$22N1ORWFpHJT@vCgF*W7-urpv7Kmatr~4WhLf_W;*zJlM=}-bohEv_SNv}vr9qzZWMfR8Vt4<J?`)zU+k?TR`ij>3D9WW{<$)KD;(liIm8Kda;+u~Co8oO_+={0WWZMB8xsM1M2amOvaAGL&l)o)&lXV8FMjXQWltQ=7pH(aFrom#~&qOby#j7JF6aOrIQj{1?%UP*=10)D!8o{}L=z)wh2K#wK;hl0q!&}I-n>IyGf5D&~5-PA3(4_KRnyDe1U`oM_kL_2BJ23r+38Uh_dQPBt<RNc@#(Wkxk3&S<MWNJNYAPZLi32BIM^{%Pr(zl+hubx;ak3p79b~$f(wOX!~6=kRD-|i%~A};dxf*fZ;O7#w4P}d&FSa~f{CUj_L@0RrWu&?e|b<^X1X1F&LWr=@ExCf%xIi&`21XpViBX-B&c$2k3_Xq%FxmdWvkNI3#4;F8ZIjcsrMJ5rQ5TOoQX=ySGW&Qfl`Td!BPM->ify>=6ZFznZY%21Bu6oJA96A{;fNujL+wMer5fHF*JKG32p;?{O#*6%cUUiLT^i{K^E7jog+=9M4xl#=YRN`(D4NhQdpZCaL65WzvFfJEoKeRC-wX_GzoP%9hC@4hha`aX7O<mSNODM7F%(Xh@yN^*-NmKV#cEla}Ip1DPsD8*BDq26`I$fTDt<l{R%T9m|8D>*}>GGapWj_y8oHBagM-fQVnoD(SNRw&7A&#(kjXeXGWw^Nga9Fc$yXG*X-#!!_Kw0cc+mNsZ8>~BSw55i=u_~Ktp8zZC&^&qS4};(J!^enxTE>%ZfMK*VxqSPuX#Rv==5FO=SMFNyg4v}++coF0hKKlbtlD!7Plg<Z<<Ey4IFK+0I6{9|yy|r9pu6gc_}EG)kM@f`k}#lkw7DhB6?%dCQ*b`7!%}`TYrMG3BBpK4d#!3CI`<l-!Fzq+N0A9Ip?CYj;Y&J~z687@MZ6xyq4nOZCLzJLm2Zfy`Kqrig!V&h;DgNM!=)Bo<>S<Fm1k*_aOHV-biw^M6-*U>3Ko!sWwyYoC6%5@BP&M!-f7Y|lwEX*tINZJn(4r_fq@}g8>~TlVW%k$WLHiXJ9n-GFDZehL|T9)UE}!xaHm9)J?lJATK1AO@+A-%nyY9ZPJV|0DZNRK0ev7$qkoLDz5vF}3EYj)s>$hWd>@vv2m<&T6apc~!8F^E7isp9sRR!9{bEBaF}3|}`06xAjW45vASGYSo*aO8Yw1RF+bhzp8D8FU@G3sGDB8Ou&0a$?i0TWb*VtD<>0CD`=*Q>8r*roe<5M`wHyzZ7;r*sonUvBxLfGLLRG$#&fwA4p#bX9suu)~b;~==VN!g={rt2Lt4<fGsd_b0AVkv|$1_fq~4f*Y)U8?hDXj@KahE5=bY#G<uFjL)Hj*`7>n!)0C?TE~aSbd)BrM#tFRBy#9g*;%rK*95*Kz*EiP2}PV^*^1_#%VZ-SVv0-Iyf;gv>w26X#lxddfQkAytP|wYL}3)sj)VJ_@RB}5j}vVz1U?a0n0eosp$>59>7o~=N8b;W$b}NUk3ct!4@#LwS_4-)l{aCWWgjZyQmsK*^N6zZSWIcp~15xJ19zx?DJuR4%SLo6yb?7m;z~9S$_hr3lhjK=ev@IL_kHE2`dJGnVZZb;09hiycX@DbecAZd{>owfqGT`kp;Ykx{HQ7h$$Vr&TQ@@>qKXX7pLP9?;d4UMaw1|GuL(*)?UP}VZNVXMlZbil%<$`d@)#8ih|xCcU>bIEcs3~&#SdlhqMnZKK4P4&86PsJ?sBooOi`2$a%!0D4zcl5RdygTw$A(9L%vEBbjxkzSCI8@C1CKQQ9I?g%0-8;^xO`_KT(FNi{aGXU*FK-4|w&C2+Ibv*qp4b>HxE*2Zj?yfN_Z7u^oe#Q(ZccOpAqKPZ~CK;KNfzOB#oIz*~ZXm-&JAI*N`>TQEB1%uPz%8$ZbKg;=!e7h}?DYG9g07Ou3rj>uYO)21y*0j{SR=TiGytK{!V^1MCX(`(TxV9~J4mnz2qIje}QMH#?$R4nya%Kb31UF!4Mc9+>Ds48utisOs<Y4u5eQCa6fsR@#frYqgJ@W9v!qb4so!xcFCLB>hOBnM3+tPvyH6&#mH()j$3<KCZ*jwFcH&;Jz)O3Z(obG0g;t`A9pA0*sR}nu}!^3I3OukwI^p^yb$PV_fa1od(btok~>+=Fg6@L+w!wB&{@ZEJZ$IFr@-CL#n4ZSYL%i3Di-*-WP?`QhGz<#`J|1PTgyP*v6m-E&AV|O`AX&4Pk0}RELqMIAS_gdU?A8YsL(HDXkW-MeZvRnmEl}b^g$3n2;6f1#Nz6Uf?Co~zm(f9jP5rD^@h+O-zLGXdo5XhW{%V@T9NQ`AqyR;~m4_LJ{E~|tOZgD)!1-9nG4WES1l;T*s*xjzpCc5B0q<I)ivdG64nFc0;5TxZ4$TFsN7%&MS7Cht|(^^=4-*R#}5D8PVqm2M|!v?!PygtNel9A$jz>v{CLwN!X1~G6mgbRC0@knT|8}L#HMgU9Z(-aY1HU%(|BxX4FOTJ|>uNL&fNJ(WJ`!z=hAQIKI{tB)_V9u7Iy4%g`AQwF<(yXnLA_h=oua5NU3WEBGjh6e+oht%hfv4i&+pLGzKx-!kj6;J4-9u<PS5kDKRD63**g6b<Wj^{X3eO~@MIgHz!y2=y-VJePMv~6zDLtHfu}9m-?hiq<$E$oj$#n?4FoK#3F$KrYWHOx=qlRJJu;i=Y34xC1vGH9T+qT+j>nzbiHGT}WEfon5TT5?_OyM$xIap<CZET@>5Tq62+KyC5SyhNBTzz1D=jWJ$4E>AQ4~_~iL=MH++eOBVHcp}$DH9O+8RL+9@Gmx9AfV;joM)Q)0|OcTHNZHQRO-!_DvA#LQFf8B`jO+H1^>H=#{gUBj4*ao82}*$6rR<kSq>>@^fVc0-wnZRuDf0N6zow;F^Ik#UjNwk!mRLQ*jf%Pg`iPMeI{J%odVOPZMG>~!7PQ>Y!rP@U4HXBYKW}LTrnuZ-9M$726ShEi;YRtN%i${8vKkn)nb&b&OqtDcqb8Ve+~C`-S$!U+=NhuC(+o@IhiD*rzgwNJ;$i|9Ols107JJ1FvNM#VOsu5&|zxoQizh~`)F309PdpIe4HFN<mIaI`6z}@tM4gz(VKdA<Fw@y>@Cv%OrMUGORM6?alU*tB>`}AFd{+ZYt7x+%spe`2WmZ}--)Ce%>7w7UdpV>c5BSf^qj7F@XPiR6$9u~cDpYchk_xDr{w0Cs<GV(ER2MJxs#m)M@S7;{k0G}KZ7yPd0ht;s;1M=f$eR1k9}NAV<M8Ni_@1F4OZ3wjk8@K#ialpkrO63WuVUUW*;QH$}EVU%np=swP|f~A+rJVbgnADr{!A5{?-Y%bUqw?x8PJeJdNjBos69dh_O)Lz&X(?MVKD3-=K8@$>Y>eP!#JgLu2g_#mK13l#3Pd&9XG{3ImicSVsgiA<1%J>y*%q;nhNIz7qh3vUHJUZfT?fevVbqK(q>cM-*lkq8x^v<O}(gL^1$<D8=!=)0YP|^y9KNh$IP#0A^`R6~JO}WKwv+lYyc2@<iT8twHhnyr$;>FzcVEyVzzdMqDn3`TbXr9=QLPMI#+|t2>l%w4j#GYzcp+X8~BOgX;{d*oeDrFGe@{I@bj39rMon3svQcE@H=G8JDhk+KsC@RD16fN0Q;`I-gt#GTa2gQ0?ucB%nQ)VqIFW3>2Egxu^DYqtTNR3~9{?FOa3nPzPG1o6<BK*97}V(eOcNLh*uzqV#$I+a=K;!Y4AtOG+hXS=mT*9&KGtxs}w0z)owd&x4J5MkmzPw=N-IzE^Y;6%RBQdu)FBH*dO?K8kqP$#{@p3<+$Qbta-X8;euJ3mw=xc@0V&97M2*<cosW5|3d{Fu5p3LKSOl5z!=qQiz)nl1Kf_@sy+HeB5KRWqHOeMNjgN%S31|@@iQ`W!r3eFm1_9RLDF9XWJL5#xPwj=j18iKg&CU=|I;YBe1$l;Il>l5u)aSFfO!u0Bj!#$^hH@%s%k%su}~L2Af21Q@`_2mfVLpd|jyqijdVRnMrNc^%%wYe9F(g#^$@;<1-+q=`#JhDKxroMcG_?v@2!2m)^XM(h$Y$O|^`N-ILeLh?{l{xo<Sfp1@JE_!p27r*d7NsL25^%P*VpJhu<F=8#VPPM0k|X)^V%J8_)vwKsK_HU&NqJ@WV@B%M?1tgdqP4~N2Z(J1Ve5V5Jf@Aum}96|5JxZP;F`e^EghI+JwT6%^v<#jv-V;Hj;J_!{t45dEhjEaP*(3Wv23`7(N)frR}ZLS1iD%5AV7cBO7u;9g7jS|4X)+HzM;`6h7B3$A)k4CXtoio#sot8Fr!0V|{tYNJNy)r|F8-$)gZC8JBo0*7ixgr?#;(K6Umpzm8p-RYgs)<OlerC$(-0(ta-Grk)PfPa^*f*q@Yl$r&J3(0(NTGtGu>1S(yak(9b8KJu37d;seoXz;q-_FOeN6ULkr->rT0G^d(H-8(Al!c;4KsjcmL@5%ckw+&^7Cfv(h%_ghOOs7im|VYkovQLM1f57f1PsYO=t6>sXxn8dY0Ctnh7Hs2Us>-vRoVB@%Yt9$y%pA(I1ul!Wh07ISoUXW_b9+8dUufFO2GFiX4ok&y#CNTF>JFrP`rQ!_cl{Q(wkRtA({l4MX<fT-glONd+%4T6}C{B5HieV?@3nhOES*P6!y-+%owTo}(8y)3T3ee`!&{k)fa<C#X0TQs%$=;d?lOwSmGw#Fi3m7Hberx<rGIqe5AGNe={vNd}AySMzvDxyzzE8v!&~mNN-Fj25{1A~LZj_;&ROVpS_({u6Vauu0)nH*_#IU?EWiL=qS@0znL}q-2%%0y_;1Rn)geaE4U<vQ?F$IiBo8juHpr6&&}jw%R|ab8l3ktC)G(KAsoSP@yYe>7tf1lc#bxlR60iAB>glD&&mp1|On{CMcQ#y-SH$yIvq$6Wj$FNfDdD$eJ(2oRkrmo7b)0Uid?CC17s8w#G)To+=tMP5l!YBsVByd@?*U4SyLt16VP;(l3T$#&bx_fRUK)n23?;%yb5aA)}`vL5h(o-5Rno^0#|a<#sAGnGD(uQ;Idf6$){H$Uv$SOp}o<6%X~rW+B&EiIk~JUckr8mZ&?zr>Bq<f1%gJx}u2aTDBOFrBNjR4GiB>f*VcQQN^yZDKEA8v)|M{s*{5B?<#WQZRwO?!8CXIUcre7gf;SMC$<n;j?`A-C=5SUjtN(THB|<I^@H7mK=)~G1c_xM*J&Pe%!`C}#N*4yd?S7uEJ+CB+<D4#F@&sHm74u*+Ap7eYi4<sUjqg)`+$hqQ%iNAHVT!1ol90hG*Q+NK_#;2S+<y(=C!2&2|Ru+o<v(l<3|y#?5&}Dk&B{=<Bl}u)~k8Bw5d#kur|6g0nn@SO~BHwjnPvp+TiIvX4$y+T>U#Rh!!n+NR<HhOP-y=s|bPlDb^BLEdmc_-FqS)E3k6RU^ke5QXeN#?Nl{1@wg&Kd$DU(c&X2ESCh^|H6B5m64AP#52o7Bv^1y%ANWrHyvDf&(6cOm2GEm6e2&^N+(&pAQ&3NZpI{`Y$4Jm}%#^KUm=p*eIM~DSndIB=aUxjiB)_jS#crm>cL|i*jVCJXH~fq;s_Vrz8Ri~=)+6@)c$Y?LX6KvfC@}Dxn0iXlEwuI-Y)yA^^do!Bu#fb7f#pMs_(+@^3udrpI)S89qx8kJX1GzRtQ=%dYYLP<6TsRjm%NS+43aZ#6bJ<*Y~mlTP2v&JDd9C*xEd|mWC8lBszw1|PfrcnKj<AWbX1+9UAo$t?C|8`A^_rONvrLEF>I}*4aJR-%~~o<t2%RQb5p8J7TrOVnAOh&#}s5s79vc7G9YDT$SRRsO-fvfcIMV5I~;)#V#0wt0;@)YJ*fqkbkDAqDn0@MxJ9pEFr#}WV)Hr8i)sQf_!$^FwVomh?`BBhi&GvHuIkzD=c8fFrV8iU){uGy%$L04J7IBUbUoWR(agkv%@w`cW>c0FF3r?wv<A9Np{MjVR~|fZ%xlF&I!ytp%$zTm6X4GJmB5|((*5<|&VBt@-Ami4wVDGIXid<3wgTJPam{x)2(o|Xi^}4j>DJ_7KtrQa@$;o+=F8yDMny7W!3ji|U`y0%OBK_68PiovR9h40zC{b)(6}j&<;2Q1YPuk!Bs6VyD&SGKUzIgdb6FEfl$^kPk;S;I1jEyXwJWz}S=fA$H*u=7RODo&Bx@9bDh{&d%a-Vc;V8zCQW}5(r>JOicd=O*tZB0+NK=D+#o`9`bvaoS(SDsu(bg~?UE9FezDX|iYD{pWB)MAPU<^Y`phu5fFx517LH3p-j^qo9TwRiCqX5y|O+H2x8==xBl)0jWhvrUFm}E~Le6mJ=xAG{$0VJd+XvuAOanz?RWf+AQUFV~;sR<LR$r?0`E#B;6G}UUVp`C}UdY=p7B)E7(Js!G}aigaCv1|9n5l^ZyNA7DeH6Yy^TNG%`y}ZX-_b{43<@JEia2zFKjm^DX$WyapSjASNnu~%TQE<PrX6Al80j$)ZLpMaf_na=<bN{C+?(Qw!E2Z5&fK!I1zEA~j(j5p%KR=}_)XZy?j1nr*8md3ng}ZC0p&~wAzno~S^x}D-G1)%JC7Ap5DSQ)pdDr0)bGm_z+q2pZQD%><r){nnnTJa*?4t!n0loBkf;8o=m7#0WofC47h#^a*RVB@S9{Pq{Htmj@DMr&3{A{HRxs@Ws2k<{<<ZOKU3K-0oSul=7g$3t|DunQy8KxHSNR=B2Azrk?b)YcJ`I5Q>lOTce0$x^Z^^$A0CKfkEpDHqp5rX0Zn7PntN-bm2fF~0mgTMjE*Qu(QS?V~sT~VCoK&k>YjBUnC4#v525m~VuEGs1?+iAMvTqrj^rN@-9IB1ve$Gre-?i+>06(}9cvmd(>AXs_{kGT%$P*K2O4H~vt^~vEHAKQe<+_KSBG6r0q;S#r6!6}U?a6{G0ga#M|=@b|`=k6Qubm;^4-Vf{QDdHLfvtW#>$cG;{NMTt@e)$~8vOl?pa=hU=2TU}sCt#xcuRQ>cz7_}WF3*98#_i9Bh#o4O!V0Ufb(7VnDJ-0tr%N+!<P;*rK^Y7gF$^f^;8bt7$=0%<EEfjcL~sc(rhl$6DbY6`BLHKEGsaSt8`a>K#M{%DU^l2MEp_z*(ts6IPg7enqZdbULE!=EhdyT*`hizwC;SAF6_~eV^6xYRg?%Ff&UC{=&j?2t^$e=m<XMk@^Yug&(cU^cowAX6zMS>D9bSM*#{lMazAQ95gFrOyma}+^vd}@Q!!X)e4@6fuNi1qZqsws~l0*<{qADf4=2epCITin56)}Ba(ig)um|*&-`VzD|U6redM>o$Y1b~&X2<9=VB~h0=Fk371Qr&BVzY6Pmatx$-Z7NHHrN)3lObWVWZ>f2f3?9%0x&EQBb&-$<cAN?=I|NMh^?ilj@h#%6w{{Wp?hR??C6(5DR#}O+VU`9(-M8rXA;`aJ>8=q)r0NbdpTYr_ub{C@9%aM_Sz-e-+P8*+h!@@)t%4F?6vz0e!eyD7`z`@+9nkNnzX$A@^YO6r^QT<8WohU*>sY0$WtR0^KNpwu82<hyM0j;x-#D@5r5t%=g?^3Fsuei`i)Q34nYFXkP-UJ)W>KS*#Hx@m;VY>yG|PNg2cNPe<s9m5WziW{OF~tb7bQ|hr_P>rYQQ)WWqLBNwa!m`Xl6wmup-$xx#^MlM-nh_J^7q6)naACRqD^8v<76!?gQCG5Xtl^Y5U|_Cb6DIEw~a#d%%i-eU$XKx2_G6xRXSvZsFRN@W|SFmCPhhM3R<j7Cd}B-Xc0k(wp-1ji(qLE3Hw}HrhF1-m{jyFMfz8X!3d026ILl1UirKqz5VFZmv?uD~LDyQ$ggm{7FIN!@3?xc6hgIeM0Nd*ck;+Z~Jq9aJi(Eqsfo51RVHTr?g5SrglK63;dQsB16R-l(jAtX5x!-xeS>cqWRmoGUDYjHa{7ar_8yBOCc)Z$AN%v<<%4b8|DU-K!?x94=;%@&u_)(O?<1YgOe<5&nYaIM0JeSW4d@#{fph@bY~@@_8!6iOP5moW2H+;dHAKvaAcD;Q{IE_hD0MuThc~W(=3HZLH)aYqtPzr=E$e#SRil0c-_qn7T8JSGqB0h$(-U{+VzNlxCCVRHs~}SuJBfur*@?a*#$w=PVrm{C4v3-?}ku^ZnszJKZ^HI>mLZByPnwvjHs*p{n>>Zy4O*DwqpEZKsQQNC|ICccL@zewkGg4?e|BF&-*ml9`tqv?epg!KYn|Cn7{kc?Ee^UIz&O%4PBWa-6f3KBMrHp4EpwOKYsk_yW8x1{ON~(e0*I=pI+|XgF6%4=B=|CGbE`(fZ_TKcP9dx+vAkkmmv#P3gmKEq7Y9o`@M(do5e#StyvpXj4*R`D0I1-#zy}!><HSaM(ylwk2+->6Zv>b{q6T3e*EsApZDNzzn9G&-+!ch6MCgKx29X@$h0eXrN<c)FU*Jfu)Fsn8-o*zP_a&|+#QVW=Fu-cwdB93P8b8cw!@;yFBGh~J>*cATSd2_1CQv9!(TJK?vC;Rbk(1U6=qn1p_><530a`7rZ_y9%GEv)8JVWNI;O528OdEc9y7POvTf+J;|>(uv)J&*Oa3?;mrGJPwzHe<bXq-?e<X<6yJc(X8A3WHR_AxIXTlY^DpZ@6u3t0PhYNY{&$Uck>}Sl)-AAqit?0+I_4uW{KQ!#4#pRF($CWJ?cKPzJf4^RTes`<3nVupe-kOy+1uhJxKprjx!;d+R;39QU_oj}E?H{}ZU<)wa`m5R!eSvV>MvAVn^q?^JFEx8jLD9e$V=Q8{SOQb8I*fRX6Z(rROktA3{D4j=Rn)WE<pBP&!uEM0Z@{!A3thx2T=kI-VGN)L=;0ZCe3|cu+r<ik`$Chkj@gxB^ov{4LL<1RMH+ptKnQUp8lo_#PsF~@10}dXhS0HqQ|;d@{m>^WM*%HH3&hfLeRmh^#tx-x^WZc&krl4e@)Tk$@D6Rh!H<gby<iYyI6Oq_HCo6;p(vHR>WH`(V`TDl9%R%EF0iV@Z_8rT@&r9k0QAG+7m9`}l=kgrEIl($xb6HkVQh7|R-r)ENw#&ap{<){86F)f&j`VibvbtV{)0~AL#wvH@C~q&@cpMxzg{J<e@ye(=kbc%AfM|U#a_a6jA%||n-yu^p+K;VLFgw0iKu^EfBf`Q8MD_h`0ZUHUyVM1UJH@>0hJo!IREYI`jI>!%4+V5qz!Y@-_|&W$MNKl9a{Hup?URk#IszHMQ#T=T=2#Pz~KAHIbTedHdLdoCXkPMAKPe4=?j<>ji*j=z-|j-gyrNJzVhwSO$qYMo3-D5I^x<Z*|w<VR4lro_1tM4VfgT7`{6Md2~;VQO5}RsaU799A43PFcr0urTs*_xNp7&PCk^`fB9LX+&${$}aH^$#6ihbqSgLTRJbK2*u|0Qg=|f$+4tz1Ta$G&4pcJu}i9vo3I=)Sku9D73VJgQC40-H`epy-yR$q)2^>WR|v>*);#;xnvAahJ%Z*t_)j=wr?+;h?Wsu+M=Cxw+K)gia!VFZEBDj34`f&7>lJ&|Rlg(UsDB@>oYBI1B=16&0nhZ7Z|yjd@+KkAl(1``|H1w@Y51=@zo#ZD~b`(67aBz+7Fm(}j7sH(C+$1ds%_#~9!vNeL$1k6w$sR5#Zs4{fQ<6uA#A<g(rfQGI+QR^4@I;V@sj@{7pG;cg9_Q}I}Fhx?NPdzM$ZfH3yPXacE6I5IMKn>Xa$e|zdBnAxM+>TYGL=|E*VtYRtJLC$?GD-v_eM=l@N-lmpnTEmM`>6YTLlZoiUyRO(VYE%9-V+V=VmbscXnMA2wLUuO1TE+4J-H8L^u?Z1$*~Jz0aZA6oLw6RRmcn2N@%k&`nPVTscBC$&mIj$KLDy$Sfjdc6vr7yU@vJsN~>yT&?qfU8D{`@bbN<9bDCXen~3UB(=DM|=5`n7@YK>B9P)0FjYhH<OrlH>szsy(5olPAAAS(E4%23nl#%F0b%lagWJ}Dzv=S3Tl5JDMH;bY3$*7ME5AUA4I%O?fbSlp=T$MZCcU*dy2m6d+JviJsg_Q?YI>M!X471f`#HUgz*cl(5bz<y}5l;uVk791Qnlf$Il&~AH+qegc(gh^2Tjaa$noiJ0ekM5s+;F5o;Rq<SJgho-{d`z7#q)!}aR@V!(I|gs@hh^mcD{`<)1GgVOZRwrFULqGPopmMIUMXOm(h*9l6sF6ij{%!v|uMKwJ${@03TS#<HwD$UR>`FpOGG9V0nN}&DCD+dl;{HMm5sU(y3fifOMR#7s~o%n8R*aYlZ=q2Ewo^zyo54zEB&D^mAozgU%Oa>c=L1$<hQ$LDPx%;TFhKucZ^odpqTv$bH6UcgE1L!a1Owd|?+S+K|^}x9wwUDSGphEUjlaYJH50L56Mc8wMoYMA!zirR9sPtBmOy!#4S210LmlPsUg8>#>ehbcKyer=k6zMs?U0J13pNeY4`j+~YBdp@z-q_W=D4(yuWB`=S`f2&H5mn2}zf<3ijIt}C8%cK6_9yj*OhY?!Gw@qe5LaYQ$EGkagqo0fkNA4y6B2aR9G%j}bGLRe8W$*N7H-RBDRn-N)U@at%6;&kiIxVQvZ*F+Ct3Y&Fer0N{e%mS-DrB{z=2|S_+J4ErlG<KI0Tz=@%uuKpW=L@`ovFqG04g4Ujm*WYl`k2p^p^cr)dZ2W2b$JJ%ecj!xO6S<*qr>2#U6Iu~jcE~>iB%au%h-)ADv`=<;W4r+JWGPkQI{M`mA%>r;GIu1EHZxo!xfcju7z&Z%J03y3~@W_1cB@f4s*CUt@XuNxf7<FvFE5BoF>JMeV@9hJ<;Jr93bFYVDPHD9G1y>+6<Tr6W3ps#_7i4(wH4pI~|Bm0j<^OPKfi6;~+b73h0YEZ8yZ$SQCZDCCwr1whyAMkyUgUH~zZ!b3|+Al!Mo;EnUhn#ucGu+c8I@t!M3ZrsawkDc>q}$s8{1F!{GViaUsqG22q;s~#ytgTV?MhqWzQLU)B<*RIN9c&nBA&={FU>a6N5(D(#DK{fT|ySn$ZRriXqu~4zCC5!M)#)QNKlZEAq!U3_=7xK==Eky*RiIh4X0nbYGk<di><D4%lq3d&AbjJ!Bt^ouhX8d|m>SLjTTdy4pm#dGM2c_bRTL&Vxz0<i?LdHiFHsun5JY~lK7zTauvPO@_eRy;@U3DDf1vSs$Z?S8}&aq`6jhs)?S7PDQQ=F1l|7H!FxbCy58)O<n8uf7tynEt|B(pr@eDPfo+8iD%e9hHy6}gh+v~lizS{J^~_^1JBQ9lz+v>)fe*3o*o#_Pf9Kwe8?680~!bha%m4zP-SMtYktx5>`$ycxXob{Va5LLpy+(yahdoun~$g9pD+M5aX}gTov5Ws3u}SnW=!Oqn78Gm*-OvKc;&S+HqPL*9y{gyZbE9Q*DYV7o}?&fo1{%-WHA$6$6AM?hb9v@m=un8(zQHtz$L#WHnc4%OB$oFYH>5B<~75%fp9xxEKL$!}apDhf_XRA29))o-Q|d7jd}<cZ8a?_bhdfo_66;ZrfM;{g|(L<<)*CV}0#HF)eHj=oz~NL%>L@q*(}5GnoQf@Yz%!;RLxsZA{3Wk+k|5A4WAtf~8HlpVB1%l6taCOloofhgoVYFL6Mr2q(;@s*Ey0bQCgZbJfki>ztOKeciT!!x|#(DAWIi0bMjxHR(un7Ot!LiH)zF^0w2R?#l1rohIiwk@w_M(~D+2*|?OY6(f>cf@JBOi3!!cvk7gxD%Z-A2<MS{`T^`G+4*eVAI9du>)BVmLw)C2EhL*LdA4h-Lj8VypcHP==I3~adziV-6j7#gp>z5LYjnJt21)yjONvK9Ll2H7m`0Bvfla%otjxi73s68(%`gK5VLwY4(7*z_-&FToZ822E;^-PEujcgZu%JH7W!j=8TtK0#gWmoL(`baHVO239`5})5Q2!~Y5-<YuIY=@>>JMiaar`EExSMz#;I}$dlKN#Zb(#3$6%Bmjnu}i#c$M6D*7@z81&T7iIO}edzN5(qD>6|x(MF^16f?SiTuHIK8o1EDm64}XQqC$VU(Cm<$_QwnlTfZ59iEKsfd9LXIFJ|9+Jg}7FzW-ox{auVijCh&PU@68ylc<iSAP=Z1yqkn)(vdzUYI&?=)VxRQ3KVSb{3RjiYi!LZS~sNpRHjA=mirfsB4LQ&4`xFaydzqxS)L4k~_yOCrNzLCy>zD(M{aRP>#xkHEV!K@Q+}xQ$S3c}3EIl}oP3u`vZBDzN-gk!<4Tw$Rr`2;5|V>$p)$R2WI!Be);7L>H3aBof=ek=>{Cz9b`N8oR`pS}87SDVvv##qPh;c1K>uG3?$Jtzj(}UpQ28)7^1ZZKQhUl%l#~tLlpcZVYf=hpbCr=iCNTGp^tXw3_WA8HzZ23k7oH;&bFEuFg`|#~K52sCnf2X89^^QFH{?aWsPl2rmSTk~LGkXM#+lYO%{{taVK!Eui5-)dAaPD%jC#Z@~3ECX>H(dC0bf#?bI_dt5V<fyaWGF2bsWtS;|J5+1M9NsaJ5aE&z6x)IBUZ%<JRpQdwa;Ue-+rI6m#B`=}oZ%dyP9<5KKII{qB8Su5alrn%To!leYGAL-D=4Z%s31u`I?0C%q&0!tq^R&8837g)O@vr#|#9sr4f^6Gf-5NL=1eq^Rl@vnXLKASBFV9{>ikf68necIHdiFF+u_mQ8CzCNWehlh<u!jlES3DCcRBE-9(@}uQhmWA<ITzWp!U?W0Lk?R@lkLsi<zgdlvAYEh6tdh&zBq{e<0|S0TaKf2>Ff*7JZ^X$D~c;1<J%j@v67bI8Hbc53r<HxG1SPFU&c&{W&<fZc6nJMCQNM=61PlW9jaaO7tPORdafN@szuO&^tS2$l#V^qVw4%qXZxL*?Cx0h)AZtN1?WKVYJ7$t{~=H~qzYNnvf53>9WEGUF3Xxm8+Tn(Djq3cIKeN$IlbnB#GaSnPHS%`RQX@vX+_jM?)20r<T|88z*#x{-5=0vek>PUo%EwFiCT}j_9-#IIb-#czzs%b6E7dkx=J;+CmhaJ{i)<d=$V62&d%D3Vn>*+4APk*5X}_BPU~VHu&i^3C(w`y52LkYb8zeXfGPg5xPuCJh7-G;Xet7ro4g>e7?nk}-7bFhd5ZL01zC74XQFaoedo3o33eK32T{k1-eiXhX6x;KuBgpCX^$boL4<U&uC%+k!!y>mah4MzHczZIT(S@SzNSsyvVOzFtJN}uhN%$@0iMm==H}px_qF9fr2ROIRNuC=y3jzSk<zN`xV_@|u&G`ZpO-jWPLU$%=IiiD;^SsZ5PD&x-vHK_Lehac;#|m@w<hqGWCE{$3V1MIy63d}4HH;>g1LC#TMSj`6%fFD9s=l(Y3N<~Fr=HwOXmT)+bc=xmo}c~e91wZ^&!jDkeKA7SuSs<?dGByk5Py{KQbji1bNnA?=NlB%~bLbE(DIFnuQbG2J=O6^b_!na-E1@#8aY?OE(u)fNUK!<5!#+`S~Y*`ShC_UL3E?MQNbDN}Q{dE}NJisD0_V8yc65-7?rLI*Ztlz~s?hD@vaX;sm@4jE=wOZfZQ9i8O7psmHMbQW_C^as1rPITpEHj!Pdm*oa=W;oL1QFvB4rLSUs}fK^`jsKYULtL=)gqe^Z%8ezwmP(8{0<?NycNH&Nygh1{iwmo=yzK6Hbch6YZtOCyj9;M36-20FW=}{im%s~1hJ*vx51Cxi=;uELt(TeSK-nYB0h4EZKSBY%B=cb>Q^qqUv;W5*aQ6_pxrmmszvhQ_zcMWr}r?S0warAyxeo52sQ#!i`Z`6T<0&12(h^d!`LfC$NTIhGOiw6#)zWkg&n9XQBM1+q-izFciUSIuo06ttAr8S}oZHm5%4$n;a#eNh+=PTtAHx;9yRBYFx{1)DmtULzV&X&iCHgcvz65Ip3%|jcrQ6*^UtzD<h?+1J3eF*2Gp17?sm|}$lkTh8*YN7AOPkAMAA!mb}x_f7wG(Jm&U$WE~xzDvVBw~aM-flb;`mDp^^4U$X6V<2EOY^)LH(pu_1cLsTn?YA?siP(_%&|JgG0)D;|HY}T#WFG?uT*)dr_>4lEm%TVxi;p;a&po9Rij(JcGPYu=b*?|Q%{LaiXde)yf{mdaE^|x;(ZGhcM4#bT)rp_BL3grt|U2b7>IpIl1HR;&poMJeDYKL_f*QFW+56tQ%-JE<7J?pCfV!-a3$)S<FAt54wll0HU*&>blCdrh;aQbs=NLo<d7;za{023%a-2%c}tXbO+hS5RIK`@9@DK^x)2eqTZ-nf_X)uf5M*1MIatW1RWi%EyBfY-HtPWxc*{KGsK6K<M{37ynJyA<+N$91BIek5#HU+#OId6#`8?Go@|c)W<QXm6Y8&Pe20qJ$Ol~78Y}0Q_Wp#D66aK;k<wRi%u2p95&8J`&iZ1<L)O>^``&~wcQlyF<bYeha$jTAm*NtLHP4upcQKp2O&=#lY6s^gch&@mSy@TcTJtffRdC^iOLn{3*Z~rPNu9yL}X@FwJePd)MY6wX*5iOh$@xCL3q3u->xbw?P=(Rh>VXaFJ+u?y~{eP&yjuXN%s`B|HIJz=8#cqJFN+R$0rmH@cf_rK02hg^Z>Ad2(t2^?1=mBtw{f$Q@Y7mFoP!iXaZOR=F+$y}`nU_O?W$`lb2;7c3mNHr&s)W~WfNi->$H-0xqu-svV`tRgGXX|@+zHucN3*(&-}*#!;LZsk!S%!a4?S%_Wo@N!QS0lrUR7Z>5veSC6d7)VRC~&#aEL$EY31A4XUbDaWUtB=2jjrL+hv{PVB~jRq^6_bn#;+Plx??ZP%sswy5zt_3BOom*W*47ejWWtD!=-GZ-WqA^nUX)S_quFc|!~3t4t@nQz8yJP7`~|{o@bdIbraOJgamdHp^tw_?6vP8m4Tz&@a&VFHu|o=rY$SzrBaCZGv5$CI|rNbvTPZG#b{ki6$v>Xg=ZGOt@x+DotH{LDaFP2GF3BS#X`ItCYq4hRL7ITx%@WmPr21Ot8_NtZQI=e518SM&y)V$)@`vLR{cwS0n>Ywuq$x5*sL3ta~bEB^i)`spTL}t<yA+uTf2e5sN=7y8&qPcmvgd5-ZjH2r(`f*yjzkO%YgUE&4Wc#)%>cI?tf`B*1g~mg9>Pat>HM3SsJ$x^^;&3avH-78w9!F$M&-2p25;!r7AnU<N-8{!9l8%M(Y{#X1>@OqJV$Ahg0NUj-Qj3$6+PMUaC={K&_(rX)>!n>-$|_%T2<d$btwI=5DRK-NSvG63u%$wz38N#t}PEb3nK+xXm;^t`}kvZJ)V%%M^*16OVt0kQi!bG0>REY@70q9i$%Ugwe*TK@6-=Pyae=k}I#5&VIx+PF?QXXt*ugLaDZhZe50AWXy@8}_AZKa6U$4>yhDai0&41LMQf_7B;=IDdy&<m&}_)L#4<6`ya_)#KZr9`)n%^A7=Up0N')))
_ACTIONS = _PAYLOAD['base']
_ROUTES = {0: _ACTIONS}
for _rid, _patch in _PAYLOAD['patches'].items():
    _tape = list(_ACTIONS)
    for _at, _action in _patch:
        _tape[_at] = _action
    _ROUTES[int(_rid)] = _tape
del _PAYLOAD
_SHOP_ROUTES = {'BAKERY': 0, 'BRUNCH_SPOT': 0, 'FARMERS_MARKET': 0, 'ICE_CREAM_SHOP': 0, 'PET_CAFE': 0, 'PIZZA_SHOP': 0, 'SMOOTHIE_SHOP': 0, 'YARN_STORE': 0}
_PRODUCTION_ROUTES = {1: 1, 2: 2, 3: 3, 4: 4}
_SETTINGS = {'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'front_run': False, 'budget_guard': True, 'room_guard': True, 'clamp_sells': True, 'dead_stock': True, 'terminal_liquidation': True}


def _router(observation, step, state):
    if not state.get('selected') and step >= 72:
        shops = _get(_get(observation, 'town', {}), 'unlocked_shops', []) or []
        if shops:
            state['route'] = _SHOP_ROUTES.get(shops[0], 0)
            state['selected'] = True
    if step >= 144 and not state.get('production_selected'):
        shops = _get(_get(observation, 'town', {}), 'unlocked_shops', []) or []
        branch = 1 if 'YARN_STORE' in shops else 2 if any(
            s in ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP') for s in shops) else 0
        if branch:
            state['route'] = _PRODUCTION_ROUTES[branch]
        state['production_branch'] = branch
        state['production_selected'] = True
    if step >= 288 and not state.get('crop_selected'):
        if state.get('production_branch') == 2:
            inv = _get(_get(observation, 'market', {}), 'inventory', {}) or {}
            branch = 3 if _get(inv, 'TOMATO', 10000) <= 9916 else 4
            state['route'] = _PRODUCTION_ROUTES[branch]
        state['crop_selected'] = True
    return state.get('route', 0)


_IMPL = make_agent(_ROUTES, router=_router, **_SETTINGS)


def agent(observation, configuration=None):
    # Keep the entry point last: Kaggle selects the last module-level callable.
    try:
        return _IMPL(observation, configuration)
    except Exception:
        return {'farmer': ['PASS'], 'hands': [], 'market': []}
