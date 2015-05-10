from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.garden.graph import Graph, MeshLinePlot, MeshStemPlot, SmoothLinePlot
from math import sin
import scipy.stats

class EvalScreen(Screen):
    graph = ObjectProperty(None)

class EvalApp(App):
    def build(self):
        self.go_next_screen()

#        graph = self.root.ids.graph
#        graph.xlabel = 'X'
#        graph.ylabel = 'Y'
#        graph.x_ticks_minor = 5
#        graph.x_ticks_major = 10
#        graph.y_ticks_major = 0.1
#        graph.y_grid_label = True
#        graph.x_grid_label = True
#        graph.padding = 5
#        graph.x_grid = True
#        graph.y_grid = True
#        graph.xmin = 0
#        graph.xmax = 100
#        graph.ymin = 0
#        graph.ymax = 0.1
#       
#        points = [(x, scipy.stats.norm(50, 16.3).pdf(x)) for x in range(0, 100)]
#
#        plot = SmoothLinePlot(color=[1, 0, 0, 1])
#        plotsub = MeshStemPlot(color=[1, 0, 0, 1])
#
#        plot.points = points
#        graph.add_plot(plot)
#        graph.add_plot(plotsub)
#
    def load_screen(self, name):
        screen = Builder.load_file(name.lower())
        graph = screen.graph

        points = [(x, scipy.stats.norm(50, 16.3).pdf(x)) for x in range(0, 100)]
        plot = MeshLinePlot(color=[1, 0, 0, 1])

        plot.points = points
        graph.ymax = 0.1
        graph.add_plot(plot)
        return screen

    def go_next_screen(self):
        screen = self.load_screen('screens/before.kv')
        sm = self.root.ids.sm
        sm.add_widget(screen)

if __name__ == '__main__':
    EvalApp().run()
