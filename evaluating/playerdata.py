# define models related with Player

from kivy.event      import EventDispatcher
from kivy.properties import DictProperty, ListProperty


class PlayerData(EventDispatcher):
    players = DictProperty({})
    lteam   = ListProperty([])
    cteam   = ListProperty([])
    rteam   = ListProperty([])
