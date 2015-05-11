# kivy
from kivy.properties     import ObjectProperty
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion  import Accordion, AccordionItem
from kivy.garden.graph   import Graph, MeshLinePlot, MeshStemPlot

#stdlib
from math      import sqrt
from functools import partial


# project
from settings  import *
from graphcalc import build_points


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
        self.select(self.children[-1])

    def associate(self, pdata):
        self.litem.associate(pdata, pdata.lwin)
        self.ditem.associate(pdata, pdata.draw)
        self.ritem.associate(pdata, pdata.rwin)

    def refresh(self):
        for accitem in self.children:
            if not accitem.collapse:
                accitem.rebuild_graph()


class InnerAccItem(AccordionItem):
    graphslayout = ObjectProperty(None) # kv
    applybtn     = ObjectProperty(None) # kv

    pdata    = ObjectProperty(None)
    ratefunc = ObjectProperty(None)

    def associate(self, pdata, ratefunc):
        self.pdata    = pdata
        self.ratefunc = ratefunc

    def on_collapse(self, instance, value):
        super(InnerAccItem, self).on_collapse(instance, value)
        if value: return
        self.rebuild_graph()

    def rebuild_graph(self):
        afterplayers = self._build_after()
        players      = sorted(afterplayers.iteritems())

        graphbuild_info = []
        for name, after in players:
            info = {'name': name, 'after': after} 
            if   name in self.pdata.lteam: info['color'] = COLOR_LEFT
            elif name in self.pdata.rteam: info['color'] = COLOR_RIGHT
            else: continue # unexpected
            info['before'] = self.pdata.rating(name)
            graphbuild_info.append(info)

        self.graphslayout.rebuild(graphbuild_info)

    def _build_after(self):
        if not self.pdata:    return {}
        if not self.ratefunc: return {}
        return self.ratefunc()


class GraphsLayout(GridLayout):
    def rebuild(self, graphbuild_info):
        self.clear_widgets()
        for info in graphbuild_info:
            graph = DiffGraphLayout()
            graph.build(**info)
            self.add_widget(graph)
            

class DiffGraphLayout(BoxLayout):
    name  = ObjectProperty(None) # kv
    graph = ObjectProperty(None) # kv

    bplot = ObjectProperty(None)
    aplot = ObjectProperty(None)

    def build(self, name, color, before, after):
        self.name.text = name
        darken     = color[:]
        darken[-1] = darken[-1]/4.0
        self.bplot        = MeshStemPlot(color=darken)
        self.bplot.points = build_points(*before)
        self.graph.add_plot(self.bplot)

        self.aplot        = MeshStemPlot(color=color)
        self.aplot.points = build_points(*after)
        self.graph.add_plot(self.aplot)
