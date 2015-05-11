# kivy
from kivy.properties     import ObjectProperty
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion  import Accordion, AccordionItem
from kivy.garden.graph   import Graph, MeshLinePlot, MeshStemPlot

#stdlib
from math      import sqrt
from functools import partial

# trueskill
from trueskill import TrueSkill

# project
from settings  import *
from graphcalc import build_points


_tscalc = TrueSkill( \
                    mu = MEAN, sigma = STDDEV, \
                    beta = STDDEV/2., tau = STDDEV/100.)


class ResultAccItem(AccordionItem):
    inneracc = ObjectProperty(None) # kv

    def build_inneracc(self):
        self.inneracc.build()

    def associate(self, pdata):
        self.inneracc.associate(pdata)

    def on_collapse(self, instance, value):
        super(ResultAccItem, self).on_collapse(instance, value)
        if not value:
            self.inneracc.refresh()


class InnerAccordion(Accordion):
    litem = ObjectProperty(None) # kv
    ditem = ObjectProperty(None) # kv
    ritem = ObjectProperty(None) # kv

    def build(self):
        self.litem.calc_func = partial(_tscalc.rate, ranks = [0, 1])
        self.ditem.calc_func = partial(_tscalc.rate, ranks = [0, 0])
        self.ritem.calc_func = partial(_tscalc.rate, ranks = [1, 0])
        self.select(self.children[-1])

    def associate(self, pdata):
        self.litem.associate(pdata)
        self.ditem.associate(pdata)
        self.ritem.associate(pdata)

    def refresh(self):
        for accitem in self.children:
            if not accitem.collapse:
                accitem.rebuild()


class InnerAccItem(AccordionItem):
    graphslayout = ObjectProperty(None) # kv
    applybtn     = ObjectProperty(None) # kv
    pdata        = ObjectProperty(None)

    def associate(self, pdata):
        self.pdata = pdata

    def on_collapse(self, instance, value):
        super(InnerAccItem, self).on_collapse(instance, value)
        if value: return
        self.rebuild()

    def rebuild(self):
        self._build_data()
        self.graphslayout.rebuild(self._to_graphs_data())

    def _build_data(self):
        pass

    def _to_graphs_data(self):
        pass

class GraphsLayout(GridLayout):
    def rebuild(self, graphs_data):
        self.clear_widgets()
            

class DiffGraphLayout(BoxLayout):
    name  = ObjectProperty(None) # kv
    graph = ObjectProperty(None) # kv

    bplot = ObjectProperty(None)
    aplot = ObjectProperty(None)

    def build(self, name, color, before, after):
        self.name.text = name

        darken     = color[:]
        darken[-1] = darken[-1]/2.0

        self.bplot        = MeshStemPlot(color=darken)
        self.bplot.points = build_points(*before)
        self.graph.add_plot(self.bplot)

        self.aplot        = MeshStemPlot(color=color)
        self.aplot.points = build_points(*after)
        self.graph.add_plot(self.aplot)
