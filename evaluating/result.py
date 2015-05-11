# kivy
from kivy.properties    import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import AccordionItem
from kivy.garden.graph  import Graph, MeshLinePlot, MeshStemPlot

#stdlib
from math      import sqrt
from functools import partial

# project
from settings  import *
from graphcalc import build_points

class ResultAccItem(AccordionItem):
    pass
