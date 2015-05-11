# kivy dependencies
from kivy.config import Config
Config.read('config.ini')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.properties import BooleanProperty, ListProperty, \
    NumericProperty, ObjectProperty, StringProperty 
from kivy.garden.graph import Graph, MeshLinePlot, MeshStemPlot, SmoothLinePlot

# stdlib dependencies
from functools import partial

# trueskill
import trueskill

# project dependencies
from settings import *
import graph_calc

from player import Player, Team, move_team


gp_points  = partial(graph_calc.points, *(RATING_RANGE))
new_rating = partial(trueskill.Rating, mu=50.0, sigma=16.3333)


class TopLayout(BoxLayout):
    mainacc = ObjectProperty(None)

class MainAccordion(Accordion):
    prepare = ObjectProperty(None)

class EvaluatingApp(App):

    lteam = ObjectProperty(None)
    cteam = ObjectProperty(None)
    rteam = ObjectProperty(None)

    def build(self):
        self.build_data()
        self.build_root()

    def build_data(self):
        self.lteam = Team()
        self.cteam = Team()
        self.rteam = Team()

        for n in PLAYERS:
            player = Player( \
                name = n, mean = MEAN, stddev = STDDEV)
            self.cteam.add_player(player)

    def build_root(self):
        self.build_mainacc(self.root.mainacc)

    def build_mainacc(self, mainacc):
        accitem       = Builder.load_file('prepare.kv')
        accitem.title = 'prepare'

        graph = accitem.graph

#        plot = SmoothLinePlot(color=COLOR_LEFT)
#        graph.add_plot(plot)
#
#        plotb = SmoothLinePlot(color=COLOR_BLUE)
#        plotv = SmoothLinePlot(color=COLOR_VIOLET)
#
#        graph.add_plot(accitem.plotb)
#        graph.add_plot(accitem.plotv)

        mainacc.add_widget(accitem)
        mainacc.prepare = accitem
        

if __name__ == '__main__':
    EvaluatingApp().run()

#class EvalLayout(Accordion):
#    prepare = ObjectProperty(None)
#
#class PrepareScene(AccordionItem):
#    # kv ref
#    red_list     = ObjectProperty(None)
#    neutral_list = ObjectProperty(None)
#    blue_list    = ObjectProperty(None)
#    graph        = ObjectProperty(None)
#
#    # py ref
#    plotr = ObjectProperty(None)
#    plotb = ObjectProperty(None)
#    plotv = ObjectProperty(None)
#
#    def __init__(self, *args, **kwargs):
#        super(PrepareScene, self).__init__(*args, **kwargs)
#
#class ListItem(BoxLayout):
#    name  = ObjectProperty(None)
#    left  = ObjectProperty(None)
#    right = ObjectProperty(None)
#
#    def __init__(self, player, btn_target):
#        super(ListItem, self).__init__()
#        self.player     = player
#        self.btn_target = btn_target
#
#        if 'left'  not in btn_target:
#            self.remove_widget(self.left)
#        if 'right' not in btn_target:
#            self.remove_widget(self.right)
#
#        self.name.text  = player['name']
#
#    def on_btnleft(self, name):
#        self._move_to(self.btn_target['left'])
#
#    def on_btnright(self, name):
#        self._move_to(self.btn_target['right'])
#
#    def _move_to(self, target):
#        self.parent.remove_player(self.player)
#        self.parent.remove_widget(self)
#        target.add_player(self.player)


class EvalApp(App):
    players = ListProperty([])

    def build(self):
        self.init_preaprescene()
        self.init_players()

#        add_accitem('win',  Builder.load_file('scenes/result.kv'))
#        add_accitem('draw', Builder.load_file('scenes/result.kv'))
#        add_accitem('lose', Builder.load_file('scenes/result.kv'))

        root = self.root
        root.select(root.children[-1])



    def init_players(self):
        for name in PLAYERS:
            self.players.append( {'name': name, 'rating': new_rating()} )

        neutral_list = self.root.prepare.neutral_list
        for p in self.players:
             neutral_list.add_player(p)



#        points = [(x, scipy.stats.norm(50, 16.3).pdf(x)) for x in range(0, 100)]
#
#        plot = SmoothLinePlot(color=[1, 0, 0, 1])
#        plotsub = MeshStemPlot(color=[1, 0, 0, 1])
#
#        plot.points = points
#        graph.add_plot(plot)
#        graph.add_plot(plotsub)
#
#    def load_screen(self, name):
#        screen = Builder.load_file(name.lower())
#        graph = screen.graph
#
#        points = [(x, scipy.stats.norm(50, 16.3).pdf(x)) for x in range(0, 100)]
#        plot = MeshLinePlot(color=[1, 0, 0, 1])
#
#        plot.points = points
#        graph.ymax = 0.1
#        graph.add_plot(plot)
#        return screen
#
#    def go_next_screen(self):
#        screen = self.load_screen('screens/before.kv')
#        sm = self.root.ids.sm
#        sm.add_widget(screen)
#
