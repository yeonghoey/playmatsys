# kivy
from kivy.app            import App
from kivy.properties     import ObjectProperty
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion  import Accordion, AccordionItem
from kivy.garden.graph   import Graph, SmoothLinePlot, MeshStemPlot

#stdlib
from math      import sqrt
from functools import partial


# project
from settings  import *
from graphcalc import build_points


class ResultScene(BoxLayout):
    graphslayout = ObjectProperty(None) # kv
    applybtn     = ObjectProperty(None) # kv

    pdata    = ObjectProperty(None)
    ratefunc = ObjectProperty(None)

    def build(self):
        self.applybtn.bind(on_press=self.apply_after)

    def apply_after(self, button):
        if not self.pdata: return

        afterplayers = self._build_after()
        for name, after in afterplayers.iteritems():
            self.pdata.players[name] = after

        App.get_running_app().show_prepare()

    def associate(self, pdata, ratefunc):
        self.pdata    = pdata
        self.ratefunc = ratefunc

    def refresh(self):
        afterplayers = self._build_after() # calculate expecting
        players      = sorted(afterplayers.iteritems())

        graphbuild_info = []
        for name, after in players:
            info = {'name': name, 'after': after} 

            if   name in self.pdata.lteam: info['color'] = COLOR_RED
            elif name in self.pdata.rteam: info['color'] = COLOR_BLUE
            else: continue # unexpected

            info['before'] = self.pdata.rating(name)
            graphbuild_info.append(info)

        self.graphslayout.rebuild_graphs(graphbuild_info)

    def _build_after(self):
        if not self.pdata:    return {}
        if not self.ratefunc: return {}
        return self.ratefunc()


class GraphsLayout(GridLayout):
    def rebuild_graphs(self, graphbuild_info):
        self.clear_widgets()

        for info in graphbuild_info:
            diffgraph = DiffGraphLayout()
            diffgraph.build(**info)
            self.add_widget(diffgraph)

        # hard code. make grid layout pretty
        if len(graphbuild_info) > 4:
            self.cols = None
            self.rows = 2
        else:
            self.rows = None
            self.cols = 2

            
class DiffGraphLayout(BoxLayout):
    name  = ObjectProperty(None) # kv
    graph = ObjectProperty(None) # kv

    bplot = ObjectProperty(None)
    aplot = ObjectProperty(None)

    def build(self, name, color, before, after):
        self.name.text = name

        self.bplot        = SmoothLinePlot(color=COLOR_GRAY)
        self.bplot.points = build_points(*before)
        self.graph.add_plot(self.bplot)

        self.aplot        = SmoothLinePlot(color=color)
        self.aplot.points = build_points(*after)
        self.graph.add_plot(self.aplot)
