from kivy.properties    import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import AccordionItem
from kivy.garden.graph  import Graph, SmoothLinePlot, MeshStemPlot

from functools import partial

class PrepareAccItem(AccordionItem):
    llist = ObjectProperty(None)
    clist = ObjectProperty(None)
    rlist = ObjectProperty(None)
    graph = ObjectProperty(None)

    def associate(self, playerdata):
        self.llist.associate(playerdata)
        self.clist.associate(playerdata)
        self.rlist.associate(playerdata)


class PlayerList(BoxLayout):
    def new_item(self, name):
        item = ListItem()
        item.set_name(name)
        item.set_lbtn_handler(self.lbtn_handler)
        item.set_rbtn_handler(self.rbtn_handler)
        return item

    def team_changed(self, instnace, value):
        self.clear_widgets()
        new_names = value
        for nn in new_names:
            self.add_widget(self.new_item(nn))


class LeftList(PlayerList):
    def associate(self, playerdata):
        playerdata.bind(lteam = self.team_changed)
        self.lbtn_handler = None
        self.rbtn_handler = \
            partial(_move_team, playerdata.lteam, playerdata.cteam) 


class CenterList(PlayerList):
    def associate(self, playerdata):
        playerdata.bind(cteam = self.team_changed)
        self.lbtn_handler = \
            partial(_move_team, playerdata.cteam, playerdata.lteam) 
        self.rbtn_handler = \
            partial(_move_team, playerdata.cteam, playerdata.rteam) 


class RightList(PlayerList):
    def associate(self, playerdata):
        playerdata.bind(rteam = self.team_changed)
        self.lbtn_handler = \
            partial(_move_team, playerdata.rteam, playerdata.cteam) 
        self.rbtn_handler = None


class ListItem(BoxLayout):
    name = ObjectProperty(None)
    lbtn = ObjectProperty(None)
    rbtn = ObjectProperty(None)

    def set_name(self, name):
        self.name.text = name

    def set_lbtn_handler(self, lbtn_handler):
        if not lbtn_handler:
            self.remove_widget(self.lbtn)
        else:
            self.on_lbtn = lbtn_handler

    def set_rbtn_handler(self, rbtn_handler):
        if not rbtn_handler:
            self.remove_widget(self.rbtn)
        else:
            self.on_rbtn = rbtn_handler


def _move_team(from_team, to_team, name):
    if name     in from_team: from_team.remove(name)
    if name not in   to_team:   to_team.append(name)


class CompGraphLayout(BoxLayout):
    pass
