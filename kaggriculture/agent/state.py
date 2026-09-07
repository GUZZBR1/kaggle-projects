from dataclasses import dataclass


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
        return self.obs.get('step', self.day * self.turns_per_day + self.hour)

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

    def tiles(self, opponent=False):
        farm = self.opponent if opponent else self.me
        return [(x, y, tile) for y, row in enumerate(farm['tiles'])
                for x, tile in enumerate(row) if tile != 'LOCKED']
