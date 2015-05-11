from kivy.properties    import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import AccordionItem
from kivy.garden.graph  import Graph, SmoothLinePlot, MeshStemPlot

class PrepareAccItem(AccordionItem):
    llist = ObjectProperty(None)
    clist = ObjectProperty(None)
    rlist = ObjectProperty(None)
    graph = ObjectProperty(None)

class LeftList(BoxLayout):
    clist = ObjectProperty(None)

    def add_player(self, player):
        row = ListItem(player, {'right': self.neutral_list})
        self.add_widget(row)

    def remove_player(self, player):
        pass
    

class CenterList(BoxLayout):
    llist = ObjectProperty(None)
    rlist = ObjectProperty(None)

    def add_player(self, player):
        btn_target = \
            {'left': self.red_list, 'right': self.blue_list}
        row = ListItem(player, btn_target)
        self.add_widget(row)

    def remove_player(self, player):
        pass

class RightList(BoxLayout):
    clist = ObjectProperty(None)

    def add_player(self, player):
        row = ListItem(player, {'left': self.neutral_list})
        self.add_widget(row)

    def remove_player(self, player):
        pass

class CompGraphLayout(BoxLayout):
    pass
