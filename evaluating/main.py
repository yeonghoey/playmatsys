# kivy dependencies
from kivy.config import Config
Config.read('config.ini')

from kivy.app           import App
from kivy.lang          import Builder
from kivy.properties    import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

# project dependencies
from settings   import *
from playerdata import PlayerData
from prepare    import PrepareScene
from result     import ResultScene


class TopLayout(BoxLayout):
    scene = ObjectProperty(None)

    # top layer(scene transitioning) buttons' event handlers
    def show_prepare(self):
        self._swich_scene(self.scene.prepare)

    def show_lwin(self):
        self._swich_scene(self.scene.lwin)

    def show_draw(self):
        self._swich_scene(self.scene.draw)

    def show_rwin(self):
        self._swich_scene(self.scene.rwin)

    def _swich_scene(self, scene):
        self.scene.clear_widgets()
        scene.refresh()
        self.scene.add_widget(scene)


class Scene(BoxLayout):
    prepare = ObjectProperty(None)
    lwin    = ObjectProperty(None)
    draw    = ObjectProperty(None)
    rwin    = ObjectProperty(None)


class EvaluatingApp(App):
    pdata = ObjectProperty(PlayerData())

    def build(self):
        '''kivy's app init point'''
        self.build_root()
        self.build_data()
        self.show_prepare()

    def build_root(self):
        self.build_scene(self.root.scene)

    def build_scene(self, scene):
        Builder.load_file('prepare.kv')
        Builder.load_file('result.kv')

        scene.prepare = self.build_prepare()
        scene.lwin    = self.build_result(self.pdata.lwin)
        scene.draw    = self.build_result(self.pdata.draw)
        scene.rwin    = self.build_result(self.pdata.rwin)

    def build_prepare(self):
        prepare = PrepareScene() 
        prepare.build()
        prepare.associate(self.pdata)
        return prepare

    def build_result(self, ratefunc):
        result = ResultScene()
        result.build()
        result.associate(self.pdata, ratefunc)
        return result

    def build_data(self):
        players = self.pdata.players 
        cteam   = self.pdata.cteam
        for name in PLAYERS:
            players[name] = (MEAN, STDDEV)
            cteam.append(name)

    def show_prepare(self):
        self.root.show_prepare()


if __name__ == '__main__':
    EvaluatingApp().run()
