# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.

from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi import mlab
from PyQt5 import QtWidgets, QtCore
import numpy as np
import time
import os
from reshaper import Reshaper
import utils

os.environ['ETS_TOOLKIT'] = 'qt4'


class MayaviQWidget():
    def __init__(self):

        # models for shape representing
        self.bodies = {"male": Reshaper(label="male")}
        self.body = self.bodies["male"]
        self.flag_ = 0

        self.vertices = self.body.mean_vertex
        self.normals = self.body.normals
        self.facets = self.body.facets
        self.input_data = np.zeros((utils.M_NUM, 1))
        self.update()

    def update(self):
        [self.vertices, self.normals, self.facets] = \
            self.body.mapping(self.input_data, self.flag_)
        self.vertices = self.vertices.astype('float32')
        # self.visualization.update_plot(self.vertices, self.facets)

    def select_mode(self, label="male", flag=0):
        self.body = self.bodies[label]
        self.flag_ = flag
        self.update()

    def sliderForwardedValueChangeHandler(self, sliderID, val, minVal, maxVal):
        x = val / 10.0
        print(f'scale is {x}')
        self.input_data[sliderID] = x
        start = time.time()
        self.update()
        print(' [**] update body in %f s' % (time.time() - start))

    def save(self):
        utils.save_obj("result.obj", self.vertices, self.facets + 1)
        output = np.array(utils.calc_measure(self.body.cp, self.vertices, self.facets))
        for i in range(0, utils.M_NUM):
            print("%s: %f" % (utils.M_STR[i], output[i, 0]))

def get_data(measure, scale):
    measure_data = {'weight': 0}
    maya = MayaviQWidget()
    maya.select_mode()
    maya.sliderForwardedValueChangeHandler(measure_data.get(measure), scale, 0, 18)
    #maya.sliderForwardedValueChangeHandler(0, 0, 0, 18)
    maya.save()
