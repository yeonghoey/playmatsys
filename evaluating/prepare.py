# kivy
from kivy.properties    import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import AccordionItem
from kivy.garden.graph  import Graph, MeshStemPlot

#stdlib
from math      import sqrt
from functools import partial

# project
from settings  import *
from graphcalc import build_points


class PrepareScene(BoxLayout):
    llist   = ObjectProperty(None) # kv
    clist   = ObjectProperty(None) # kv
    rlist   = ObjectProperty(None) # kv
    glayout = ObjectProperty(None) # kv

    def build(self):
        self.glayout.build()

    def refresh(self):
        pass

    def associate(self, pdata):
        self.llist.associate(pdata)
        self.clist.associate(pdata)
        self.rlist.associate(pdata)
        self.glayout.associate(pdata)


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
    def associate(self, pdata):
        pdata.bind(lteam = self.team_changed)
        self.lbtn_handler = None
        self.rbtn_handler = \
            partial(_move_team, pdata.lteam, pdata.cteam) 


class CenterList(PlayerList):
    def associate(self, pdata):
        pdata.bind(cteam = self.team_changed)
        self.lbtn_handler = \
            partial(_move_team, pdata.cteam, pdata.lteam) 
        self.rbtn_handler = \
            partial(_move_team, pdata.cteam, pdata.rteam) 


class RightList(PlayerList):
    def associate(self, pdata):
        pdata.bind(rteam = self.team_changed)
        self.lbtn_handler = \
            partial(_move_team, pdata.rteam, pdata.cteam) 
        self.rbtn_handler = None


class ListItem(BoxLayout):
    name = ObjectProperty(None) # kv
    lbtn = ObjectProperty(None) # kv
    rbtn = ObjectProperty(None) # kv

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

    graph = ObjectProperty(None) # kv
    lplot = ObjectProperty(None)
    rplot = ObjectProperty(None)
    pdata = ObjectProperty(None)

    def build(self):
        self.lplot = MeshStemPlot(color=COLOR_LEFT)
        self.graph.add_plot(self.lplot)

        self.rplot = MeshStemPlot(color=COLOR_RIGHT)
        self.graph.add_plot(self.rplot)

    def associate(self, pdata):
        self.pdata = pdata
        pdata.bind(players=self.redraw_all)
        pdata.bind(lteam=self.redraw_left)
        pdata.bind(rteam=self.redraw_right)

    def redraw_all(self, instance, value):
        self.redraw_left (instance, self.pdata.lteam)
        self.redraw_right(instance, self.pdata.rteam)

    def redraw_left(self, instance, value):
        self._redraw_target(self.lplot, value)

    def redraw_right(self, instance, value):
        self._redraw_target(self.rplot, value)

    def _redraw_target(self, plot, team):
        if not team:
            plot.points = []
            return
        teamrating  = self._calc_teamrating(team)
        plot.points = build_points(*teamrating)
        self._update_graphmaxes()

    def _calc_teamrating(self, team):
        ratings = self.pdata.ratings(team)
        means, stddevs = zip(*ratings)
        tmean   = sum(means)
        tstddev = sqrt(sum(map(lambda x: x*x, stddevs)))
        return tmean, tstddev

    def _update_graphmaxes(self):
        lx, ly = _calc_maxes(self.lplot.points)
        rx, ry = _calc_maxes(self.rplot.points)
        self.graph.xmax = max(lx, rx)
        self.graph.ymax = max(ly, ry, GRAPH_YMAX)

def _calc_maxes(points):
    if not points:
        return GRAPH_XMAX, GRAPH_YMAX

    xs, ys = zip(*points)
    return max(xs), max(ys)
