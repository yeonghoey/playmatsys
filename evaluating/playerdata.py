# define models related with Player

from kivy.event      import EventDispatcher
from kivy.properties import DictProperty, ListProperty

# trueskill
from trueskill import TrueSkill

# project
from settings import *

_tscalc = TrueSkill(mu = MEAN, sigma = STDDEV, \
                    beta = STDDEV/2., tau = STDDEV/100.)


class PlayerData(EventDispatcher):
    players = DictProperty({})
    lteam   = ListProperty([])
    cteam   = ListProperty([])
    rteam   = ListProperty([])

    def rating(self, name):
        return self.players[name]

    def ratings(self, team):
        return [self.players[name] for name in team]

    def lwin(self): return self._rate([1, 2])
    def draw(self): return self._rate([1, 1])
    def rwin(self): return self._rate([2, 1])

    def _rate(self, ranks):
        lrs = self.ratings(self.lteam) # left  team ratings
        rrs = self.ratings(self.rteam) # right team ratings

        # empty team, no match
        if (not lrs) or (not rrs): return {}

        # float pairs -> trueskkill -> calculate post skills -> float pairs
        tsgroups = [_trueskills(lrs), _trueskills(rrs)]
        tsafter  = _tscalc.rate(tsgroups,ranks=ranks)
        lafter   = _floatpairs(tsafter[0])
        rafter   = _floatpairs(tsafter[1])

        afterplayers = {}
        for i, name in enumerate(self.lteam):
            afterplayers[name] = lafter[i]
        for i, name in enumerate(self.rteam):
            afterplayers[name] = rafter[i]

        return afterplayers


def _trueskills(floatpairs):
    return map(lambda x: _tscalc.create_rating(x[0], x[1]), floatpairs)

def _floatpairs(trueskills):
    return map(lambda x: (x.mu, x.sigma), trueskills)
