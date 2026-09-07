"""Read actual interpreter commits, never infer executions from requested orders."""
from collections import Counter
import copy


class EconomicTelemetry:
    def __init__(self, module):
        self.module = module
        self.originals = {name: getattr(module, name) for name in
                          ('_process_market', '_parse_order', '_commit_unit', '_do_hire', '_do_buy_land')}
        self.daily = [{}, {}]
        self.active = False
        self.current = [None, None]
        self.order_map = {}

    def install(self):
        for name, wrapper in [('_process_market', self.market), ('_parse_order', self.parse),
                              ('_commit_unit', self.commit), ('_do_hire', self.hire),
                              ('_do_buy_land', self.land)]:
            setattr(self.module, name, wrapper)

    def restore(self):
        for name, function in self.originals.items():
            setattr(self.module, name, function)

    def row(self, seat, day):
        return self.daily[seat].setdefault(day, dict(day=day, turns=0,
                  orders=Counter(), sales={}, buys=Counter(), hires=0, plantings=0,
                  hand_turns=0, cash_start=None, cash_end=None, cash_min=None,
                  hands_start=None, hands_end=None, hands_peak=0, quadrants_end=0, occupied_end=0,
                  expenditure=Counter(), unit_actions=Counter(), harvests=0, pass_actions=0,
                  ineffective_actions=0, overflow_items=0, first_revenue_step=None,
                  animals_end={}, shed_start={}, shed_end={}, inventories_start=[], inventories_end=[],
                  shed_peak=0, carried_peak=0, shed_capacity=0, cash_reconciliation_error=0))

    def pressure(self, row, private):
        row['shed_peak'] = max(row['shed_peak'], sum(private['shed'].values()))
        row['carried_peak'] = max(row['carried_peak'], sum(sum(i.values()) for i in private['inventories']))

    def begin_turn(self, observations):
        self.day = int(observations[0]['day'])
        for seat, obs in enumerate(observations):
            farm = obs['farms'][seat]
            row = self.row(seat, self.day)
            cash = float(farm['money'])
            if row['cash_start'] is None:
                row['cash_start'] = cash
                row['hands_start'] = len(farm['hands'])
                row['shed_start'] = copy.deepcopy(obs['private']['shed'])
                row['inventories_start'] = copy.deepcopy(obs['private']['inventories'])
            row['cash_min'] = cash if row['cash_min'] is None else min(row['cash_min'], cash)
            row['turns'] += 1
            row['hand_turns'] += len(farm['hands'])
            row['hands_peak'] = max(row['hands_peak'], len(farm['hands']))
            self.pressure(row, obs['private'])
        self.step = int(observations[0]['day']) * self.turns_per_day + int(observations[0]['hour'])

    def finish_turn(self, state, before_audit, audit):
        for seat, farm in enumerate(state[0].observation.farms):
            row = self.row(seat, self.day)
            row['cash_end'] = float(farm['money'])
            row['cash_min'] = min(row['cash_min'], row['cash_end'])
            row['hands_end'] = len(farm['hands'])
            row['quadrants_end'] = len(farm['unlocked_quadrants'])
            row['occupied_end'] = sum(isinstance(t, dict) for line in farm['tiles'] for t in line)
            row['animals_end'] = dict(Counter(t['animal'] for line in farm['tiles'] for t in line
                                             if isinstance(t, dict) and t.get('animal')))
            private = state[seat].observation.private
            row['shed_end'] = copy.deepcopy(dict(private.shed))
            row['inventories_end'] = copy.deepcopy(list(private.inventories))
            row['shed_capacity'] = self.shed_capacity
            self.pressure(row, private)
            counts, before = audit.counts[seat], before_audit[seat]
            row['plantings'] += (counts['op_PLANT'] - before['op_PLANT']
                                 - counts['no_effect_PLANT'] + before['no_effect_PLANT'])
            row['harvests'] += (counts['op_HARVEST'] - before['op_HARVEST']
                                - counts['no_effect_HARVEST'] + before['no_effect_HARVEST'])
            row['pass_actions'] += counts['op_PASS'] - before['op_PASS']
            row['ineffective_actions'] += counts['no_effect_actions'] - before['no_effect_actions']
            row['overflow_items'] += counts['overflow_items'] - before['overflow_items']
            for key, value in counts.items():
                if key.startswith('op_'):
                    row['unit_actions'][key[3:]] += value - before[key]
            row['cash_reconciliation_error'] = (row['cash_end'] - row['cash_start']
                - sum(s['revenue'] for s in row['sales'].values()) + sum(row['expenditure'].values()))

    def parse(self, order):
        parsed = self.originals['_parse_order'](order)
        if self.active:
            seat, index = next(self.parse_sequence)
            self.current[seat] = index
            self.events[seat][index]['parsed'] = parsed is not None
        return parsed

    def commit(self, op, item, price, farm, private, market, *args, **kwargs):
        ok = self.originals['_commit_unit'](op, item, price, farm, private, market, *args, **kwargs)
        if self.active:
            seat = self.private_seats[id(private)]
            event = self.events[seat][self.current[seat]]
            event['units'] += int(ok)
            event['failed_units'] += int(not ok)
            row = self.row(seat, self.day)
            row['cash_min'] = min(row['cash_min'], float(farm['money']))
            if ok and op == 'SELL':
                sale = row['sales'].setdefault(item, dict(units=0, revenue=0))
                sale['units'] += 1
                sale['revenue'] += price
                if row['first_revenue_step'] is None:
                    row['first_revenue_step'] = self.step
            elif ok:
                row['buys'][op + ':' + str(item)] += 1
                row['expenditure'][op + ':' + str(item)] += price
            self.pressure(row, private)
        return ok

    def hire(self, farm, private, *args, **kwargs):
        before = farm['hires_today']
        cash_before = farm['money']
        result = self.originals['_do_hire'](farm, private, *args, **kwargs)
        if self.active:
            seat = self.private_seats[id(private)]
            ok = farm['hires_today'] > before
            self.events[seat][self.current[seat]]['units'] += int(ok)
            row = self.row(seat, self.day)
            row['hires'] += int(ok)
            row['cash_min'] = min(row['cash_min'], float(farm['money']))
            row['expenditure']['HIRE'] += cash_before - farm['money']
            row['hands_peak'] = max(row['hands_peak'], len(farm['hands']))
        return result

    def land(self, farm, *args, **kwargs):
        before = len(farm['unlocked_quadrants'])
        cash_before = farm['money']
        result = self.originals['_do_buy_land'](farm, *args, **kwargs)
        if self.active:
            seat = self.farm_seats[id(farm)]
            self.events[seat][self.current[seat]]['units'] += int(len(farm['unlocked_quadrants']) > before)
            row = self.row(seat, self.day)
            row['cash_min'] = min(row['cash_min'], float(farm['money']))
            row['expenditure']['BUY_LAND'] += cash_before - farm['money']
        return result

    def market(self, state, env):
        self.events = [[], []]
        self.order_map = {}
        self.private_seats = {id(s.observation.private): i for i, s in enumerate(state)}
        self.farm_seats = {id(f): i for i, f in enumerate(state[0].observation.farms)}
        limit = max(1, int(env.configuration.maxMarketOrdersPerTurn))
        for seat, s in enumerate(state):
            orders = s.action.get('market', [])
            orders = orders if isinstance(orders, list) else []
            for index, order in enumerate(orders):
                self.order_map[id(order)] = (seat, index)
                op = str(order[0]) if isinstance(order, list) and order else 'MALFORMED'
                self.events[seat].append(dict(op=op, parsed=False, units=0, failed_units=0,
                                              truncated=index >= limit))
        self.parse_sequence = iter((seat, index) for index in range(limit) for seat in (0, 1)
                                   if index < len(self.events[seat]))
        self.active = True
        try:
            return self.originals['_process_market'](state, env)
        finally:
            self.active = False
            for seat, events in enumerate(self.events):
                counts = self.row(seat, self.day)['orders']
                for event in events:
                    op = event['op']
                    counts['requested'] += 1
                    counts['requested:' + op] += 1
                    status = ('truncated' if event['truncated'] else 'invalid' if not event['parsed']
                              else 'executed' if event['units'] else 'failed')
                    counts[status] += 1
                    counts[status + ':' + op] += 1
                    if event['units'] and event['failed_units']:
                        counts['partial'] += 1

    def output(self, seat):
        result = copy.deepcopy(list(self.daily[seat].values()))
        for row in result:
            row['hands_mean'] = row['hand_turns'] / max(1, row['turns'])
            row['revenue'] = sum(s['revenue'] for s in row['sales'].values())
            for sale in row['sales'].values():
                sale['realized_price'] = sale['revenue'] / sale['units']
        return result
