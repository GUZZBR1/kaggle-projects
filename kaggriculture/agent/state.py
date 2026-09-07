from dataclasses import dataclass
import math


@dataclass
class State:
    obs: dict
    config: dict

    @property
    def me(self):
        return self.obs['farms'][self.obs['player']]

    @property
    def opponent(self):
        return self.obs['farms'][1 - self.obs['player']]

    @property
    def private(self):
        return self.obs['private']

    @property
    def day(self):
        return self.obs['day']

    @property
    def hour(self):
        return self.obs['hour']

    @property
    def turns_per_day(self):
        return self.config.get('turnsPerDay', 24)

    @property
    def step(self):
        day, hour, turns = self.day, self.hour, self.turns_per_day
        if (type(day) is not int or type(hour) is not int or type(turns) is not int
                or day < 0 or turns <= 0 or not 0 <= hour < turns):
            raise ValueError('Malformed day/hour clock')
        derived = day * turns + hour
        supplied = self.obs.get('step')
        if supplied is not None and (type(supplied) is not int or supplied != derived):
            raise ValueError('step disagrees with canonical day/hour clock')
        return derived

    @property
    def turns_left(self):
        # Official framework records the initial state: 720 states = 719 actions.
        return self.config.get('episodeSteps', 720) - 1 - self.step

    @property
    def days_left(self):
        return self.turns_left / self.turns_per_day

    @property
    def positions(self):
        return [self.me['farmer'], *self.me['hands']]

    @property
    def size(self):
        return len(self.me['tiles'])

    def risk_posture(self, window_days=5, min_buffer=1000,
                     buffer_fraction=.1):
        """Classify the public cash gap near season end, failing safely."""
        if self.days_left > window_days:
            return 'neutral'
        try:
            own = self.me['money']
            other = self.opponent['money']
            if isinstance(own, bool) or isinstance(other, bool):
                return 'neutral'
            own = float(own)
            other = float(other)
            if not math.isfinite(own) or not math.isfinite(other):
                return 'neutral'
            buffer = max(float(min_buffer), float(buffer_fraction) * max(own, other))
        except (KeyError, TypeError, ValueError, OverflowError):
            return 'neutral'
        margin = own - other
        if margin > buffer:
            return 'ahead'
        if margin < -buffer:
            return 'behind'
        return 'neutral'

    def tiles(self, opponent=False):
        farm = self.opponent if opponent else self.me
        return [(x, y, tile) for y, row in enumerate(farm['tiles'])
                for x, tile in enumerate(row) if tile != 'LOCKED']
