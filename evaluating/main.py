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
        mainacc.add_widget(self.build_result())
        #mainacc.select(mainacc.children[-1])

    def build_prepare(self):
        prepare = Builder.load_file('prepare.kv')
        prepare.build_graphlayout()
        prepare.associate(self.pdata)
        return prepare

    def build_result(self):
        result = Builder.load_file('result.kv')
        result.build_inneracc()
        result.associate(self.pdata)
        return result

    def build_data(self):
        players = self.pdata.players 
        lteam   = self.pdata.lteam
        cteam   = self.pdata.cteam
        rteam   = self.pdata.rteam
        for name in PLAYERS:
            players[name] = (MEAN, STDDEV)

            if name == 'player1':
                lteam.append(name)
            elif name == 'player2':
                rteam.append(name)
            else:
                cteam.append(name)

if __name__ == '__main__':
    EvaluatingApp().run()
