# define models related with Player

from kivy.event      import EventDispatcher
from kivy.properties import ListProperty, NumericProperty, \
                            ObjectProperty, StringProperty 

class Player(EventDispatcher):
    name   = StringProperty('')
    mean   = NumericProperty(0)
    stddev = NumericProperty(0)

class Team(EventDispatcher):
    members = ListProperty([])

    def add_player(self, player):
        if player not in self.members:
            self.members.append(player)

    def remove_player(self, player):
        if player in self.members:
            self.members.remove(player)

def move_team(player, from_team, to_team):
    from_team.remove_player(player)
    to_team.add_player(player)

if __name__ == '__main__':
    p1 = Player()
    t1 = Team()
    t2 = Team()

    t1.add_player(p1)
    t1.remove_player(p1)
    t1.remove_player(p1)
    t2.add_player(p1)

    move_team(p1, t2, t1)
