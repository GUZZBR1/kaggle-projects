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

# --------------------------------------------------------------------------- portfolio
# Tapes: yhay81/shop-router-0908 actions.json (4 x 719); stages from its model.json | chassis layer: sell_lead
# The chassis above is unmodified upstream code; everything below is this project's.
import base64 as _b64
import json as _json
import zlib as _zlib

_TAPES = _json.loads(_zlib.decompress(_b64.b85decode('c-rl~O^+kjwk7soG|oXKnaRrXtggh?6<ShWNTnv)4~2^dxD5kFd+_X;@&3E3ib*me_S$Q$z0b)i!B-<uOcoh&;(Y9n_3>~2_WyqOzyJGx{LlaKAK(2i|MuNK-v9plcOUP*`#=8u|N7tl?@w=hdig*9{XhQC|MCBPdi`(T{q2wc{?C8>_WZ*i-+%b-?z_|9kMBSI_kREJ?%%%q{rL0G+xN1MfBet8<!}D_{M(1W=RazH^W*2g{Qaljj^DX2K7Y;oUw``L{pTO}{`vIX-7dWS``?epe|-MK=Bj^x{$qXBp9b%z@Bix`|9JVT&tLR1nzvhAzFL2JdC!|)x_<C{DXX7cd>#9(zy0yk&p-V0(?>r1@%h%BA3G1~>c=+UB5&~L_un6l`wP#1^H1^boQ}VL`10cW_u`gbKIx9y^^3RT9@oO}$Kwy5{{GAH=jUI+6xog!zk*Nq{OgD7w<Ygvo{qYt`|TxN1{O>u@N1V#JH7vK{B8T{%P^5)|1Y1fWc3TTe|-Dq%V1k`)w;#=d|3VN^@-+Vef!LMgvt*+&Ngdc<A=`U*LlLLFEYpf_P4m6R=<1Mhr@lpe8J-PE?XoR_{;9Hyn-;Hyx$Gu9Upfb=I!sRVcr*pnLY0~+?!9&7<cfT*|?uSUH;*1sPH-iztcZU##=8mb`-`N1Op2WkXIZ~@<3lMK>ciCKyTme3@A8~h6Z%|Q>8B^U$=SDiiOsLoJE*A&H=|Cc#Qgl*<L7ot8rrAF6-rQ#<#@t_xf*N{^Weg^UpsYzyI*h|8o58!%si|^uKPmxa&8;4^{$R5XUFqd5H`*Z^L!>lC&&7`f0sqiAy+Kj_<cm_;!?T163zO%c8(+boreoKMii#*=sJVF(w!3K5E=x{ySkLd;7}mYhLFv!TKG#-s?_to?DZz_O?5W?A6J-8<^+hx8CQotZ}*wJ)6lVU3|iST}u75zk5&>sj#`rl9N1dX+1^Hv3T^dM4KI4S+J<iW%hgW&_{(J_I+|*kOAJLox{V6DkSpy?9qG)2uh;~!o;zwwWcdc=Lbh~G-RX~D{mf^d%@*izVPqwfBSE}dIlNg>n!LbU)FG6FMA-3wV%VHJme&^GDaSp-XQ2*odJ0;l|OHAQas?s!!<ilMS^vYfp2Y%X+rm4P(PHz%Dxa(!CxkY@tnv2#Os_Ah`eq^q7a(w%cTezi?Ak%^{UnhNTU&PB8PThq55C_t>V5m>vvF@C>}7`i{4`ZTSn#Njbk1!_%;@+L#B5~s%H_hb5)B*XWe?H?LStYQ@lrf&X%jS@z`5-uJCPbyRzm{z#4eBS7fMr(MSmJH^T`|h`DhIx;Jae6hcNmLG>Z%eK)KcwgREO|5I$^fDzF?i-^VpOO!Wt?q9^?Y2;zl4g7@>f6k8}SQK{q-W0zgzu$f~m%#;%Nb+lqV;@9q#t(JExD2aO4(lHKVO^n<Gpn>j;~l>#GBe6*1y|QfuvNs66|y+=dGDqdTy45&bE_nI$l9wpf$!UvF-jo_sDU)Xs`9kEjyZ@#cu+Mto{fP>)-~zGC+HNX4KueBLvoMn6QwP+?lu8x0c4hd8@Zc1e^yTtHCgFYa(2+T29p^A;8_E`Oj5T5KV+17oZc(@KKH`wMfk#9kSb*wJ$7z_{LT-*J^!N`n1Br6v0u&Nb<nXkdH3h#vS~qlz+>3NcstcLzWu~U5iag9$R>ulokkznMJ`(yyrpE1nN%DcYSLZ*aU7!Ys$Yg}vQ9BF$fyc39Nb;EoNThxBIoPZZNU`I_W|7M?VkB;N>=&enEw64Z|_fkJO1|De+N?=<pApU#uIyRzo0rH8gK=iSS)ug2E_~J;}u`elDuF%+(W%Z_&k(fKI2L>;$6D`Q&wXYJmD$TlpKz`eA>MLh1IZ|PdS^4{ucK#0|(pKFdk`u>5}^yL+Z7<*MdY>qQzA^g)kssr+5lZF2ZTImv(#Zus<SE(wi&4o{|Q>y0pZuUz`?%?qDc@_J!I?T&|2X9J*@))8pEV5dygN__yMHf<5d~WqyACG;a>c?=3h_`262y?Kpz|@*DSW7A#l~_I>4=e%eHSP<+(ezot<}9E#f`NbXUEKG!cu`UD-|d+{DZV*+$|NM3D2o}ExJ;?&v2TmvS+odrquu6btMa{Q#Ilp~i++R(j48(K9&a-7}rtvE200P2L=@zTJq<DfJci8<wR-1(VEyil;|Z?W}8{DG*WJ$eQxx6}56WRYs}3%n<~0M!<U9`$BdGeiG73!}kOJsvUIfEAzL6nE2<X_Lm#=;|7XI*{+uJwmh-lc%(Ik(6SdB~OZ>Y{&{-M2@utjgcm4e(7U#w#C4Ag?#~R5C{~~S#CS`L8b&&`RHgjvHs}1U6wMo)l$sU#Kt*E3d+OjV}Yi>xs11oPRcTD7F)x$gzh1WtQvF(LSz2Kf-2qC_YW`BO(dgKszApY@nRP_@`JXUz=3KVj$>~<2vmxp|3dfb;v<m->26LH<I8NMc;<9x?l=~>I~l>4)NF&)DaCLQ@Ww+XKU$`t4B1%Srr##jx#eFegwDK7OW#8*!x*7E%*;(eV@DF1dm~R4DAdc9<s&BpOnQ!@AEmNS`fRUd1<n}JwRe63i1U?F!@Z^>8#W%9Z}-|wre7pAu<Qa|(Ps0X`fym34U$GNINgcl3&QB`9=QBM69;RuxtVJYyPjKcVtqFBo(0&`MRe4wWW&wW5xNyER#F3R@guvCEdyCVl2#GybuO}EKA3VE1)zYXeX|7+x_c!~o+mB20v*v_m&w&Aqvuw+D?7NrAFt~sFW)x75xfk%yk=04jRRS_ifhD!e)`sOd^uu&`RV8X`qIJDAeH<Xp1<aPmo}pgC|ka2pVk^Uu@4wqe4w5jbWYQh<o1uvO835orBiXWDmceZ+3l9L@l2;gj!x&ed^j+imFHw{v=%wAULsfx8vszHfw$L{otRyM<2;aiZqJWZz(+tspeqfAB<A2e5ia+r>d1B<Iv4K(YzIR2lwK>TX5ro469VopRFh&MV|WS<8ZNfoE(rjq)F^GMgPmcDt6|yD&cTajP&b(u1s(xof`&rKthpT#5BTw6K;QMx=b@gVJDaPNZk`?y2F{+dj`t|;kgXr%kHa!XfHFq3oiqV<_pyoN#C@*xjAPg2Ux8G8hQXCJ9yH3cz@q3C!dz4l;16H5-PRGC(<sb4MPNY>D~Q#2Sk5H*sG`T>dNi(a$Ka{kj-w~dIjR9`6Hh>t7!&9Cz+#+LltF-$Sd}>`-QF455s3n0YN0Z?Sj1D|R+ptoaF(~783(V|Xlb*F&dHb(Jrvq2^iid99+CwOlE*dj_kl}C_S{3LxRG09DhBPeVG0223I=M)JZ(CHPh|5-H}B49#{OlYq29HTU<0gc6TErV$jJ*`L@%bR+{5rhRNH)6{%D{wM&mmqJ`iJdxkrIf!8<iOtSd0u`YiEqiwZ>p2B&o%y3?IDc_^M#RzC|+R>&)I+tx&~Ph)8FuAA9$WYrwXYVonnD!;r=p6hYVqL_M?2kAdqN0QH5%VEV&0Uw8<pOp&6w_yj4AV0|qwto0wFKqsPe187@D0^D_!d(=FQfVUk*wAW+`zmlp{5p38wjRHR$G~px1(4EGilI7>`+&X?W}Y%)06#t?HIWcG`;1Uk{?9&(_j4c*p{|e67n3H%ksw320i2Pbb~G0#I@P2_u<ECy7*M<_OcIF|2;qeE;?Z_MaB&PnSo{OLupaon{Fqr8-M%?tU4;v#1BCto{SqM2ZSsdNMt2YX)=eB!mlp??BELg#Kj%3eyT|)o1<8PNS9H}BU(9Ic+wtj5*+=Uv@UTzk;6&b(4FHdDqRZXLdtCvCoW{299VGkPnUDDW^Hy3$hUyVH^fG?N3I1p%pj=X7bLo7Z=1^e(d6S7Ow*pQkuOP0nrz(&XIav-B9O4AkeDvnRBXr@DCe=AlBHdW(`QaM%cfW&M{B2*n-pOVjQgA4!pQsyS_jA6~cWs<~oB@~nylsZ8kqlXqfV)PGBF`f?0g?_<jo5=rn4MACHB{ZQG2+Grchl@=Bmd5NG>R^`c`-+eLR#2T6|L|$(85%$qo&`j^P)yPl=Y#o@rx)fk-FIr6^a-~2nDcgEc*2=F3R&#J(8e=iU<gWB7+`Hc!w#N&yw1jfFzBb<>mGVPGzmvwa*bMlC6}ZJ;*t?FThPGkT)idx8qK3oEuurY*`vxMwEyz$&T&fWDbW)Mef6BG2c`x<Mtc%TbDT#pF)<v?t;KEzJyHeJ<e)PwB;E7yr47WPBP|3<(EMzDn~Y&3mBuj5o|xm>QH_Uc-!_arVqhsfPYX;SNL`6>@4J0q-<^LnRzj>Zw}9ir?D`ADm`F0B=Ufz?A)X)?tBuhz1_3>xRza2jR{M$@x{SdXKI(1>#45=W@3=#nj!72J{5zZ=yBJ;LOPfmz+6thm{LFly}OSwYr#CfH@Vo(oI-Ozv%v36%5+V_UN<arv$#8@;i2h9eIolw8vEewIyG19xK56OqAX~gnkWK`C*<Nx)>}*?s4jAT55~Scrf0zB12sXY>;_t(YC!S8Sd^nX!Ji9b1OXll^`T)o=!1gXhl(i=wH6ao>87%_6+11kVq<uSQ6At-F^5M&7!-;aw50q`vV$b)%3L`Gm2|)(Bv54`rr7y{%&(B}0Ruivw)iI>v<l}l$TlbkD*|FpbG#_*NhM=fV#=*&I~*iAnb>B4?K<25o2W6bbx7zQMcZFShq!YpT6>pq{_zmn3W$Pwn-k0(+uNS)1<CiBc~PjkV33Ei*cnl4>JFp;1sFFMaAhs;XfP=DWX$lA1-{m+%r{W4@Wi{6iujCcx2-Kz{z>^U(>P^-s%Mbosj5Uv%nuyL@i*c%=FaN1HDOOV)+I92l!m&wq=xt_B5&b01oT1cNxGY}>z;;P=-?XqsU*s(-o93939u!xFP*OoTrq-u?2;KM14}Rx4eB;zSM^X<yHi9ts<1%E)yRHpF(SnZ3)Vr_G;T(zjHiImdSdgGxFn*_2OyeYENuO|BFh~t3%x6=JdGZn-fWtn?;H`CF_*jI6yp4vcu^Jzf;A6lE1qH?N`N4Myt6xEb#W1`>Qu)!ruoa5uE+(6G{>2quL{~5$h?osv(#&1Q`u#Ens!%`rvq({oC_jo%J^{@J0(r}TtZ;9O<Fs4qhhlI4M_H>=0=UzNH?ESL4x&{klcT(ZpI`%nz^=kgva8O)|EX55o5eh-ihENBXUJH>FcjR)rqp`5(sK#9XO18+T8I4+It?yMKnyILCK=auh^@Mvl?u}DX(-VdLr=ikU<Rd=y$}$mSf&`R$CL!MRxyGz=SA<Bq8Uzow1kar;>+1F+5c4B99@<Z#ZUjKrw^+ScB1!<$cA3A`ff96b)&I)__w%EJKMz{TYy#5mwKp*?MT2AKgUyEJEi?t2jQw0`-U7#lEdz!5Af=qyY=?x?<z1RL2euGRMoZ?{ZYc&VL6RRDh{(ZfNf6P`G(-L6tz~oj{Yd#JFe)P04G$67+CnI6~Uqpr|P~Ku?tuU>CfmwkI>U)2o4>q1Vy!)`Dp~IkGZryJIuGQ4;SZnE}oYreYne%r7TfQ9UqyzHIKHj~4yoOi-(h^YI-OhF!pU<%mr+4{(^JuWYYX<&x{%(uz^Wc6NLEnIB@hYhpi6zapX~f2ZSY>;I^b$3Cb=>G8)OU&6_+guM-HP|%#FdN_>V3bNC;l*x_r)rXcIUalawrXmMTKCj7WiMmt*c!NW|Q<ulP)<!qH6xR?4Dw$Wb(=D%pxG}{%HmX+85?a`|2ErBF?>CB7DE}j>S?!C>$^EY;TmhTzFr(xpu1nbEf-+f+t{{BKsEC<D$(+y;VJ>p9sdX?`@pCAg`OID&#bEI#d}#L3J?i6BUXKN^VH_hH_}Qw)Jl$8So2F@PJ{3SpAxb)4m`vs_VTd8`t@x~1ab|I+RM@JWQi8OMl4W=kxr6c~#WA^2+X*q#PCUz)Jr-+?zDdj}F9UYyB5~XI^-O;F=|`}DERCK<d_q?<OV*_zT95o^OUA5+$F=JgdyjD9oZjMI-vof~v1ic*pm4NQxqJX=eF8|`Dv;BiSM}&+(}a}8cu2TZ6nL7Br7Am-bA5li=MHw(yd<!jRuV|T(^T7R00rzjoTHSSRU$I|uT|vrrcrRH0Y=#w$I@Ro2DhZcDF>7eNQ?FBl~4pls{u&k@~6DZZ};vB7gzx5fJ#0%X9~tQL~E}K=#N8#2r(h!1y>ysma6W(Ff{O~yS8zmLWJ19iilB*oqUgk3s5SjFb;SlRi?^SC$mNZDY)txPQXR;Mz1sW0)`+;6B_;qu2A)81YIRATsF@Phudy7?IelnI99b9$c|(|GnVC@Mm(qOEeK3Mof*0=v0_7^CG1F0xk`~Qg6IcP3^=zfqWlTb{m`7;jF_;TChXs=)j1ADeUeHI#RaZ7XkCg<^K|Lr-4x}lm?jeahSEKqul`VCKeEgnP27V{(-3QmY?5JFSeqnliRTwg3`m7nL+*nsfT1fDzTG0@86d)Q{t>NJ`(a$S=7QP-XhU`35|<(&+ku?`GLtSNJ0~!As-P#*y4`UARWS`MF^y7C=>(jdLd(J)<IkXg#!3f~a}a_(%{NFe?qBLnhlE`4w0M6ZlNImWu~1=0gCq5}lTi@u*cd8)xi*$n^fBo4k4d`Sxj5FifO{PKT<Rk{Nhyo*K^-aZUf#A1SKgK?ec*`eG?x8dS+D35lSqd(nRQCEU+4^~J4|yKSJFDrb6o3;?154N;<f<GCq@a-Z;qUc-G)>g*Rezn%!>eIm4)2_7)Dj;Oa?Vg!6XccD5%0aS%o#F@W#ltJ6h*vI%&*txjWI7AXkP-F?lG0>FbOob!>He3nk^<WL5U$3782yEkDs|LblQw7oA23_@vCzlGt>x<hR@Q4=fv}6xP^as30*#`-6*TQ{s22uTT-ABZa55)<N~+V}z_6kNvanU=}z?ogjji(>gDg<V_21Mz3jmp2Lzsm7Gt|WtPUmrkd1VdvS!LFBLIOlPar9t&UlIa9BtDqr|&h{>iNr4^YEv-bVqG@l8t@aS?$mJxJ_A_imG@;M>WOzQzjUv6}%5vCQ0AXEN)6NyG9I7=%498eb5MCN3m|SKX^(sxee`moTXHB?*K+ggN?BQD9sJMd7u2&NQDfHQAg3I0vQh#$Z~AD(XHp;1W~|%g<_9JCg@+MH?{=<tRK^YFJS=&2~9Fl2Xl#t3*x*aVkW)tO-Y^{cl#HDunc>`2uIW;K1Cd<POG>R!uYtU6^tJ6Vf}Y*E5Zoq=Za`$BsHT?+In3y0>#>81R*`+0Xh|*U&gU+gnC{#_BY9GNP{Q(leUtk)0jF-Umps$5KNv6+I;7Hn(i5X{DeVdK?r+q*4@`+JKQhV7EXzORO~1-28+i9E8whJkkj4jg16EqA@@;h3&AW>zPAfAm_MH(701BO=??QM)tfL!nPux!WP#$gYzZ(q^%={UKx<MAw@{!%Dn*|h%o+}R!F25fq`Ctc|WiH>k`ws#IY=QWN=~d{=Uc>3gtdSb;A-yf(m?oT2g2t=H)D=u7{NE(9?8OL`x)}7}VNSeCiWCA~vn!R<lvZ@{(af52GiG;|gX%1?By*rUj!dla88D8}U@;O27`8oq^M>)|+iA&w)jxf2<JMk`gZ<RXJ2DMxV<fkycPe*k_*VpjdSoaKQ5Am21%D7iTCLiUs3I4g<H~OC$=rBcOCiiD&y=#fq^5DrRUdM^CiFt*gi=v%)Z`6%=64St)#7_HdjFSIg%pBpie;cKTduV1eZ#4k_lYreVSym?+NkOl2x6F|qbELx!L-mYIbvlh9Rmn!Nw`vG4#eBnXLf$yqGRUVUH`+aZ`fp+Q_ix&$Li4S696NLlklI$BA&Q|9TTPdAZ(tcbtJ^Gh)0$>MY5Rw>fL97rX*Ubda^Y6<tRUQ3{scrZUbaBc|mG~{|4t|6dcmW&F3Vx<rhg@J0IiSh`@Ow&ZYZozmu8sHI&M@@x!XivA%GgN3`*m9NVPXKN^N<~r_@+JaSqI<#-pDdf_hI*mUCHS&nbIg>RbM?c08sv4d@MbZ9`Frzm7oMI;`>U4&)KE22PK*N4Ph)r~s~uj=`e7E$+Wc~sA9M#uAfHLfcj5vhHZZAOnXrqfKIK`au|3NN+Wjo`LCO4pozXdFBaDg8aQgI2BJ%uQ)LoKo$C*m?(keu-DanGz^v?h*Qkucw@cGqy&R1jTL7e0=kfbMHSc;g?jFeA)StQoBG)ZlzVIB{xw>*f9fG1G(;f&BRpwfY`{z%2H&U#HHb%=0Vm&BCQ4b}ceR-pG(3{eQ)L^AqetoodbwUTW7(VQJVXQdA4z-M9{D-ZP6-OLpjoYq$gC2YUig5=*g>;|YM@RH1mtg%EfoPTon^$0QCyMyaN7$}Lpsz=-VH125h9HM(^F9C{)gy4GT!WshIT)HY{1wweTVh1(Fl4=#5ib_Y5Lhog~w7Xo_>FBc5;ea#uf+2N!_t$6^gF>@@--RqI)ZGjSqm~c5>r}m+3GM-Jugc1L%W`E8Umo7m&{PML(5Xal^a7J3=y<{F@DS9`lC6hqrl(oc-@|cG{zwbBG|{}lhb7=Ta?spI$N5zwPi;cJkbf1VjBCMs`v>s>=^;CN)4GvgP-A9DOFpeg!q+*UB!oK=c`t7Hr=kauu~_4j?`it7G7C|9C5`X-UKKuTjGK(4B9~KDZ3M^Uply3|P%gjwFZZQSS64H{^>ZQCMq*Vh;2<xLWK^)HYOz2r#V4j($~{xo1gx>BMhX)`KC#rHBJ=~8AJhd=Be9b8p9z;#gi*^1Bb(^-wV^Ln;}r{(v6s98(`Y7AlK>>B2yNkt3AUB3OD+*SmO@#99so4>BA{CG4YqH`zHm*cERso6G5v_pA8LnA53S7#4kd~(3Bv#ww%qQg<2rCs$Y`*m+lq$};UbGDWH@YV0nUf~)F9B=4l_MtEx?vHQ|ZXtiX8NwZ;F(urDl3waFc8K-N!;&6(>2<?qo`N)5;vBmEmjM@NTym5SFP#JR#_nB~@|3;c79B2h!pf5IE@3mbIk|)zw`E#K&YZ(u+Y2?F>{PBhbeZwA>T6u~gJM(GaXp$kRo-RB0V`IgI;0q(Z<yj)tdhua#`5T+@h@0;T0xUsB_2k1^!?*;vNV7<4kp?!ko9n+dtp=t893+*r`_VIf)9(^|bC(S#t37+a{^gJ<5Ejb64H>-(XzMgx3nTEQJLk5UY$v!%zc?!BUfMO{74ha|P;bNdTS<B8u{v7m4=g#Ou4#}OS)HJn}^!@O~YC33c`>SW}fb_|6p%IMsQL!J1B>ft1q2kGvBzz85jDPE>2adC3T$=1D-HpeE9=YFJj$pkm>cnfUPsV3Ut$amYQeq+SN{rV<fCF>g$pv75!`BVYg<ieM2nDX)WhBKUc7JfEtO@1oycB)%G(WhfNAaq%2g!aJD9%|^RGHH8~gSB}ZlnB2dm2@GDB4#!<Y~EP{73s|6ZQ_R{S7fMmvkkeGe;E)fCf(DR!kJE)b}xQc$a?A>+*qb`9nTAtnK)r`^ncwEf>M4wq*70TgP%SX;2zZ>C)$sf7G+@<G_t`0K{wwQx2dnWxlsLc+Gk|#f5&Q0T6_x@#$`vi{1-1M^O@5f?Fv5%6$K;ib_T~To)DHLWlOW2`m=gxsW76T6gBZ#F_AkpkIS?92CAf&4N@qI?321y)C$RM{=8&6GF6HN4}clrWE`N;8E)MdQ`rGfE&hn@O2SCTnNr9p@A(TQ+LW(cZ-}xB$InEnDuGDLsHwE*jZE`ByHH<MqvrO)qs~Qr9nS%Qm(~`Yxvp?lsqRpWI6I%I@l0@=pfOPdwXBDF`+wVhM|{!DUwPTX!uWGjW%8nyyRs~V5t&Xd8>ipdV5#oQz(4hK-P*Ne@)1A@)Ax;*03Qmh%x#lvyGGnVTl+A>sEJZFPhR^OwyPhh1y^jBLz?QQH}L6Oe|tvz$YpiDd_Xq!x%HWvqc9P+RC%`^Qt1te<ZF$advawe1S(ahgpN}bHF#N1mxLaG=bVL4G7&Rlg*WOmXiVOL(j011C5atlM}qmFw~y)#kRuagtkz4oBc;Dt!ZV^KQPqbcsGuQ$xBZ;j6FPK=vhc>hSQtxIo#m+5Q7SrtXS;n%7PB{;gmEazgjbqWa*yd0;+@0CF)i2C<hlP^V3S>*k_qz{SZ?9IFR4SLaf7@BvnznLMgC8Y-`q-N*FmD}G<q8%3>YMjS39#?Z(J)dSs`rnf=*Lr_&cJ1g7?aeEp|=Z7Sw}eE7J)g3r?h<a;mG#!)dC&&@dqFa?$0<YewyB>G}fJD=U!P8T?5Ag>ju97_8?qOLnyuu!M;w>)|B?Dil6N2`QcBvFFpg=Fm1?geyM2`}I~X0jMc3G6hKr40U>uw0B8X05eK)WBC|BO&Hc#B#i1H-~bfo(By$F*5g7pyPVWqNDl<<q;P%}Y^yMUMeSRem4PY&xkS2~JB&P*&tOxM__;Wb^q`*eyyna?3!!XLg4-xGQ=XU?OtThNFm|Exxb%<u!Mq)>q)J8{<D8lx$7Z<{c~@4qlZfi;9`p6m4AhrMVD<5CRG?dsZN1#n-Y?E9F2q$-4*RrMco83W5yEdn5#!yTxJHvyk+z5u!yRBUq$REMC>bzIE98M;Ta?@GVXUZP3PmuG#mT8!oQ{s8IUE_g)-vH<qMLAR^NAW!+M4`2ci{KS0N#MwaoO@ChGYQ)yObmYkfYS*P?=Hr;yF>?E++ZbxacpU>4w@%0^9MB7bD5CX${g*f9Q0t3n{gOzd(g7W8z|(6+sxa#g>uB9VwuIK#kZx8&ro++0h^xfN90HK<_6n@vl98<|fO!sJ3CbG1l+woQ(*DKrv`>a+ngo6bkhv8-3e08$ep?HhYStDuFfM%=EpoC6hxIDN)HIwN%uies!60RGxpb`>3zV7*(jGT@e~t4CSe?`Mu<lLNp!Kf_50Kt9bQX*&@HQ*NO^ncxJ^F>yJzc-=S16r{j~g3laI>q@IDcNp~<gFU(Kq)!(U2&iUb+I3z@&AX}wFo?`zV>|h<P)zl)$n9_-hKAFq*@x5F?eh>3YSqAXx2dU5~Q>gk<Ldo*(hk)aHyPn~?sB(2+H8Xo+lfhklAWEeVi1D2`@9kSFTi7soEVn^plClY_=&rBCqEkI)dV1^0rzizBgFBibLX9KVD&jjy)*Gq{#fj7tfsa|NtwB?9W?`U;IUJjkRVRvt7SL^G)m#xeK7XaJOYb@fAl1<ls+<9tg%7u5TgX7Q0xaC4^uQ(P;YYxyG73Pcqg_~o07MjbbSzO7otT*v{v?oHi76NtSZRG)B$R;B2n#Q$eMomK&rqi$G)go)*b-Vq<{o^VCT$aN3X~*Rf7O#s=4hNk4}|OJ5$~cN{L>_((LAz1QIE<36lcd>ga9YbscxGsYFRM@z#j9=>WtGB2i=l`iA_<nv9DJm!#7DM6UwM_^<DFdRzO8n-j84XP*7!ytrw~*6P}L)4Ki#b-n@wew0`rt>wbQ_&sz2fTv|4z-m4zG$8A1+sCe7#-h2yh8`7;#%LIplv9Kxe1{k<0O=|NXc0h4xXe73xN%2l0Gnruk;|SJq6WEq8huuUJOVshB?#L0iC{GsFGl4<=-~RaN=O6z0{qxI#<QXJKbYkJc$`)R>ID{)$KpLMr9Z67JFo?yn0AHcFYY703QYe5303HCSYV)@$?!hG`(=(?KCL!SLCdlZuTuWAygh&ELc7_UWb{K=4fbuLUoY{zVSB0*p)>J?NWy}ySzjT8Q8<IeqlWVWrb`_@I$;c++pNdbPbwZ^x?x5%rFIL%68gGtL_`mdumU=n1EbqV#GCOQ)9cGl2l^9yS|JCn<fglX0vin_@r4qscR|<KhImf`Gl=DM!U$XzyFCT=<Y+Si5Hq73Ud-%+`R2O-QBGH>)b?>825q`Bj4eex?yF-aEI2EZ!_}oPUW*v8Wi;wI}NB{DZtcHatN3Xqz((c%DzCC36r}4$=A11e4URI<+avR>FG}h%}q9g-(as4p-s=?LOx=TxG_eD+R@apBAlf`O07J@@Z;p7_4?rHs$`3y~<B$d5@Y2}8hDp|tOo3d5mNwHwS4H`}vtDsho=N%o^^%t<^_4Zp$HYHNAj7I<mq`Wjy1;OF<iKH1el0x@ZXh+`ERaBj0-fr$Te#D~%=XE^G(+~A0ntrm@bh_ixJ|&-25Kh=J9}lCzKi!<uHJMlDY_3T5@RrhA(uBgroH~mIIlP>l54C7s%sJx7Bbz<7@pBx&*;2SpDq!z+s^d*T^C&3MB?62u7vN*YaJm5QF-EZ~wAh#5HFY^IjQu-LXip4Hp$I9?R$AL<jNHv2b<?cd+aI2PdH>-#yuFs=T(@|SKR^FU0)Ej9eknAGOrn(5TH`D9;lOkFYlvyQPo&`g8s9j+0<Ii4c6pX=`ze<TB2|EYtsw^?Jt>|*Hk3KQ*^7UbkzO|u&;J-v>Dhq>z9Ow7|Mdh4rcrD^Sa*N6gT8)uY|N9<#gAg~%OC&q)BC=d(Yh{n`E~%9y5Gk#+U-y3aHP{J|K_?=`sc5C|Lae`y#F$W&!>gg!u9Rn|9(9F!(%C3QB|M6D(U9|4Az%VGZ4Y$gXc?0Dq{4v&akFWANlZyf+`U)sm-^@8@%lB;{Gtz_V!OjV^pHASaFkm@pjx(;QY&$6sE{_y!aJd5U}TOOWvWf+3}L@v$F(DCGcwuc_I^ZpsNHL#WAWSbJe;<B9BDII>aU2hn~yx(SeO05*}XU39r7$9DiGDvEYJ%dW6dQrT)7)29*pm=bgo2-WP_MJ?~s6_2tu3Jlo=P9-uCzPAxg8b>hGq2vjoOdZE=&yI^2b4g6ObQ1U<(88NlWP6rflIP{a9HlU0xF%qAXczUvgMFHa<;-{LSRzakqbYfd-k-kX8hD$r*s3EBIe!%NXCIDbkMaS_zO<atUcW$QQWN29wn2j#K(*c7SvQT4kk?y0$4d%ZSMzXiB2pjU@%gp6zde=)V+$UTu(_Qkvr6`Ozbj6HL+c;f@p3UTwP9jDAB`>9V+JEk277WuSiBhq8iXq7xj$W2%8y3L3s!S65J$dM(LJ<2tIWNcnr+u~N@U|%D_GoqhCMQR9w{o@CbS;>s6-RS4WTY3{L9j8lgYBz)U)U6obB&#RS;Gy0N97x^p92#O(2Fs~$b-`x@eUrWV5%e}_JA7?wm<H=$H2F?#x$XOu%%>B_`)2iV>~A^02!}hRte!%DiVdzWIsVovxNZfg(bvcfx^s<0Hsp>ul`nXUz_zi+?ikiF-abS;dfO!T0HHWe$l@p&TM$Jb3f@WeTtC}%GFu|du_=DHXC?cnBRze^Jv862ESfhg6_?lGKG+lPf&dbdfyGJhOIzo@Bb9nn*$NiK8uLP14~aJzgitl@WQSSU{PY3{G1;_uqZ70B?s7r{C@k{07_`m<QhEoLDXjaP$!Jbuqx%S?y(=%6*@VyN=qk0U#BtuN207&aK#K7v?y)K_+w6)gelSvS4pTRUZdv3RMI;oCy$voJve|WnQ3_Nit%g=M0}5i3MrGw8FV@^B=^W=A!j6GpcX)83AmBFx$}qWT*#^9?4UrnQ|X0qVao0kPFX2lnaAn9vhQ;*yk3Ma+y$vprqN^PCdlt(tc+p?@Yt_r@jB>Oo4ot;_ciSdGwuS90ouS&574VQt_T-*7-W;GNtMDFBL53-$@k~%6bFZzbf?6#a!S=N!!|X=%emtFXmA&WEjN>;$)g7%Z1Vf4yoc1SL#upoOs{l|jlx|)C$GJ~5S59fHY(>2!->Um=VDO2U_M^)^(@H?#=||-4OP&3#+7KqyLA7jtj4NPes5P(ayahtY4-vY*PXENl(VVmZ*fr>q0`2O@kj$qm)y@7Qm@s$79_e?RrPXh+cIT#yXm(@T-7AWHA;GO<(aviVq(c924v2Gs&@<pirToYk(v>3S(7@hO=3C?w61Tl)TjpVnq+&B+S<zbf$B)U&}o_M3Cwe@T+>gR$PbE-isk5xJW$EW%g`rE=j6;)cLa*}5E>Iq*d}|&NUNPtG2+zO#asg>z?}t2_O5wm1kU-ksFWj@Oxn=BMH^Z*LUNql@~t>9lmP04+VRq;uLRxoQWA5@<+$@Rk$9nC(?=eABK{yUu|;}DDub**BN>ZSlV9LH(FLfsIP|DDyP6sL-*w#+mr5KYVzdD(KEEmMrYY0LP=92G?EYlp;-a~8ob{CUE|OBrv*bxJlnq&-i^#E-pm~lfO8-sdy6a-#yTZO;+7on^+s=KEDS=f!I@(RFKRR!hE&H}BdpXxl>?>Nd`y_qSbe-piLfYj;!{z?tBqlBOj<0@xQi+^pb9wmF<MFcGEf&NJ_yN0(N>fE>o2g5@b;VKj<4H7L%fwn_T$XO#dD~Pyl?*~f5{qcyZ1@h=BQmGwQa;?7W^DuAnC(U&*+e4mTL~XyhIpFYU3fuEma_Fg191=b|6)sb=hx?p+V%{v#LL&URtm&s#|4y!-X$k;BaOKqrG!9@M>Jj*ZmKteUC-xQ6*X70ygj&dURR1Qt;gntm)Au}ScPeu#>Kl87iNmEapqFKKDyIN3KPU%bUVhaw1xn{^Sug&sCC>kb>601(|GH=G!l$6O+i9Eg{I8U$e2D-X6cm_kM4->(zod_W@#hr=RsR%z>q967)N01;E;$J5v_lDr-L&<G529!r>)=J=n3zvtO&nNx6aHRnHbvM@6v|bK~@N4yA7!5ek|ySFx0P;<XNU8g?YTMXq0WD)AL}};!}BzUW*_WL}-JjHg>YGO&A$;GV_SEtk1MBW6*hh;TF0gy0NG<%gc8HLYe?W1_raQ(pV!KZoRMMn`CmzXjb@?<>pAUpld8E05jRYjmluZ+Pv09bnI2v!TB#tm_x(V@kh}5tet%lAb^PkC-cv1Y?A`-%EDBOJXV<aE>K#PGPs=*>C}~T4=ci?da5Da0A<h)B`+pCC+m?a^pz$Z$L))KlNcXVs@~k%RH-zu8`Xx*Pu&nC7nA(Wu_{r~y~wj5zciHLRv1bH_PY1Gw9oQNZo7!$kFsKrpP*w0rrDkmZ><SS6is4JGybV$66_;$0m>-=b3wU&%0;N2CAcIzx2|-6?S`k!UcX``CSG)2;V_%znq%(ID{xeU94E%ExfgU(?SL}PRAbvF-?yn(osv6vYs_z&OL|=|1tByso@fC|f08zvMo=hx@4U&zI(Q<xRM<LTA{2L695KrYkSC_Khpcv6f*K<)eC0uZO;D^IorM0?FzhOkle&Wv2L+0IXQH!YR&q&sL+dzu+NbfhSOyeKX)(NM)Xg4ueLZ+{uty;zkU+1!o#iaUt^be|b!J@WS}5=)&F0W5cE-k=Q2a8rL*+(tqC9HwDj$t$e<S-fa>+kkBeem<B`+9Fk>e02z=CU+Gmy4=VkAW<v-?VuF(-zu?klA0fX27ksOCflPKl9$B4oODa^BP`TC~Kn*I?J(hT^5`1K}C|Ifi<T<&?Ipn019!+6e2gR`k4_^NL+AX4k;dF)x+8*xMbz;A3#Z<?|U5<NAFG>n!{#xVs24Uj760UgQKXON|zP`eO9=@X_~$U0wp3;QU5NHBnX6j2j^Ul=~4ZI0Xmu2TYE3M$9*E_AudI9h8^ENu#J19%-VobqfQxBRV(?_4XcOBgaueHy#<DXpu<vitB%zb-=hB$N3_^f8Htz@ik6}m581sh$>8EG23z3lcJc@lun4Kq;W!y!U73z8eA=p&FodwRu^CZLjtxhT9kuwvbr@^YS|(X%W&fOumRhLc=|%rkbSth&fEU|fCM7u*$L4#3f-~-qv_f`;=LPj4%VYc20M0yqH4nwr`}pU0}v<Q3x$EEt*`T<$dpV_{ozo4YIXKk@f~VK?#neAcy*6dLZr`a=CQg{N|{lpQtYO)7*eVHui%IhrAUiMAdCj_r);c{w3t^q0D5#8q<VK&l3gft)CocZY}crNJQYE_4jT>%N-Q~Lq6M<~cM7gSA`lWz9LC75g^p@Ln+D|*F&kye!=Hae0`Jhu$!njpIF4ZLs8y`yD}`lfzQypo0#)ML0+CZRqJPUSm6b(A%IQ)|p90CF4cBIbJZg8viA)`iNzp9JtsTy5xlq7ZN8FMETvtTy$!TY1sk@Q|9EuzAoJL(N`KJ|cD{#eRb1bAYjBd=$;_MQ^;0k8@6(c&>>9b8uDAmh+aXTsoNY4{A9|r-ChV>v`wN--~DlJp41CS`40ueOiBkpG|Ok@UC1Wa|JoO+TDN3bR5%oGMVf^!CV1(!~zVI2l<Zi6dkXOmjhn};)O*o-Q?vA|V6dbUnHwFhrirdTb>__zb{c>MUMM(9|A2al$fUj9K!cf<v+hg!#{Cs9{)24g%qh_$4MXmfamDIFk~_CL9eG!5Z~GtB&<W`Yv_u_YrRv$YNKy+R5nEFgy<B#U-%KF8_AZ3F<PdXBAzJ*oUmC|;SK?O23FO(wP(VCRuy%D=A^2jjG%tt+FIo6>DZ_bvnP#tTBsW;&-Vwglts8EQxUe4l9s%!m~tE|^jdJfY#bnJP%t<L1&X)f6z&_H*^b;+x4@eZGM((GGg4Ao`4Jw_Q4w#5a{FZw@sni2~$&yZ|D-QHkzAGysm{_#5#WbCdYV^s)GZ>_TS?wX3TttOzBwSAqyIQV7vONUwVuK4CK1!}oYc3D(<hoMjI3E9xKud6_Y61a)@aoouP0bEQ3SG0fu&q@0CK$R~`VJ=Sm-^^?!qRg#3>=>5^>ToAA!<ovvAs+y~LIM^!_P@4Jj{AUI|)rN$J%r=Gec}*W<{!G&UjDk3I-t$)zYkQSJ9!gn~rH4ieui9G$YafzH3qCUd40+lFdJI$JA7f}MQYR!YU;w8ABRzGqpV7UtQ*HbJ4bXV`x-C6VZ~38<B@O<2BA;l&Qsz5Cp84TxQ~r?A42dABnZ*p7QV$A!fULM9U1u4w!sC`CE6qcyCdO%DHDW9B_2(U(_6U}g!|SOLh@Am*-bdN_-7hYwqe==%lUrfCFiWlDi;h>d&^hX*(ncbG$t5$5z^~Y*1?deJCWeVK>y^1odssPm$J~e$`T;ksJ7ylsivX6Mj1=xJ$nv9+vsvyy)dCpL;tK3~ME09Mh92SQ{=kYOrSyv0MFv{tZPcX}fAcl~yo9=k(Q!{f;51Np86fY(%jx96ha8qZA`0|<YJGh9E?t@?L$$adkZTq63~16!uHSJU0MpsO9!oYxX1du-K%0W$a3@Me$hUcF`;z5LEHkGnZ;~KLOM$dT3AU!nhNkCaE2#!sN&#WP+H^<53$HjseQ#$|+OpRrGfE6c#|Q>Y5*aV_ko*Lj0LF*HgsYhO(dsqLynL(ZW+JO*WTE&E)36-=Tj?bGlN6*eG*U8{22IolHi9Ot09DojCBE{~Az>(?r_)($`KUAWQdS*c{d;ERMinFS+FudQCr&e;Y=D~jlOfyS$GDeA_3CH#)Q>;@_<~pc%DwcUW+~9k^icNvhToPX2dLixjoSdiJgAT6+3#cR&F;Wtxl+;D7CfOS-?5th6cF4%{!yPm1`A{=-!b|sUDNWM7uTggQa)O^po%FpCl~wo@;(YN32U*G#+F5&;8e%qJMo)zqbqG_(gh7<V{CDbiJ@hDLDV3{g;O@~$pKu{W;fJm%Ce5(hTG-|9Nnn_mE#<QNr~KQz=Powm-QgGn7k^I-&@70<#_(^(~tSy>P%#l>|{mcjIoH8+44pR*{?sl2_BDBkKZ}fV==8d%E8PJ!}Bq9a651{<}NRA_W$tP^FOG`$o+#US@+n)AJO#pWGnz4c(w8<8c#=XS~n!gi&H~Wp)+H7pTu!>DeNF+z7{Pk9|s|dOq|N2=EP+c%g-IFTP1C|6tH+o?m(GI0<}I@<Oz~PUPExeWzuxC{uEM!?R=Z@?{->HMZ|&R;98z0CKOg}UJIFLLYNgrSdB*N;hW|Kyne8;DUm_nn|9&kzM@=y>ro44K7o*MIpgye<$B(=ESfj(WN#Ixs0`UQC}(uaOdl*u2AkN}8cQyZV8%pp$IMv~#nC0soQ1SeH5+5<3j(+%3*DNZL_1(1Xq^OULj-;XizijO(s|#p?xuVR9v%5Danok=)uI2)0i=L&T_^mwGP(#gVfxq63}DKP9KuYY@}`6Udo&xAW;-~3NJ9tGXw0_ySgG~-OiX8`nXFg}Y}7WVf~;umTM;!ce_U7+<<#qZX>bPndW}D5X#I&?i$|BDjE@QsLHfiKu*s&{^OP=nQh6lFJMF36HEWRu`Bi9UHXVb@neVy*a`-rLVTk343OdRkw4$TAY3;mu^CrWKum7|X-Fy?z(zwt#C_ef(EPr4p%1D&`)e#7OwP6uUoD`)ljRl3(iq<Ps3(>7zz2cxSS_xqeBUxQ#7eVwkEYi+bxOX2OgZBX&X9KKP3w*1uG6c|HWl=qOSN0M4*3aAX7rEWspFv@gRpV$$YNHHjOMxs4l!s*8pF&2Lz`7h4U{*bH>Ww>&NK$HLo!pKQR^zGavdTQ~KcBY)eiy=|*ymCXz$7I?BznRS%0AqKUGR2`d0WEV`RO0U75Eu%uc8_A6vr2Lo%m7V9%<uTNBThE7Sr)#Z8@WgQj>-8O()DkVnt0dK~%w`4`+q@nockS5CQ_51hBZm`KfqkQ;-hF>=j@^Nok_3UPW9P>VVTiJH(#oD*4H(M?L^`6v#%+t6fj?k`7BB=SXFQEF2y;+l3nrSyA1KW-LLdm?4YuN>XDkpCi?TRa~x|)K$Acy9h<2;#xVbQW+)vM^rC5NM=@ykX510Kl=`5hl3FKVrmW^fz!53QPqZ~*Y-R|3(nCk6<jG(qz(lcyN~U)7e|-~`q-@^V%8x_3ZK6Dx99lwhv#43e|XkahP&WRx_<XdD!u*W8SuG&^V%Gx^^P$|4@ytFB3adgyMB<2H7V3AZgiAX_9rXXXt((D=R~tUFX-6l`Q1Dq6=<=r6Ot@u9<p>&-`MLQxz}xvhs-d;x6wA#m@VTKw?XC;bt=I6szEkYU^kq$=`dTOs$HC%LPG(We4}Ybdw(76JA~Bp^(@u_wt$>CUSUKL4-aU;X+=pk=n<W`up0AL&8QCVsqgavcBZV%C!}+-1fI3=?asHqCg{0g%X#?PE0to7B~1!pQVM8C-IRqtn4@qxs$@!4%o&vwmL!M<QK@9l)uk&+Y+N8+BBQ|S@0|#6?`Di-x|LP|MikPyb0D2$g>a-GRUA{BZ_RdP_G!Xk<jnn(-=CqQLu#Q71F}ptJUJDPPFJ;g7%<pmcDi|j)VX@`O!;6YQ^qz+TENMHT7Z$|SI-{GX9du+NiPj7>zE<Z`h<5v#9uCZ8~WNlu^LCcl}h$K+cR%x)PA`9Pu*0=QV%|tgG%zShyOoReuA)&TmE6F9#fA;NGv&nlraRr`<8}mRjCNd@-VbaxFRM+;pbbu+lW;q&tnMenTD97rA4Isz(&F=TSlF$&Dwqi{s;5EFr_Uzq@BWr<v1F~SLo)=rj$!b-$u~d8$yM35f{?=;UteDbv@C2?dmZA*pV+2Q3EOTVG-CRhgBKmJU&(xp9WQ5Rhf=Uz>?-Y#YU_HvHg(R)`=G3kepdt@@Jl&2L&XQka74R5Gi~M0SU6}YvYoxy^^x<sPcY6j0T+aiq{PoDGo4p?D|z*)5N?fBFUiAE82+Fl!i6Aqzz(8<1+?jd8Y8w-zTvV<h9JWcNtV7dH+z^dzhoODTw5u?7KwbfNZh!mmJl_%4FB#M&v@{&^GJn8)ldx|FgM`m(3a?TfiOeYEGtoODTad`m%U;1*X*oO>-yi^MF6<2tUu1bAEv^y?Xs6mV|}q@u5<H$-iL&b!v_PG$U_k;S@DtuGulm8z0nyiy@Zgpg1Bu-Al|>UJ@NRTSP586iV&EyvR@}Sr9yiK#&tlq_kd`F!y7xgc~{lI2XKqUh$Y~OQRYjT$2$i8(Jnc5@gd(mXc8g6;>WFmYR%mAt<Lmmh3zHHdE}*oc@Q8E&Vo?@pDEb^$X(9rBoy(J5UVN;R2ATBwMQ3C@;k=REW99?!4l**;T4cmUTj(IW<FcKsbUyK#mKE$W%LIR%%4BmSak~(Dc-bIo^hS(cOx)_^;Zz^3rTmiJo~FpOkRgsbOJRuc<o{Zft-Q_z7gx^7H|X_S~wA_8cI)C#}u!ng%of%h^%j{kJCM6wG|Hn~}^d%hV0{eO1q}`1q*ZY6o}SC?a&0^65y=F3{k}P18-6`Q(&}0FS2hBVsV2h4P?|wi0vK0=BSo&Z}X?vX8o)<=<Il$arBNc$wA1(=bYBMJ$TQl-+ApjX-VIaDyt!S-)<Ts1V0m44`t^$6#ONaL0^TK=iOn8q6aoUP4(H+?JM{ZYv)zi7*U#sHC47mCWf1M)1B(j(0EB(RhYxLeMG7yRQvFmK8I;l0rW!ZcoKn*i3jdgGYN+R@PgVAf)spA7PKP!F?Y+Y}(aw1L#gd$T}#w4pb=jvD9O#Kr;{uwmf90lI@68^T1id_&U~{PI|fcIKSwW%1y|3U)g=E89FM*G4v=wd_Zj3oxN$@7cLY?m>3?PR-jQoN8TGJ45R^2N1+VBP~&1HZjdFb1jgd&$z?xHI;!xqaV?e@qv^VUkHbcqln@CM?1Ma;n4|)|`!DyUPghsIhqpx;Mqjktz$(5xl2PrfxKKFQmt2bMG@m3J@>M&XaR-ng5!vr~*Gs2^1bLGZ2+;>rvBokB>$q!{i!QNj_LUh@yy#$3qS~dE$T_1}B?iSYo(_wy7ez)?eWH>86e}}Uq@k_nJg&%`&nPa(k{A(t3r&eiRo?+)B-6VN{o!L(R|lk5LdnHMGIWgQ3g8aqnMs>1r214k{!#y)U{@GduP%#M2#=Xku|vRDhwFBh3@kt~H*LHd-`y;CAv)Sr6K8btlHk`XBrW%ZceRk#6XLcJQG!T6miAe2{XsukLmkv8Wwg+H(w5G__hU_mD(i{cZu7N9)sILS+;HsJ)#f&ktXO81xcbG9^ss-sdJ&HmkZRf{R$yDd7BXCa#0JL=a<j^Q;tAXqsyDWE@DMJ^F_;e$gs1^?YH!)=IgeC8@~qd@G$P!gg4ZbV<^!|bmNEkiV+#|SUWhmm`4g^s#|n;esY(r$cOf6$0~;N^!^6_uzNGiU>+%{IL+)~?@2RX>GXUW6FZ_P@Dy5iJ9{BieM2VSx`KeMx|AJY0axZy^;>2XLL?x-@9`&f3AW$Ypn`i)zb3XdEJ$Lz14c4meSLc}z1D2#r(q^xk^h-E+z^|9jmwii&0$uPTL5|~mHSe^nXT{x=49Qe<RHBXHd4dR|*njc*)(yK_R#mbXTNPbLkEs|ML_%4lY+Pn22i^^f{UW)%x{VY!PjU_Ixhi5VY^oq{)H>x!!hcvH_cg_TSpotMDb9`PC>qF$xmOQR-CuD!a4^ldVs2dRtb}@9?7Bq8G8@>fs%Rm3EB}18eBry7%(Iq!8kWzD?L}}Ae2dK@`s5jksK##TsOhCmj~X$x05*e6qyko}1vxOa$EA7sI(d9@mUq4cR2@YfE5bvJ)Z=JvqPdMZs|MeZsNJ!^AVo+|Svi7sMLcJi_#D-_zaiE{(dccBbJS7@79BB@^Ty7RcbFR_=UU0YysU$44xAFmDQl=vS+Li}^JJPhu*gd5DVCP;E@fC5U#6;6hvC}Pvgw{^@EC63Xpc*aI-YuM+`K3dCu(<Q@-aMlbPG@KD$RKrurTG$S0QC3kA0#ECzpXCHNqm(nMVl_EDPsF(MwFW0cbu49&>SYS!Q6v$E}hEoG2}NG7||0xEmC!_HKgC8_KyUJ(Nu1qr=>8s-=sx(>G^Yd!WB7^uS*pf=jqbCRj||*!e?XCc4(@bdc!`vI{F@8yX;8)=ZdvrdFg|$%e7Hb@rzPdA{|oH>wh)<$?4LuKv2ET_>~_UcM$-#Mx|#d7)baUWTX6-4L-3c}975QAD+TF*r_>jmI`klKIK5s4@kv?jDmKhB|#;=z|9kkv+HXx~wc=eRh2-aKpf}KRJ*g4VbLn6_#+x8elNuK{w+`+ilLcdhA2ktad*{u5eSv)Mf65W^RhFD}!+u^6O-nW|s6Q46DaICi2uPLkuzG;fe&d%_m#$?&(cs?;I>WrOkZS^XLAx;7E%o0~K$W*AuT8dG1%iR=0GId5vgS5=NsMJC>%QKy}S@x}r)r5f{!%SbfZrV|3SvONcs}_7zUZZ#{J%bQ<_Vi@uIaF0)jR*24)6w^lp9=H!YL|JRiHW7;4^?;z1uc6dtEGesnu%-h8`4>B<g3^R6_C_Crwa*3fuz$YD#97;R_5nO(wKI!R`qMB3%CmELE!o0SA9}+;rRitv~I2f;I_AK@520DK6hwCe*<s?_Je!5Sq21W!|kl10X2q?009Ukc!+<RiQc4QlWgMccXj9jnG8tr`M(+~-axo@91eso-ZD%LStRFENV{3YLh;}+2L9>ufq#TvjMA&wHI|Hi~<1jj4qzCjpHZ)sKi+x8$%9_#+(Xq`#XM}%U1s}9S!Fj}BqAKx`)k<mj0$>H&~YpP&AIYcSRh~gE%%8Y$__Ug2JOqNR5fG}@+$vuMCA(>0Ha|Q*~^|~5R0SYa2ia@1H7(sYp&#RK?4wJ!7q-(=de&4FS!mc~as7{$OG@fn~h`Xr23^&j*OL^1p=X5min5GHPHlCe#2S5gr9p_y{4Ap+#)<x<JLqaAOjX0*7KrhwwW!kmL<h+rC7DNugXnQe%K+)7z0>!J!k<o4Nllffpu9H(*YG0={7I{~@ias%o6<FCHT%S>5nIfvj6sZi^bsvi<(!@ev)^$JO6cJJlsm}^mz{#&)`RT5JFL^M{1rFa?+iHH94ShNdDUs0BB*I1}G->jJAG5q>R@yK9`Md7UN`ITdrxj5<2OCw)%bAc;iH&Ik>tNpPa{}}2-&Tjt!C9Kl=w#nw*DAvc?mO@Tx4r~ni0cB@{Vv-jD8{FJpYQNzy5)K%-fpQq(s@Ev=S$4K^aea9UVPHpa_+q3`pO*@f6cOm=ldQegw5mcA4({%;?ivzu%Y^Mkcy)sf{vOe10C0z`d$I+wz?2{i~R#V7x&{htho%nthxn@h1(j;gG#-(|KO0mN!+^G5%s0?l~qX|0ONK0&SRrCw!H41aMET7q_5d2=L^&Qo`EDYASk_+^|AY)Na@lfNKgie*OoyeY(E|X7qNR#0dx&w{XT>y)t!hG*_t&Rmt&IsHdoEb(tR)npadciYM7xR`5<d`aDGxVyjfC5Ct{JvEL{2XIhNHvh3%oQ`JHVQZazFmuP83~()7<*Ad3mM=vxBCHDifeFq!zA!+vBM@Z{lJ3A-^i*&WeZ%yC*KiT4$|HnWzMF9>QwBhw%Y_PG6t5_-w^A3U*!KedRbL48YRh0@$$h`|Mv(#rZIq@=Jz47z(PwdeKoracqU+yR@n4G&XIB7!t;0<{_YNI4={y5+V08ra4Jgq?x0!8B!SzEG7z+kk0h9JgM}E491yMGM&9Ty=gTVMvw!YVOfj;$65W@S4c?=1ojozr0(~3#HC}&V%lhuzL4l>zG&uY?908$T{_H1XM|c$kT%K_^PELG}({ZgAG^_Q#h21!Q3rNGuOlUk(NFK+O})%=7Dv3+i=)7!u~<UUP@}_2S>X6u0|rR!Q~l3Qi?|s_2&jE>CSZUW^^SHo!+kMZ-4ys^AG?0{`s>B1bntoFUmtL(J4Rikuhpq!@Pz=wM%!s$hHfek!-9gNMhQI1eowB2_rOz+dBRd2Mpp*U&oaZF*koR;Pu6_^!ZUf70hyJlT<<q^3;Cd-psWL@W(VL<FcbDD?*f{-hz~u&JCd&P7F#_Tx;F1h<IcsEfV}Mb9O~phz|*lE}}Wm$>O<V$aW1?rF4Z2Yi?2k?n?<YmV*k@Tf0H4R__@8OCX*TSUbh0A;iKhM5OBrA?hVm!$si3B<j>o+{|4`V5+@>O6{R?^XiniC7_q`k%FsY-&c_Yrx0}aoGYAL0(pm#U`&$71r^tv#(=~1y3_EI<pYDtc(p`JzAp|!j6+_+-Iq($J~rfn&C_Z<DC?;EO-+9ZLI4+F6t`Nl`lrbalL<b2NARl7PJpH_-Sxxpt9%fB?M^I-s7od4@am-~M%<E4b!|7hYxK2@1DM6#1j-#H77J|fQJ#4;?000q3eSb%#av3)DGLU=%|wIyAbiPLh*I6h6<vj18b8P_1n@=+u%<*QVn=bI3i~A+N7UMyL+9ZyQYBlVd!lC`ZRv_c7zDy;c-x<W`q9G61Q)mJd;hkoca}`S-PEf5*ulT_FfW+6;>G1O6XdaY=V{x~H=l)U?iq+F;(461XGBb{gj*6$9m^S58<|W5&p^^_)X<Y!q)TL!dA<DYEXofv;i9*_*&pzbTtDROCXv-bRX<<j_E_<OzSU@me7U*Mv3eOO*krtnp?AGZb@Y@MeZn$-$8q&Tvc2q<NaP<=td5!{z3W5uuFvm0^u|He$*%Vq2PH1CO?oV`V00Yr@8du`>Kjr_PVfX-H}(2)gk?0+z-cnm`Ba4E4DL?4JqHT;T)h0kVgrZk^#zU*t}W1fvT63_s(`V&n*?!#P$R2%KRo~P{=@V3-3^*&`RtEBKmWRY^UFTGxrD`x`1Cd#)`;f3l@Ts?vIlp!k5z};pH!GiaozbhKelwT-~am4FYmuRgXh!2GUNL8?|(lY|KUl+UNJ47zbdI%0tC#LPm_rG`oZ(1WZV+=TW5^Nr;mL2Lv%p`F>LW;n{Safc<C>S`@<rFw||<{s{O_esRgkw-i~{UY<^jHVTx?Wi(kP72Yvpw<ekmaQJ0kB6u?vhzecsyv<+R(EsrE!Ypz<iNHm<tSVw#F=0lIO%^KMFA))a@p7836%<<=KwVsg*I*20!Zq)xRhli12-u}KC=6zw9+4GLWz4`Q9|2u2kyS$A&e4IG&JHs|NA8)<T*il%rVF_K-R~b<9K)Y^i`GDTO+Zj+Th)^3)X2CqgN;x9t?O4bYL?|GvOZK@(gUt`#YMj_9oVEm^%6P#e>{-FE@dI8E$LH#0Um^oc=J5&SA#vGP%6hyZfK#q43M2w(<W7Cg{I1}69+Qi7A2n_;{~c;R)cKm%xy)Rkqj$ZMTsm~MTdra68Vlvj;VWj6IgQh0=-Es@>150QU-D9_r~OJ>#@pPh;GuZl(t3)XWAW%^iMAoBSym8azjtboSn2o4c|is^rF}Jrx5e7FN3+vt2Vvsa)mqc_G$7?NR&TNgGgpDDg^8?nuU&|IJ(4&JI?0zc+|uXAxB>e)FeC2{J7#ctgP?b#FO~&UB_XW`+<0*1r8YeVQ~1!ICUg%@MGKo>n0G*p=R^h|UgwlR<aH|&h0tU_L7TA!nC*onL`$C{jvR}wLiNA;TV2D2!Qb(uJRH1u!J^|Rh4GuDxszj`I{l1+JQP-o)(&F(kCo@dM7}EF!LDNZL(~OR4Z>yvPgu0+$TyEhOgiA}#U<$8tSM6n8Tka&hoJY}uxi)}g!cYVv5f;pMEfiv8V@XUN_6f1MLeEH9y1(>$j|u^1dGCM-<#rB<oDap1`yvWQbzu<527~XhdN<ghE*wtb&vh9uF%PuRa$Z^#~Sm0B+6<9S4ca~;NWEkG_yCEQzl_N?%^tlfedd#tx^J3DFpHOO4EY_C=+g(0!)r)V<5r_)Lo()agFPAVo2_hTM*4i#y~BA%o1=TcXQ{@>Pey|E1gO`FG;B##0nezCyWYxg))!Rdu89}UU<C-U$_fWrA(v8&P|Zt$w>Xh4B)X}&Ej>?u{L@4=kMouo>YxC&H!`PHopBt%~~NUYVltYVGP(suDVg^mblXGXmN0;NvFL_1`ZnHd0=P^=YyP!-ws@CR3_U@mZr!LQodK;N7WFt%?DWJi(`5v&)V0Whfads{e^JvliH}9Ka~C%%AJcr@q+ny#gP?TDf)RmRM)+vC^yI2W2)6jf68jC)^r;DYDx~rT|VtzfZ`fe6rOT675yzP5{Nr(Y#5I;z;wy|j3M>r7y!)kY^%bL&jA5D#Zz!{5l&lE3)U#<&6VE_YBavOw8Vf)G*Bsyp+HeYPUz$?E4LOfJ+93dA%I(te=FW6*uz$8c!x{}Q5yDcvUVz9#&jHDo^$1ze%eHSP<&LZ-eu&0ihD0ZpQu=nGgsXa=(-hNYV63~D$lEJ$g>kFMw~jkm}|fUxU(S1-ZjsRTaKR;m2%{gNgKMiXhW+;2z6V%z7+?C5<o36?r>>TmY?o=DTz7da@_fu2oRQtn?Cd2OX3gHXkb@R?m#-b3^bClNHzHd-V<GbYKudUn%Z)wp}*&W$x=NYG1`C?pWhUB)0AmrXyP&TK7TTCEymoU%X&(C7fC7RS@NV9%7(1aMdVmZ&=_e_sqCBBoNY1iU147^b;LW%ZRbA7l)x$<9qlI8ADy?$QpUDgig}vYI44O#c{qJ6(DXN#@s>LU?ToGAT0-}bMOF<u1fem1VnLN|>-&cn>L!v=DpjDVdxcO{>?UxaT8HD<TMq)2V(7ony}I~FWI?){Q^oi)S1e<h)1A5FSm5qt1Y=UO4N|8R!$H8ybWzJ1(Jso6ja9TxdD#kX`Bw^|v!%}pK9s6#LG&Y}>Bx>GGLF)$K%oYGzc6wgJ#B(oxf8Na`fRUd1<n}JwRe63i1U?F!`sHD)D;(~0^&@+NNPA*c139Q`OUxkb_|KGfa#IaoV?drVgik_yO+AAw^>_$=1QHYCKjAnpAEfd0ro1+dfah57TVj9x-%2lTl~l#bLl2&6~SKTA}i*DDW_2Y3Rv1VTL7WgG8gfrC0C#$+Uqj88fEm{DtBcE7x?3K-Q?xlCOCqZfuS}m8{N`X08wZV`>xHB4pvqn#mDb=X*248vgNDxX{~`1`+%{<hx`b)I;Uw$!tCaf;J<{WQ*pH_ILA)e?UuNQu2&*Qr*m9B(pignDDd8BEplMJL?)45*DTuW$__Ix1PrT<UaIo1>4SzqR~ifn6F)DEQX#dI$aWt(7w-aW2SWCgUMs0);oaR60`4zVlVTxbcnS_0F196hpNKphM`>Ff><m*}4a<gh4qh~ay2-pK=BrIf#EQ9GoZDQ~o)KSGe?}%PJ>A({rF8T3h%j*WoOQfMaffXE7=Ij=F(Sr4V2jcO*xkn_juZE}(ld@-lYa$L^%(|N)_Bk;&jO30R|s=aMSwqi)plD)Y)+#v?-YRrJ**&B<6$|I<fDoni|f(2#vOyFZaa>iH0P)WtW7)tQDRJ-;{%hf&PoOWQesu+q;z{{WJe?ljH!jn;9?Qa_82O%Gzre~wlm}4HM$JV%$O2A6xu8FQKfPok_8Qt$2Icz!E}u;b;zl>ky~RL_XB5zW(fneWS%x1!6&kLrJHwWG-Lm=&`|H%NU#CcwF%z5YUJdFE}|FHRqkPUBC2h^EPpgm8KdzX5+8`My4<6LH7K1)G}dgIv5@v1$1N%p4H%r(dFW1e+T@{lQd#{hKv^NL$ZcCo_jewHWnDM3<H)Kxl-1&6n^k@p?e$m`Q_u1s{U_^4@_B1HtoSM5<1qBIQo;B(?7$J^Cwalv4?paM&EJpD&%YmKPitSei=t2}O++6XTJ3OO1@4Gn=Z?VE<Ja&Q*v-8FQd&weROfLY&^Hnu_B3VSJ3z8c5h7=w5vt1n*=O;74&))~=I~(S7N+CqRgCxAs#(@0avd$ucV*R2M=_vyRhT3aD-gm7>BXb%fZ*a7hOqbtcws&8efcr7GP-?p!nz6<Oa}=41NtREqTA#TUySY^{H>cfrY<iIEJc2Y-hR$=I(Couy9$y4<*w+eDZZG|%(vsyo3fAAS>R!x&cTViDH{MD;Y63ak@va+4mpi&-8)G3w=*B{`{%8+j11Kya_D9Jj1&CPOhCD$#OBiZJk6oP0P-diS#AZKOkP1;WlvQgDRQzLDmcUms`=>6g-7VZCrzqzo<zE_)bqnN>hFFBxA@z>c)gR&Jfz@IP(M*O#_s2Qsqfl2`#1wG_j%h4StA*;BmsAg8bzK*ZUQ77q#CgYmoPh{vTLZiWn;vR3+|@b&qn^8^=K4baPwl07KOC1r7BwCZ=i*#T1QR4TjxcMcqr>bVdEE3Tq1R|A1V|vjt~l9*;w@JTU?aqrFtYm2^A3#3PlDzn(z)&FrOv0H33N)JIl-M51h(cuWO$pR3uv|M|+TSZeM_#P#|wi9B;>++&DM1n%S~6wu~qdUy>c$#mO8Fm5SVl(PF--R>ti&>bEX)CO(BMf!zgxV|)pj+IyVUnrO>0{CPoV$em=&jmj^BQdEv?G#4;NcO%$-kkz659`Ls9T}&T>(*XaVny&Ec)Y)0cuSnV2)-&^BV&5E|6HjAd09AUxa7g3<OWC<eSKRp|T6?=^_i-(|su~lPX5)*4vCh;kFV|CF3(UkI%QZvVTYV}9L($`|frWH1H-NdEelewh2zqxPW7dLses6NIojHZ(fM$W;nUv|8guQN9=4NqsO2b3bjrv6PlQj0h+jVNL*m0d41w~oVIyF%Q7Ej2<nXI>%Mo?Yk{2q*bc}&lM%?E0NP}vQ%K-GZafw3q@cY;3`#s~sD80tgAa?l3_xepan9%?NnrqWGiZ7X(KV8zDp5TiW6nPLu)gfJ)+F=$EopJWF~(v`V#3M%P<M@XQ`LQJvq1({zV;R6PIm~8P+K4=xrXOL}B4ps!joaT5@*po`euEdmE&vrOSax$^a0NZuA0X9)%Uh9z1J&Lx!j1F<<RJ8Uk<NV_xv=tBq^)@G%JGQqy+Y6HKGxMTQb-^GHXR$M)*3=zH0SYi~F5t>q-qB!C?8%tnB@2A5SDA01Ug3#%DHZV<*KS)|s{E7kW2SM+09DT*$x~H{mY5$nj^l5{Ys{V1Yiq)ua;!^arYQ||b4d;HS47^zZwTmv){}HMXV*OqyU@Wk^ixTcRlR+!)DmDzVqZF67r0^s``9HjPzIJ@BpTFh$gb+4tahh}a#Ue~j;oRV)?!486&9?6tZCegQW;MHq4mV(DRD_epASGZ!C2V(cSV*vSQdI$R(TpdJiXa8LEkwdGGi`x#VN%3HSwY>5Cm%;&{jOfK$HMM0C{J3#OmTATGgqJZ%p%-F<p@h5^0VzJzo{HH;{QBmuIQh#HO;#_B8FTBu@w0961+6(3J7xFm_6s^tpt<Xq&Wl>_)|A2O5y<Q_YPUuaRy(rGf<OFCn@AR^5zAdNgxw@d%H_C#@@c3?jyOpS%;nM@Hm|Y|__XfvOW_(IpVn$~tfu_q4g=3$*t<j*DoRLW7b;mtV108D}-vhErbYPV_|J=OKd_=F#tni!H~z@2s{aoQv%KselPl3`s)Hbvt7(&rc-}e`0v3*hL;gmfvv9=zwAd_pt_}A<O%U2}K^(f+-r(4y^&Ff>?$UiTX1jFC(m;O|$jTG(WnD^jU<?msW9ngazskxr=>U!GbYLKuH4@;C02uRjH009Au7{W#8qfh@JlqHmCqo-`vpL)uC|n-hwKD&O3o7Yl(5u5}K0NdL`)L$Z&+Ty+Kh^Zh)RDC%`UvO>IwRZl_lRKSQsh<*fzNcyeTA*mlQedZQ%XOELqT9ZbbKSeai=wxW7q`h3~kLmw^r$C;p38|ULYDh#`T^U4vMY98P)OJCVutI8$Uxuq4OjP309^fN!ibl1dwoPI?_Oa4yB+1CG2A&-4fjnd<fKfZ*MUkQ5~*r1>}P4#dXzZGPsZz+=-=c^AbJ-l2&ZcRlFntWc9(Gqp31n>rjdZ#Xrcdd<Xcqy(S5L7a+Xs26V1#x4Fd2Cdzpe3}hZw-Viw%>0Qt5E(&RI}O_o0I!rO}GL!-C;(_OI(+*%LQe!8eKv7kWmpcg_1d;Bf?zdVpHp2tm5ZTIP;mkI*P&KPx#R6qkGiHsk|NwV8b{@Ht@4mjd{ASR5wl2+I%X2ltPqryfB%}UBVDU-dpimvEt0)PN}d}JEa6^870f`CUOVmNs41~qqY-brk!|}F?%f58hw+PQ(gw_&_&|5@9UZT@Y9cA0a+S7jrfGFW|pi=L9`zE&z6i?507itE%qMa#5ujiy}k(m-(%0B3qav$sdD)M()t9Dx>X>jJFn`|%ccn_i}8?fsVML?9ZOYqBIo-4cF!H`ta(XbH?1U)f~Tpr*#HXIcQ{8WIjclu`d_Qa>rJEJPy>vzGmfRda13rqhf@wH9gr65*DIk2idF-V#^q0Wm*4K)6)vy<)B%-zaLyErZ-~}j70@4t1`%RH#tW`GBrH|kdtqqcQ+I9SLWKyieH9U-7CZSK2^XMLPGKDIMygDet4?N(1X6I-Gn{~n=8axw>;()#lqNL%5nQ3_(FnRqT)1qW84kDIYT8K>)p4w9HIN<2f@UnsJB@fw+glKremXOBU1G(CLQB|@pmLQWUj)$)q8M;)TSWO2qWhsaxfwBGIZfEVS*vp#iuxp#8j1^CanQOHo#yG%#k(oWSusr{`VFOfI$!;v#C~L%JDRu$ou(ny7TF}jvamKu*b>h#m>7@>uZG+QR{%p-Dtx;|#xp>K=lmmDtM<dVZp{U?2hfJ<!X++6Lbd}t0c0j!Ms`kM?o>ffq;<RF0IFgdT4EZdpwbCAIfa&mJ;t9w0gaUoBIh6kdzx>MVBEjdn+^%N;A!#xLMAKTxnrTijs{2SZ6~83+OaWI{Bmt9tLS6U=^vAHyK`}@aRK)@_PNwYc#={U<AXX<;Jv(U8?L-9Rr<gY*J&*Ky|P}>Cnk{&YclJUXur@IRCk!>GOna`py#;O8QBA+0>o_rmQRclpx+!h7rPCqIId%f9GDjY$SMoF12BxL(wPiunu19f5>Zfvcd`m=O5u%>ZFjWJ&2-Y3<8pVRD?zRdlVb8v1k=|UOX}F__7+OYyUD8T$rCUWcv^m<(}ZlLGcG!f5b#Nvr6sZHV99T{?H^b+PAROh!B9bBiuMN=&!)uhQeUAWMn?)yX|03m#m5L)IUf6G-@z<!kUBvGEvI!}F3Fn~+>Bn+_B@9rgDN?npvx?cg-tc7z4qb=M_(#pnkH3Nm0BIM_~5XP_(zF%x%`t`DITDP*SwDcCgYoyFybNtS$dGzh3?%ZQNg#9BYlk(#$z`F7-E^Zv(9AJ0h5O1B`^qkUNpWS7)@MA2(P+V#Z+Uc>MmhW>q`;{eF$^(rJ}&N3W~yO^_*!wV`{QF1#k{Z;f=wx5LMKDYQQC^7M7pYuy!U7;EFb49LiC6vedAmY?|$IcqFBo8CQv%4&qdZa#<6OO#9!gL{$jsPxA%Nc)@|WQOO;QBdwZf6uL0w04Ah&R<CCoGf4@V3XdIiZr&5hNOf=L$}r$7W3!+2v96(UdbYQW{EXFU@MJ_?*QIAP*CRVSguM@tWRInWVk&w_%584hRMSd9HS{<rj7X&@G_?UEeZX#kbe33YsJZzGM>q(f$#|p@*c%%Oh(u$6XbRh5P1iGrz(CG%p`dZ6T$<FjxQy(1H-v3PK7}o=bq424_DNeu481ZSaYKrb$d!8oJP=|0H?5FJF9HL-0P}uc``0C=bBSYF?#ST6;Qf7(H5AHyhU$hTj06?<{IsOdM9j-sOkEEt+o7lFsEC$GJ~61Zsrb|<ctmVk#jR$ej^!o8gdRpu7RMFLgbK?0V@(T2TP7Vfp*G^F%$0y0GCKpOTdg<SRGtHiNdH(NvLz*6K&o=6RE$2CMIx=Bim=Z-)j_f9GT?ya%PZHQ%P-DQG87BOlN<(a!IwxBc1J+zk`mAMyNVTK2UN_^T#lY-hg(;XQD%i<QY$FHp0iT;y6oXN7p|7iQAjulUF`I^)W8DEMI2JhT}{J;IWSS2=b6e>RAOT7X@(3zWh^rbT_&Nc>@<1*@nhiuU`P-W=aREnmc9DGD7Hf|eL{n{gmei;lp69v5|FayiFCA*a;MDGN1tvY0a+1$k>{6S%9F+C$gNVOg*lK)cD-yn;nfoEU%i$<E%9J}df?m;=4r_FHe5qM!7LdS0L4lnCJF=9KojK=keQ~5dfkHYbTq&t7LS?=^U$7dqi3klz_8^i(Vqa^c9e>wFyu`HtVH*OBR*L+&kglLp-b>(!RDALH|Oey`!vYwWZ}(X0Q2|e<1RcsllE6H2dJTHq?{N9qMyd_QdT>>n)Smhnzi}mEI;TDkU&0@l<&j^NNiwIyE0)HQGLp@Ok;bN548JP>VuN`0Xw5}%tja!o#FK9nMCCIyQsS)+m17p>ZMhPU{jI>kLjNQR-`n8!Qu0(_nfcB(1SS1WgtmUzOWQAp&2Qk{IW=_ZE2F)PQyGNSZ{d{839kA>cbhKV?d<?Vf~ScU7husO6m~dwl0Y&ryHvMjjTZLsTiUVyoqG=!&vn>7i%Ti_@g;He9lT8(1FjyI949$t-F~kFgUHR6iV2BwFSw)ao7z|OW-A$6<K46VmSZg?&}d^xOWHFgD_AMeN~UP_i5bG=s869(p~}-6A8if&V@Auy18^!$_j+=WW^3@iY3)5Iu(_UCWYS1cxiXJuG7(Fslx$h?gc~Y^zN_GECz*U{k{uXR;arf5JoK@cGszTI}_Xk-d>fJ^_Jzz9=<%hr=h71CZSV_;OGS=N6_(t*Wn?kpCwxl*-THfroV^dp!|^*aA~4>gAYr<b>yJAkB;-JMxNS)d?EiTNEz3H`SuUu1JXlw_NH|szo5p<kd}N}k%X^vK1m37BJy6`@=rw%B4e?}Dc{rdWn~tk^hz4v^Svs3))+S#NkuNFs@e#S$wAxp=Ac}D_h0TypRTTEi0kJ<tc}E~TEIbG9?7U+Pt{_9T#8RjwUm3NtO;0SQH>NPgnVMDLq+HZFh8gZqDEpR>pv4NsR*N%6-GAE>1#t@s>Ul8C}S^q1*XwVq$UAKP!Za~6%%YLTbEoScr1mo0zCj|@I^qi<Qr_?j(y>pQduOEregXLp+D3PogP}76&y+wVG@P`Fl@QqPserOq>#~IN4FIZA;Lu#QOI!E)&iUl`KdvmvmIu7##(?aZ>G|bw-q_)J>L{5Q%lYCyx=C+^1F|Pv?@+=rrpVu@}`wJN-M+Hy5Ze!GaxKeiFiWLD@&^4g2UBf8V{t!FCcKxqb+Mo7pkkf3W$%%WTY2^8rm7CKt`aCC1|-PY-6dYccLL!pOB}Ebg9xh>T($OeMp6Xe;f@@-Cir%P`RcNDFsT)vA(3n*&bua_p`B#p)u%WlHG#|r#BOFsnLZ<yScHT=fgs>uBWwnL81vk7%{d`xd+d@GaJ2ZGuHP*XN?B<*0h2<VjiU!PG?JxU)_5}35&XVoDWHA&FA(Pn8p*ovtmKvWC;DUqmCmwoN73|JcfDW3QOc{S=GtNKkXO_SCrAY6NftS4b{U*Fb~q*0f7-fh*G>vQ{v*}j+3o>CvA>R9?$(q?~(~_;PDpNrc+I{!;$Z{QT@h<i~IFWzDm|NC_sy|{PL*+w8@1p+c4$h?+s@-^(_2s*qZ!Q;O$hme4<asbU^5`(g^K=p*_^lQ)SZjBnNBrHYgE(K`QA&7)8u%YS_H91S-;*$=k#aNv_CH?PeQtEB`VeR!q95F@-aoGVNacu8{TAJGik-={lYlC^K=w<mmspBLt=Vcu1w50tY{RD!@IeLr%0GFD=T#E@)(f1%htAFK$y`b915k=d{nr+W(H#oV55BER4&JaQQD@Q06nIJK7a~6e<cv-0cjGT|6NyOUjmJJN0Mv&Qf7SK`CnDvtlB5Y95zo^9@u<FB_y#6xk<rt*8}}+x&USc4Vp)3myP7!pS&5qchyPFQ&2spj!M9+m(cojx(i@Q{M9zO0+3ox!w?E7mlBaR8<0zmQhn_(HoiOdv>9|sz%N2g-4x>`Z}Hi0xzvCI&)p&tWw>f7;$z!Q{$Q7HbG;e2x?gm_4fa^{f_venZNR~hlTOyrpn|+Eq7&E2qQ9`TsBU>v%yl`mw|uk=eo6P$>bw|5~lAPEdf3hSee@<*LID#fwuNxhEWrxYM#9IGi+BsQVXuwE{8PLO>f}SxBm8w_L0l#eEEQE>T~NeHAi70Y^m~YJ*3hb63N#ZH}~YqR0ve6P6-{SC~EMso-PSJ0M9uKpJXCt#tLuLXV93u1Eo3Cq)HMy#*PH@L2n<`8z4s}##pVFa7RjivxH|vO`@s~MNmOQ0B`#_wI_7w5M|+wfw3@_tUAk4v7=OU0?&5)mMms(I0@rWk_oRgspKBhDa1R6k7HV{tI2c!wZJC3JS7w6FR<LgeP2?CM&kx~31(LSYm5A!9KX4h%C3V%*=h7PL>Mqg9<O$0x8Ar`V6sBk=mnjo%<y+a{{-)q8(Zv}xGks$$yTNlL>8P#LFH6emxt3-f1zPO+U26llh=&e*V6R`tXEbbxik2a01D$eKQLI&WtQw}Eno=~P1eIp2vjJ1iV{*f%VW={dCj41ya-o(eD~|ETmn#2U}OrC6d3CCB5CiEtN><|;>PkZfSNF@u}B!zLBIhh&Y{TzTdc>0Y<4-RxsV<R+DYO3D%e(G0E^nUGAjdB0&<CTH+L9$ET6%qB=K``9_c|n=XuSUV-`Z$q6D{5Xr??dFPLU6tYGXy<#FjB^@DjkUP+aVIL0|OL5|IGDe|tYZYL4d*FEOzr5UI%k-+NX-KapfAlrJmr@ddCSzL&#s2uibuka#1?jnTWh9bthKXHvFsUmF=C5Ah|WJpU|=TS0XmR86E!?q~5-NRT>#T1HQAd8bzwKyFeM{_tbcCBT?y+k+R*ya;8qO>*nb?(6LmjS#1wd1noM-0gV26ib)1|UbN&7m@*^2Kwayj@K4t#Q#`MAHqmmjt%sAumRfWz!m@qyEt8UKdho2Y-PIS;oZ0G%JEIYKtu+k2_L80f8E^e>SKNpR%JtGyv0zZGqlTUgBSS{LD?3by01@a$~ID**O~#3V~wK;^Z(Tekl~{OE&tpZ8m_k)@}9_OH~4EzM1KJWlJW9EK;J9M{234Mg8hB<)}RWWcN{Dl`*PNNxLF6vKY!!Ve@;*C531@ss-&ZT37Mvxw1umXRj3%-tf$dE7l*G623#JU{1#;YZoH&zezm<ZIkX`a$cC9(5t^wo1F8*H*rXaLP54lhdjmpJ=noIT&t-?kTInb7kx69?c;m7fczfjm$D4t)epAWHxs7%QaQ=e?S}y0db^(3x|VV^UNsYX;*P=1dmuQakAv|IIPdLSD?8UPR4jKt<MN^jo#?JF!J>0K=5~5(#;5QEHitW6Awq^D7AfL8NxB=#3B{?@Q-6=?t1UiLv1DOriaF$(l1C>Bf)<!<=FwbHI6i-+FG%lN2q3x95}ceNn1uni<5$Sgv;rmE<MO~I=mAH-r!wq+sg+$=g8)4g_jIgH6)l*V2L2>;U5O$X7g%Y1TI`bm&Ik)H$b3j!EYC@&qcBRuJJ=FhgybG>on~tj01A{HSbx>iOXe_~Li2+Q=n>PR9`4g*q0t1gz)g>m0u*4!14BTDbIRIgZ(5eh0HVh{vpVB+1wglSU}87a?C9&2$be1K!h}-kTw&L|lojAmmG|RUKNRHHV$X#N%7o|RV1n56e)A^vj#&Tc8aTXpGr(5%h+A4NrC?7p<rcU3^r2#D^Z4qu7z?eTZGI00J7H7U4e)MLa@5NoZViAtL(8Tx5?iUHc&Ct$%#eR^1nX!CY(|)aZ6bChs`pV(<Oo-k#|rC|zzF|ufBf|G5C8oB`Q<e7Y>^`-v2bB!<1Skg!j&l??as$HI*y=lU=WFA;k^QH*TR1sqfp!sz&QXc)#h(ixP!|@rbkX8NJ4noO^DI!w3Zwu34a8P><sbS>?{Tu0i{<`6tfZOuF70bt*L;*$(SEre(8o5Hk5!iN7r6=>na4llaWirKNX)oYk*2a+(E4+UaDFJY1ix@L}|PyN>TsPB3jDi*lN53H^^MDsbiQ?P*xgf`TkeG4~Bg(49f0zS&mA023#QImF677j8du($$ZKFgD;<?Jc|@b2hwc7xlJ}q>XDmxb&|Dit*!<Y)ucC<<KAGMOFZ$u&Fv9wikI6)zY7jn>M~wmf3qeqH<61E`3q{`@`J2OhS^NtY@w!&x#iS-$TU~ui`73&#^ReTUAXk34g`5|{V@EhZ?RH6ecu-im&2=<mrfR!@>qyX9bJ`cFukY6Tjp*wfe2N0Af}Zgs^w(KRd32>g(t;g5jSQzWn6|@Gk~{~800{JrPn)iHP@B+$TAoL9IEotL=gr@_a~C&*f0*=*r9L$Q_WGet$DAz+jSC;798dAm`^{{pJ@8YTGQ!{3ksFoSwTQy$B8_`0{?V#P}js|nV-6%_QP9BOIZ`@CUeR>?83sy`B2LM#GE5OK(g6X8$ZW)oLtRyP61E3QyuLJdRIaIE>V4axd0!pCVbi>?GwsaoqyKU0=cLJ+<D@DVq^*xP;s)-#sXsjZw9Gb=efQ8;rW;MAD+Y8YYEVGWPkkm`PcC7DxG9K>X#~)NF+-6?!@uk=8S(0aI!(C+QfeiFdSe3l#bhac97nJicK%)azUg9@UJ!GAf6|s69Pf-U;L{K?Yd)m{>O-}&kiu~6@QI68}r<XiY@tdbLp>P2E+X6uf9Uly6kot0DuR(-^VK5?N93brNf<na~+QN`D@<)`qMA(zdX6;)51XF`u6XCKOX<#F|e+nvCm(XbSnYG?8~PaMB?(n^Q9yOH~L#=)YhkueE35lv4}#}=3C?qUJhw-f0#df`=_GqE5T)~cFMkZJMJkd;AN?XDY6|eegzkF@A=!3cc>P4yrlc=@B&i_{2Ig6$owCOMS(VW46n&twQiAUK9R8wh=lG#&ou|>z{U>=V>0rDS6^g~zbznHu=YSrNabf!|J@v7ONN<q>f$i(3&YHwcP{?=^64o?bn!V4(6UndnH;k_ao~4GD4378UT8H?G8ouY*#A`qlsr&Hv`qcK(*Xti6#ZnU4Jf06jHCx7wx6uaQJ^q{_^IX+R#4t3o!FKHrZ0i9;R%n}gb0}cKj8J{AOKdXB2IaqCN4%zJ$Hz4GPEoT%tn{r>40kvS*S6&NcU0W2J_zuBiY+mgtz+eW#*bYz3U~u^b@X@iAnk2QdD~!x?)BZZk#Sd&t~#TCxIycl9y6F?LRk43odYzl(tws#n2fJM=wjX4PWD3RRoIto;>tXA&7mSoEKz(Qv^nHcw2OOdo(-vm6M|+T)A3nx)z+^ilaFiGSZ9f0OS~#!#0b)FKi0Pj>k^Etl<W@rt%Hg&w&Xd=*1Xg<iY8Us1OfUFjW#sd%%qc+w^zcW8hm`W17%C*pg`|d|?h%F`g3{fQ->GtAy|>6^TM<vY#Lk+5(vO!V+Q|K~d~RfKsXcSAVOxug&@$ZnrQ1$Rv-!F!3rKEuOAVzv$mloHmT-xk+}HpT)Qh<!UWK)wZM%n+-hfHef`)c{E}&pI<L7LHA}&nL^0OC#XIIz3+xq!&V@)_kW6O>4Au7pG8FDfu*PVU#*TNfMnO)uqYr+e$I~|SQHjbpabkee!u-}0OvGmat$8)AZjyys1wFzSe0^E_t+2X3Z0x;rKOXh9@LosBT-f>xMHpoT5z}IW-_Nt!qj$$t0dIuuTgVi8t|QxlSllU9vnag&@?=F#dtObBEIoNh4V>-6gr(4l6&Nmmot(vPzxZl1l-8o-1$SLH{?`uc2FQns?^Z9>Sp%|r@R-h%;WT4+4s2@UN6EI?t)Y))9A5t6XbU?-bXP5c<fiRcpY@CP2T<a`<gU|8FzulfDBu>vFX+ESA>f@46;eJvPxkLkv4|6<eQFmii1N<x>I7rIi>2CVVj!5>|D)$G`Nehotw$hr0D~RIr)85Jw&SVp;f*(rkA`LM+c#x0@&VPh=@f}8<q2i;lyIOb1^7hFdwh@dY0q`<KZ6ahKy)E<4QE*UAq5MR%2DD+PAAIIUINSw0i-HYq?l>%Gp%(x45Xh&}n1Cc%%WQOYUb3sn_aW3liO{iiWwSbeZtH-Spccu4;<w8YR8C^31wVF|p(l11j!7v^<6aMde@DB+dx9tVtc$CUMdRO5V3vYE<EP&HOz`<#1(dL8UEUn6^w;1?D+duIZ;u<Ojt^#cFp(9;npvW#|)?d2;5eI|9Xf2#pEQ;URgo4S9A##fVd97jq4m0CyH7*}LYM5h(B5qEe1rGHFBi7Hw$N2+47F%eUgdPy(nEYR5~Xwi$HSOG(Trm*dXQMB;^lO&|FOiui*F)E4O(sg|<>jbtoRO@4v*L>Hji;?Ses>}qD{f7f+}TuOhCh|vbD`2420o2E<~LtK)%%=?pxYnSG(c-B+eyGTkg&ypv_P&Q<RE+WTTg68?j;0l6?&Dj<M-xc-+(|n<`+;;ARObM*=(a~;V{n2^5Y}t%nS?8G<?tP`8Je)ojX!@JWcw2IZ=OuIxS!C6qLl7GCCl*xcw!VLOp>84>rJgk?GWHQRM%@GsRO@gYd+R}<QVjhUx>pw;i7ZHWbE+6$<|_0obGkEk91Gl?j9^S^wn6HYVmJtR;~|qDEz?kjY^<V})XP?I%fC_xoh$wBoEFOEK1ApaGjmhW*pWo$z9gYZ@lW~4b@b=C{RfqO(r0@uD{#h$uD!d=3@N9EcRhT$5%no`ZQ5k|MN$J*R%MQVh34OVJBCD8z#Q>tPTuP*S$3VWrP881Vof$TbEP&x6AMnP&xYQ!0DBd;N3c4<a5Hs;Zbgfg)Q~L|J+cegGLQu%X%)d<=OQcSgDIy`018;zH(LOq*RtpFq$O9NBiie-_4A9Z>Q(N_4leM=>$=Iyw@q*aF9Sp4V>Y^_s{rN&Aog8L1Rp%B%KRC=XvFT)X4C;?%UA8wS_3Ec0b`2~8MJP7PScd+_K(d<_r8XuQ*pH_ILA)e?UtA;wp$`cr*m9B()Btm&y{RXD`9T@9k3cQ2awK4#mYj=F2Qjg$UV2`$130>pdrwe2162aaGnU4dsKB~yAPd<cLBBoA$v-%l~l9v?(PWz_ZO;3v5+x5ceoxcwqbuD>a?AkMR$fNu7+hpI|nbCLEU6t6!UtgBx1!}F3#<Uc)*Vj1NyFiMy5hN-Pv5Fbo2CxFmU#qb-YJ$hiv^Ae;k%E0+cbL?bI-Lb8(!w&y}8W1w%Y?1yc1H23OX2&?wIWi=tNub5TWrKYZ18TSsh8qcHCjfdxIRAXejHIg{k0iXMyW(YVGPgQspgj-E8<s0OS}JONQ+Oq}Bbi*Z&_1_4rHRpz90duL=vBnphFh05S!5zqFGF0wQU&hoZ1<KXogEp0Z@IT=%;heCUWKB`pCL$aVj^0-F+K1d6<hI<GVH*#xC#h{%wOaWkB!9XpUCuA<k6Uw-GcSbYzFAELzu8jm6U|pNw&8tREUg#ovF<s>zh9{!h=F9R&1C=ov-y!jV7^}-Y3XF>KfdyR50*tmkOFZ17LeYT1X`P4ebf--oiYJxT&jOSc@`~KHHIeMo7}~t+W_BD|HHWfVd~CDIFRzma`g?Apn0l56=|5RVlFwVqVZ~1YABUlzl?ukUVF!*NKgkQWe)wT8Z2o?He*XO^ds_R#T@-~<X(IaA&}xVKDsV^qI(G!N9>0diz;5mZkkV3$p*oNIfW8rCo-$$pKRzTikq|lij8Ikn&pwOyb080)u8+_clP1NHAVaqSoROe*G#4m3)uctR>ZhX^P`oNk5{VTE;e_<!(RM&^aSTIP`~$qO9{9fen7T1vzd2!Dg$t$wg#H2j5+KoS@`o=*cMty7O&n8~7YCLize8_7=Q$m_$NOCc$$)ZKbk!7J%xLD@@##(3N9!!`uutdUMBbDQ0FQ8@%iYL(T>*!j#<uPqB>UT$kNExbR$4}e>Jd5gGJeJh{%9tkTvB3l>3p8%P+<UhlZh<10!}8cAg;2fDv%U8Sq>E(;sn)v^yb1Nbm5aG)j3Zh-B{}R;TrXKzk^%+ZC||J$z~o>a44vss2gMVbH3DfZJd3a0hjx{ZHBCo3|W$ZyGD&7&m%Vhk`7Xh*n>-$ol)5}RNb;M;>HDc)9hy>|IT_eiY~Z$F-MC+TG&z*t?)O{!c?uJrr)jeqDDNF^`WrwizqIUy4epEiWo--1+Z)^`t>a?%JWh^lAwf&2ndBDgC0$IhbfrPlG>VpB#oWr<@N_oWv$n>&k-t;t(2oZ$T_z!z)dKSHztm^<4$gz8(Ph5SsGhLl!!0Mj_u-P4u?ub?!#y?-&8B(_8awEmpK!kLYBbpg1|ApgiP%{&T37x<rx0Fpflu7GUi6*mq95iM>d)Z7^AxpY(L2AP<{`1+x9M|55Z}Ge^5<V_;u>+EaX?DY;EhAc`>nX4$q0Fu`qxtJzzK_@_?o6+@ve+d=jm_-Lw0+mR(hi2}`r_#lcu-YL}PmsjmfQVvyyUA?>X`6@#JZao4~?I+z>4Tu#53Qa}W~yN@wz!92e=x!BH}LUTZ~!0$}TbWOruH!O3rxI3lcq3K3_BKt`i`{3<5HCODoPL6`2ENGpYC<2Qo<l;=$TTCOUE^>Yk#=bnJXTatIH9@HC23nwMK=Hs>l%qSrp9^CI0UiwXp<y}bgM!?LiYX7Z786tHrn0sbJ1wwcV|a*B9^gzdhetvf6p9$Mr2J2^gCyz7TsZ}mbigAdP-P*e*!hCYuaNKo13pZ)_$ME<3g<J(HYf)x0%A^cyeRBRC1Y1&%B^QR93(lJ*k*w3I@|!8s4=f~Na!9#+h0b9xN|C6dzW$k@etYyh=O{X6U-gk+n((O$@iIgQK-6LkcYF_8BuHM4x|7D7&jMiWi9V$Fevt9%<z&0zSgVEH&Cze#JiM=_>60}tu0mlN%=9;IAwsUXOQHnszgi74;;twH{vzs&g!)_VNW^MB{I{LhPt_=hWINYZ{art^g-)Mx|_4>o`zlM;2Qd=B+9DZzE)}puqClCov#aAF@k;Uk{KuiOE3}*>NaFo^-xy3Q$#tcut3Mv$bM@vBE<>|)<M=ZZbqq$r-0CUV)K-^B%;p;Aevw-Z2h|;%N;BWy(_CcjUJxfY?`3&91)o@m%HK=;{2L;Q5Fb-H4kVjo?;+MfFOXpvpZsSaS^TRRL3`_`OBED$OVZs$C;k53fddUypPMX)N5i>*=2j0c2|<818t6+3nFOB_;DCJB~AKVLSVE_T03^5VzUDcNcO4bMvd1<H=j~Lg7ue>+<&WX#w0zOxwd$O$KsRLl|2R#W4uq^iQpq6az!@j>#so7iL&St2x?^=IE;JR-0=n4dmhI{G)$pE$)d}z*sF}Q8f?QUuXHDRBJlH&K@9Wgcf`e(W8QaGTNBPjcK=ksgeZn2A?LcCv6ttkl7~MrJXGu=k0Hx%IA(M}F@yV9gVB)XeZ_<#4{N~`4QYqgfKx#%Ly1KF8IYF|R?nu{dT5#--9-8<Lg!1XI6lGx^@rTWzO7)v7$u;j0SoZDV&ke*#|{oM$IG(sa#Y05e+L^>fT?e8XzuDzxOs0ul|bj6K$Eq^xM&GY$!on5^l)T2LfYP-s3|u<Pn8p37rdsnCo{LxtAU@P*U|FUf@wTCvNCMDV>7)`67MCM0nQGlVjZl^FDF}3JurQ~Z0@0t7X9N)P^*pe@f{V0UBG$eh)p#QaG0g9Y_C=2lIz^kic!XPc6<7nA7Z*|Vn0s5BBCXKr{iqv|EQ41KBz|N@y8!u!pX0My$x(o(43}vIE>#4veUPe$&K^Xhn5~*t{}IjA_q-AugPeMx>N#qgG0Sjm&d!-MmM|^*ANIQnOC&aEw6&OF~vMKs#eevTG+P+!WG-^H;Pp#|0Akd?TgLH{jVlm0h{hHqvR#7OW5UtGFgqTAbiNEh?zpkoX`<rE^@J{bud=(b10no%w8SEVDTq>X!g-P>f=;ij|H${93va}*{a4o-B+rcrfF?H6+lWMN;+PcOy(|Oh#~K-_^eoQW^t!f*s7gUg0zg1Wq1?0gYqQBF}YFO2{F@7Jj<9p7Hf^ZNz5rP19s>laohLxOn&(3N3eh_jh;q)LRT|O)}<g?kNjs##;k|Owd)ppk8t9g-r`>01c2|cXVC?qaI{ppd;n>E0!ZB|kkg%4_2^~Ogp|d2NVrrKc$$u-Dm#&LeSf>>4tCbOB(R%S5=g<*RNHI-1?)SVqm-OgA~OB2Rpj-iQE;dMM%fw1(qA|Rx1_@<2b2y-i}mZ3Py|J*0Z8NWr@YH=_wEW8SODsPN<KJe3dT1?Yp)9Ek3)k9F(KmxR~-_Ts_wloH1MgrwsE0CgxJ1{h*683e2;_+P%5V|4tOI~rpi?(vql0bxat{Bz(w;$uQT=nh9F848vY2bQ1xg8T_rADHqQ))+io@OB#G)cR<#<)j$}bImgSvBJg4m~2uwen8M-d9Vnd-N>_||#N|7&u=m${@IJYgL{0Y(h(45?in6R8C?BA@_ISxgAl1dH51+F+~U5ZZgbm`*V6y>a#CKCOI(mkE8{!n5+vdkS#+=EWj5NnHUl3`g`n<Q+B=NC*2NQGBJ?t?3Up(_=>-6G=|Ai{J05v^7GVO+Q7g4zRULv`U2mm(qCft>&{lP)7WCop%apeNG0-Eja_F%2y-jZ#qQ1e}~g%fcSx&!B+DN(Yg15Q06;H%Kt<U+PVVgk12ncz+?274O`!P+>=dBlWhEQ4sCe7%G0bHkMWNG3fM<NxI#+IM%p;dmQ^*>LWZ!DU0zz9Vzf$-nI=_-j*tT;E3xqmi=B?ujmt#NQX6<bxO2f=nSemOmi7m(mK#{T<eVNfl>kDwgAf~MhVbwj+~3#hEyEau|y8civVPmh1~%dMpfxd1~pB=Bn*itsKPs0g*Bz{#>loiTIXguY0PoCJJFROSB6P3c_@PE>x?CJY;}7JCFR{@Rrcfwm<c>BKhbGIw$d3Fokj@wq|DNi*mSVux7+p)EE}g3*4SXEATdSzgNtWV;&-X9P!Xdeg{QRELG|KegsdEo{j=|27C1<qAcB_DIxm;xO$%;DuW5Up!;(RjoKMhYmd3)Sn$%u<afG8U6){bdDyvGZj#+$gSV#P$#JgPn$*mL*P{V89M*)-ZO-mSY5rHf{NbExQZj-3s+sTo>#tP%Hn*j{5%-mULGV6dz!}1asggq}BUl5EYE+m9k-K%1%F;sPzFsSt<34}g`Ir>sjU|a=7;kA0sG@mgw*_;A62c_`FU|NVO>OM8#5>yMz&uUmZlLv4`8!-;$C_GteSW!03b~!wfQq7F3L{0~BDnz-g2}h>=Z&sozg!HHR0%yG7z}%?h4#tsIO*9H!m~sFU(mSiyGmV*~giM9UjygB*31y_Zw{v9}@RhOI&-z%`&^SHYTSk7y>NI#VqOR-GGn(s>ogKp72S~EVQbREnJtXBew`{6urJx#m927>RQWTonfRR36w?H~etTfcz{DdPMgwSL>(g^I0jRZuZF+enh?XafnnL}V8=eSVNxKl1oYFk`J_PiUywj!Ux7S}q1^CkPFts{nB8IZUkMM&hzy#XGGF#elXNTe5mfnI=lKd=4k64SZFu`G9FaAENNzQ`I1<vv4o!xBb<3VeQAQfMOP<t(PIhm`Hm({xlsOC+Bd)Y?>h>JvO7Hm%}Tvr)(Ll3_v*qbG~w3T8qD<^8dy1*0vKj+#&#@l@tYzz&(6fzz$ln{6u3fkmW$tPt6f5-%WCIaDe}pUWbVR!~LQXP)YySalh2!1CplYtZEvXDAtp1>;E$1GnHyBnrDDpma%zXZu~nim?MKW@s))Pqf3WtH>y`!Z4{76kyL;DSTb_aGVQQ%jYO09E2`*`dn&Yf#o6&Ddw)GVZt1kD9-atWhyE$vGz1WhM+Q*nT0Ns&{cMty#M&I@BlC*2#IsaSuD$5eP9&ZA(%d)L0m$*1S3ifc_9f%S@T3XT1mN6=INtPH<5s>h`-45OEBfh;&bFyDbm6mNF}>oww>^53HPsFOQ4o`Fh4zTZV2-<<a!&fA)sKEj0%8ar4SQ^foh<M@(9RG(?q>)!FW0v;1P>QO@(=APq)!CRA^w>a+T;$0B$=<MN$~@CIVKXd%_W)ESu+sdZExI__APg%#@pR^}~G{<aM&}W-);Id-HJ@o}NkjtCs`RP&HCci~`Y5V|Xd69bV1)VHVBW{Bo8bbO%TvpGnGh;sPW#FsWUcu#2cZ<yoe&J<A8${VerC$^3ww(K%)#jET;0`t(d9^88)YU6O6bnM(E2Dnzg;$%4o9&j2e@n!(`k`PF;QS7Ycwoa8c)q$gikikQ%hluv$HB-XYxNo}WL9uKUyJcx{dCs6g_jL<Ql(t)u4NX4$sdQByDh;Un%#FWzw)&53Sp!ZY^Q3&2dGWubx`kafkl5G6ZoE<)Ar4H!8XJQ;H5A@dE%oP}%)>jH8Y`@xq<li{#2B;<QlFW*%u|zSPe{%Qr2r=BdgX=*UD2cwRN89@}?r8KJqI+pC0g8!);Cko68Uo#1x+-M_LU^)b2Q|f#Y89P|N=K7I?`6ESyIj}l=(5z|fHU`kA$5B9*Ju`lLbHC~g)A%7-3$n$mJhq@RK1-E?g4MF%F24na%B%+9^TW?R0osLsYGz}0+S=?c){!N5Y*3-t%q!;r&-hA!*NjlNDH_$(Y(QjCEz-8(A-DI`BfuNZ9=|~e-)&RYr%Z`2k`;vAv=51x{+T{V`fN8KCMW?*EydgggX&=FK+p#q6d+&SmTuMY5KA<3sHI{jqmwh6+UZ>n~bC)ms3@31jpo{ZF_T2F2DOP_oYu)S2M)*b0OA7VpT2RATN((RIsONu|O`xC#G7;JyX^Mtg)y@3KK#;vDBd=^aGe5)CEx^v6A(l371raQOgP=o9Ohlp)XbA6$_NHm%IYgXeLsV03@ggZQ+Uuww0|*E)hJILRo<x05td_pjz?`wr|J2a80Q!l1WoB{fN*XYKKk_t<4G!C5kW!!vGkz-0r92I&f0RXt1N(iiZ&4B8w<wIBaVH&WHTeAkf(kGd*K1z?L^t>B!rP9Q2-Vij=9PW_n(5lWY0i$3j{aCppvZWJ-C{${eMY;cMOSZnqf_mZ?NMA?TGQRdK=LYB7xm(&85oIOx%qwWSNy)m;U|$7C|ni$M+T3{)T^(8m(A+!MC3RMb1s5Ufwg(?z;eX&rSrjQc*MLcl+chNo_?m29Y7(}<J;rR7*(QsZooG35K%SjNy8bTY~A!GzPB3AxnhLZsc?SkUufAz9bcTD>6AgdmI<Td3TFXWp5OUbY$Q`=PT&1AJ>*!5uM=QVgfFrN^)Cy`qFgT|Lf+B(>&q`wL9tiQieVpl~vT{@GE-5gkr7oL(Noym5ska<;7MWaOWA423Jo=-i1zo%n|8;Ut&`>F$8Q2p~i$UZyE=adOAW*1eN9$0m>Gex!HF1UK+_3vAP=Cfec1ciX6bW5mV%`X*l`>l+lH#aVv&Q~}!L!k2BB^6~eEGn{%Bel~1Pek$;Gs#`wMr(-%GbXjSH_Q22{YUrslX?v1`wRszq2)`hebRmo)W;Qi!-dO?_>CEJ9;)f(xWT<wt4Y`$n84xQb-P4%DnNFE@FMe0Zdg>kASf+Fx&kK~9IAL=1f87y+Qhq$7Qcr<{pFS1f9@QZy+K-nOWnmXIvcUpDH{Tbxsjs=YQ2le-XJqYv$7)Vmd<z!FWk<OD7cVIDnbRHZ3O@=J1tacu2FEU*5SArnOS7H&vwCN#FruIoHSt+7kvlby%d`0gs-%|<QYeb-le$*a3dwE$ykt8vRf+`<fEnRr9H7w|ZrvAC*#S^3{)p{L!br!NQphRq`3oi5l&@TGh_VaE&qS&!fk?}!skG>gO!GavP+wJ}=Jvv)&P9D4&jEp#))t+)u5ebV?of<4JD;iXOmLf^F;N7ytcQC0f7^aXe9_EbdD+9l_;XWb@}iczvMhuVnNBVnr{CFNsqV|bKlO9n+O=fz5kLvk_l=eS9}29@ZIf%eM%+MK`!K_(iBdIBUi%rgs~@QaS8SI<n(C%E@abEBdq(@nWp%!MKsNQc^_iNZFcG#?dAA-?=?#hGYmJ+Ga%Cz6DpjY1j#Cshcv(-EgdTwBoP|#^5i?_jH|jHJOx}Ug9BNV}i5+7{g887gkLnGOBNJn+)=Rh}rN3FiGomI@)rTUepdo;_{hZnpI&_G#@W#Mc7)w^2<*3+EDmsB@yM0R*vp1ZCaVW`zSDI9EkLeWRox{g5E!WlLx&K;VlU<&Y3G)|NZsEQ!sY9c2gS-T@D}c2{{!fnI+)8EFL89z5dK)4P7$lEZJF{DFTq`hHA#C)5PE%(1JEDJr_sWeec1_$C)PrOz(+MIAPNbl6s;kSxX{x`_Fd*%6(dEf&M(u0q`U2J~E0Ek7{7C?Xah)F+tmiUIcC{9;go!5W;Uxqr6h1`>DV^o9=hM9A&^BI#D?Yya^;Rwcs3|Zq1xX4Fb$XGscS%+NGfHt|`4~V=7}i)MjOrlZ02JrY<bf^L<3cvOoYY)M4+QO`aDEkRt1y5??OU0ZfhqyHM7o<hj69alU{jL#xj2vXpq}%*=FBk*p=?ot+bA?so|qR*vldn`cA@gP^pE<%ydAHkN=6*xoSGoVX1Nr3S5~)^i0bPe^YzjU)R#zL_3>_0pj(h_z1-8@FU~A3#8p%d`?Obh5g&IE!f!(n<K3UQMw3*LwulnL9bht~C9U%)88AyL<bh#Zl-urMtf*oNMKF-X$*EeLj*g=_92vXTGT~mLn{aINi5gMbn*2I<;P=Y_-hkS1+43WXWB~)alq3U?qtxb5nNj)TIZ@s&Ci&L5=r5w_hT2O4+wqVWBgwL94boA6=yb0ODYb*YK!q%0;$oT=K^V2gmXXIDDWHHrjo3dMREJO5(I6UtX~nic?<X(uuRVU|Cd<00wqdz3*6-|`jR=K6F=%mem=eDf3iTx$ecLu0Kw9fIdy1thfi>UE^u4krlS39MQOP5<RMet=b(wNho`16YsISTxRj8z05gJ(x<*Bgwz2uTYG#%A~b{MUzc=cS_BEPfOiVAOdX2lijk4y>Qp;R!Z<CC=u5&7Swo`JSWcQ83G%undm->FT``Qe*5Bt)SgTctyuV*eiOU>&a2)FQ~3(us>cnalR^y<9+k5A#b|2Jq?!sn94>sQOYu$@1=pfa7|*p5eNva&=%eGkao_!CibHN~I5o@trvD?OQ8b*f4l3w?Si)vI(o`uCK(RQ$1#Sdh5xjC<QiyJDMRvjU(17;yX#!8>$M$iPRH;k6Em(K~r&NVW5gR9Gj9=CyIp@&~0YbToF1xf2FTW?>Y$})zK2FoB^4I54U4m$UwCMEZn2?z$NJ6N5H2t3P7o&U08zvL=<;)EKwDmn3)v*B#>Q+DHs=6X?<EGlz`C)3oodBNOvsHP^Tj_N;Ev!5?Vy&9(<i9Z4+<`lq6Vx)ss!;Xq-Y1gzM-L@1h?3(<GzOJhDJhkIDiRXUAQH04L6=ZksJ?Suq2^9`nrVjMEhd-I9ZeO;NM4uU8_&H%TWG%BXYoUGs`oKt)yFk6-;zP-Tm)7pf~0o{s|!GHfK?yom#}e)GEPetx^pTJ{KBS~jKLs~)_^Z9aV{dE31C7Tz|bTb-5(4h3UjQ{oLUa8sJp=0WU2U1s-YY$&#>N%2-8HJO0`;}F(?6WEt9$K6C2OBC{>_Q(;rD32D_G=Wk6-~RaN=O6z0{qxI-<T)fqcw*tg${t>}I)tlOKsuj09ZFDOFbKx72w%atYZ(9zQz(K6ARYj!YV)@$@WEvz(?h2aCn4nQCd%mbTuWY)gh>KMc7_aYb{d1EfD$b!p4kX?SCy`()>J?dWlRw-zjVV58=63yqie7Gb``4M$w(*SpNdbPwL+ye?x5-tuU6S%8t;x${J%7dmV!C9F7Ln%GCyqU9cI*&l^R;U|JCn<p&$&avin_@rV_>hmkN2MImghWl=MTAU$XzyFCT=<Y+Si7Hca1<efZ3|R9AV5D$$!?b?>9j5q`Bj4eex?yF-~UI2EZ$_}oPUW*xVBi;wI}OaJndtcZm<N3Xqz()QSLzCC0DsPV<>A11e4URI<;avR>FHrC~0q9y}*as4p-s=?LOx=TxH_eD<S@apxQlSOMh7J@@Z;^Z35?r8y)84XR~B$ds8Y2}8>Dp|_Wo4QruNwHwS4H`}vt)Nzr=Pe!9_7}M2_4Zp$HYHTC3`hV6q`Wjy1;OF<iKH1eltMRGXiMG{R#dHH-f!-9e#D~%=XE^G(+~A0ntrm@bh_i(J|&}65Kh=J9}lCzKi!<uHJw*xZLV1M@RrhA(uBgroH~nzIlP>l54C7s%sFDoBfCAd@pCM|*;2SpD&X&Sssm0z_b5owB?^o$7vO`&aJm5QF-EZ~xY(E9HHA4Yl>IwTX-^DIp$I9?R$AL<l-$iAb<?cd+aI2PdH>-#yuEI-u6w-4pPzpv0l(-5zZ9B8CQ(Xjt??BCao{=pHN-UDCtC1-jc*)Zfme<jyF5#`{glfEkt)Ey){ujco)k|Y9m*Ww?8U#zNUxiS=YNd2^z1+bUy;_4|9S!i*C@6hth+zkL0`W+Hs;Cb;zzOg<&XdQ@#Fsoabq0o')))
_ROUTES = {index: tape for index, tape in enumerate(_TAPES)}
_STAGES = [(144, 'shop_count', 'YARN_STORE', 0.5, 1, 0, ()), (648, 'market_inventory', 'EGG', 9888, 3, 2, ())]
_SETTINGS = {'hand_align': False, 'weed_repair': False, 'sell_lead': True, 'front_run': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': False}


def _shop_count(observation, name):
    shops = _get(_get(observation, 'town', {}) or {}, 'unlocked_shops', []) or []
    return list(shops).count(name)


def _market_inventory(observation, item):
    market = _get(observation, 'market', {}) or {}
    return _int(_get(_get(market, 'inventory', {}) or {}, item, 10000), 10000)


_READERS = {'shop_count': _shop_count, 'market_inventory': _market_inventory}


def _router(observation, step, state):
    """One latched decision per stage; anything unreadable holds the current route.

    Each stage fires on the first step at or after its own step and never again, so
    a stage decides on the state of the world at the moment it was fitted for and a
    later swing in the same feature cannot flip a plan mid-flight.

    `when` names the routes a stage may fire from. A stage whose alternatives are
    variants of one season plan must not fire while a different season plan is
    running, because the tapes it chooses between were never written to follow the
    state that plan produces. The latch is still set either way, so a skipped stage
    does not fire later from a route it was not meant to leave.
    """
    for index, stage in enumerate(_STAGES):
        at, kind, subject, threshold, above, below, when = stage
        key = 'stage_%d' % index
        if step < at or state.get(key):
            continue
        state[key] = True
        if when and state.get('route', 0) not in when:
            continue
        try:
            value = _READERS[kind](observation, subject)
        except Exception:
            continue
        state['route'] = above if value > threshold else below
    return state.get('route', 0)


_IMPL = make_agent(_ROUTES, router=_router, **_SETTINGS)


def agent(observation, configuration=None):
    # Keep the entry point last: Kaggle selects the last module-level callable.
    try:
        return _IMPL(observation, configuration)
    except Exception:
        return {'farmer': ['PASS'], 'hands': [], 'market': []}
