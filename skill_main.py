from kivy.app import App
from kivy.uix.widget import Widget
from kivy.garden.graph import Graph, MeshLinePlot, MeshStemPlot, SmoothLinePlot
from math import sin
import scipy.stats


class MatSysSkillApp(App):
    def build(self):
        gp = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                x_ticks_major=10, y_ticks_major=0.1,
                y_grid_label=True, x_grid_label=True, padding=5,
                x_grid=True, y_grid=True, xmin=0, xmax=100, ymin=0, ymax=.5)
        points = [(x, scipy.stats.norm(50, 16.3).pdf(x)) for x in range(0, 100)]
        points_maxy = max(map(lambda (x,y): y, points))
        #gp.ymax = points_maxy+;
        gp.ymax = 0.1
        #plot = MeshLinePlot(color=[1, 0, 0, 1])
        #plot = MeshStemPlot(color=[0, 1, 0, 1])
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plotsub = MeshStemPlot(color=[0, 1, 0, 1])
        plot.points = points
        plotsub.points = points[:50]
        gp.add_plot(plot)
        gp.add_plot(plotsub)
        return gp

if __name__ == '__main__':
    MatSysSkillApp().run()
