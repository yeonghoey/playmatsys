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

# project dependencies
from settings   import *
from playerdata import PlayerData


class TopLayout(BoxLayout):
    mainacc = ObjectProperty(None)

class MainAccordion(Accordion):
    prepare = ObjectProperty(None)

class EvaluatingApp(App):
    pdata = ObjectProperty(PlayerData())

    def build(self):
        self.build_root()
        self.build_data()

    def build_root(self):
        self.build_mainacc(self.root.mainacc)

    def build_mainacc(self, mainacc):
        mainacc.add_widget(self.build_prepare())

    def build_prepare(self):
        accitem = Builder.load_file('prepare.kv')
        accitem.title = 'prepare'
        accitem.build_graphlayout()
        accitem.associate(self.pdata)
        return accitem

    def build_data(self):
        players = self.pdata.players 
        cteam   = self.pdata.cteam
        for name in PLAYERS:
            players[name] = (MEAN, STDDEV)
            cteam.append(name)

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
