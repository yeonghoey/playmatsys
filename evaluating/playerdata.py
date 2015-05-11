# define models related with Player

from kivy.event      import EventDispatcher
from kivy.properties import DictProperty, ListProperty


class PlayerData(EventDispatcher):
    players = DictProperty({})
    lteam   = ListProperty([])
    cteam   = ListProperty([])
    rteam   = ListProperty([])

def move_team(from_team, to_team, name):
    if name     in from_team: from_team.remove(name)
    if name not in   to_team:   to_team.append(name)
