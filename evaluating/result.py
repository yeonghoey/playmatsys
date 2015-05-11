# kivy
from kivy.properties    import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.garden.graph  import Graph, MeshLinePlot, MeshStemPlot

#stdlib
from math      import sqrt
from functools import partial

# project
from settings  import *
from graphcalc import build_points

class ResultAccItem(AccordionItem):
    inneracc = ObjectProperty(None) # kv

class InnerAccordion(Accordion):
    pass

class InnerAccItem(AccordionItem):
    graphs   = ObjectProperty(None) # kv
    applybtn = ObjectProperty(None) # kv

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
