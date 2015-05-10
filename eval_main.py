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

gp_points  = partial(graph_calc.points, *(RATING_RANGE))
new_rating = partial(trueskill.Rating, mu=50.0, sigma=16.3333)

class EvalLayout(Accordion):
    prepare = ObjectProperty(None)

class PrepareScene(AccordionItem):
    # kv ref
    red_list     = ObjectProperty(None)
    neutral_list = ObjectProperty(None)
    blue_list    = ObjectProperty(None)
    graph        = ObjectProperty(None)

    # py ref
    plotr = ObjectProperty(None)
    plotb = ObjectProperty(None)
    plotv = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(PrepareScene, self).__init__(*args, **kwargs)

class RedList(BoxLayout):
    neutral_list = ObjectProperty(None)

    def add_player(self, player):
        row = ListItem(player, {'right': self.neutral_list})
        self.add_widget(row)

    def remove_player(self, player):
        pass
    

class NeutralList(BoxLayout):
    red_list = ObjectProperty(None)
    blue_list = ObjectProperty(None)

    def add_player(self, player):
        btn_target = \
            {'left': self.red_list, 'right': self.blue_list}
        row = ListItem(player, btn_target)
        self.add_widget(row)

    def remove_player(self, player):
        pass

class BlueList(BoxLayout):
    neutral_list = ObjectProperty(None)

    def add_player(self, player):
        row = ListItem(player, {'left': self.neutral_list})
        self.add_widget(row)

    def remove_player(self, player):
        pass

class ListItem(BoxLayout):
    name  = ObjectProperty(None)
    left  = ObjectProperty(None)
    right = ObjectProperty(None)

    def __init__(self, player, btn_target):
        super(ListItem, self).__init__()
        self.player     = player
        self.btn_target = btn_target

        if 'left'  not in btn_target:
            self.remove_widget(self.left)
        if 'right' not in btn_target:
            self.remove_widget(self.right)

        self.name.text  = player['name']

    def on_btnleft(self, name):
        self._move_to(self.btn_target['left'])

    def on_btnright(self, name):
        self._move_to(self.btn_target['right'])

    def _move_to(self, target):
        self.parent.remove_player(self.player)
        self.parent.remove_widget(self)
        target.add_player(self.player)


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


    def init_preaprescene(self):
        accitem       = Builder.load_file('scenes/prepare.kv')
        accitem.title = 'prepare'

        accitem.plotr = SmoothLinePlot(color=COLOR_RED)
        accitem.plotb = SmoothLinePlot(color=COLOR_BLUE)
        accitem.plotv = SmoothLinePlot(color=COLOR_VIOLET)

        graph = accitem.graph
        graph.add_plot(accitem.plotr)
        graph.add_plot(accitem.plotb)
        graph.add_plot(accitem.plotv)

        self.root.prepare = accitem
        self.root.add_widget(accitem)

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
if __name__ == '__main__':
    EvalApp().run()
