# kivy dependencies
from kivy.config import Config
Config.read('config.ini')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
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


class EvalLayout(BoxLayout):
    acc = ObjectProperty(None)

class EvalApp(App):
    players = ListProperty([])

    def build(self):
        self.build_players()

        self.scenes = {}
        acc = self.root.acc

        def add_accitem(title, plotsetter, scene):
            scene.title = title
            acc.add_widget(scene)
            self.scenes[title] = scene
            if scene.graph:
                plotsetter(scene)
            return scene

        def prepare_plots(scene):
            scene.plotr = SmoothLinePlot(color=COLOR_RED)
            scene.graph.add_plot(scene.plotr)
            scene.plotb = SmoothLinePlot(color=COLOR_BLUE)
            scene.graph.add_plot(scene.plotb)
            scene.plotv = SmoothLinePlot(color=COLOR_VIOLET)
            scene.graph.add_plot(scene.plotv)
        
        def result_plots(graph):
            pass

        add_accitem('prepare', prepare_plots,
            Builder.load_file('scenes/prepare.kv'))

        add_accitem('win', result_plots,
            Builder.load_file('scenes/result.kv'))
        add_accitem('draw', result_plots,
            Builder.load_file('scenes/result.kv'))
        add_accitem('lose', result_plots,
                Builder.load_file('scenes/result.kv'))

        acc.select(acc.children[-1])

    def build_players(self):
        for i in xrange(4):
            self.players.append(new_rating())

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
