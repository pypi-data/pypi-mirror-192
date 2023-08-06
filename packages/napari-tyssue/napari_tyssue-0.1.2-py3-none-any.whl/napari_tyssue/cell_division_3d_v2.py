"""
This module implements a plugin that supports the tyssue apoptosis demo.

This module was derived from https://github.com/DamCB/tyssue-demo, a MPLv2
licensed project.
"""
import logging
import sys
import pooch

import napari

import numpy as np
# import vispy as vp

import tyssue
from tyssue import Sheet, History
from tyssue import config

from tyssue import SheetGeometry as geom
from tyssue.dynamics.sheet_vertex_model import SheetModel as basemodel
from tyssue.dynamics.apoptosis_model import SheetApoptosisModel as model
from tyssue.solvers.quasistatic import QSSolver

from tyssue.config.draw import sheet_spec
from tyssue.utils.utils import spec_updater

from tyssue.topology.monolayer_topology import cell_division

from tyssue.core.monolayer import Monolayer
from tyssue.geometry.bulk_geometry import ClosedMonolayerGeometry as monolayer_geom
from tyssue.dynamics.bulk_model import ClosedMonolayerModel
# from tyssue.draw import highlight_cells

from tyssue.generation import three_faces_sheet, extrude
from tyssue.geometry.bulk_geometry import MonoLayerGeometry

# from tyssue.draw.ipv_draw import _get_meshes
# from tyssue.draw.vispy_draw import sheet_view, face_visual, edge_visual

# from tyssue.draw import sheet_view, create_gif, browse_history
from tyssue.io.hdf5 import save_datasets, load_datasets

# napari imports

from qtpy.QtWidgets import QVBoxLayout, QPushButton, QWidget

import napari
from napari.utils import progress

from threading import Thread

from superqt.utils import ensure_main_thread

LOGGER = logging.getLogger("napari_tyssue.ApoptosisWidget")

streamHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
streamHandler.setFormatter(formatter)
LOGGER.addHandler(streamHandler)

from napari_tyssue.tyssuewidget import TyssueWidget, _get_meshes


# This widget wraps the apoptosis demo from tyssue.
# https://github.com/DamCB/tyssue-demo/blob/master/B-Apoptosis.ipynb
class CellDivision3D(TyssueWidget):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__(viewer)

        # tyssue model init

        # The history stores simulation outputs
        self.history = None

        # Current timestep
        self.t = 0

        # This is the stop time of the simulation
        self.stop = 100

        # Add model parameters for config

        # Setup the UI
        self._init_buttons()

        # Add a new callback for the timeslider

    def start_simulation(self):

        datasets_2d, _ = three_faces_sheet(zaxis=True)
        datasets = extrude(datasets_2d, method='translation')
        eptm = Monolayer('test_volume', datasets, 
                         config.geometry.bulk_spec(),
                         coords=['x','y','z'])

        ## We need to add noise to our position to avoid
        ## Ill defined angles in this artificial case

        eptm.vert_df[eptm.coords] += np.random.normal(
            scale=1e-6,
            size=eptm.vert_df[eptm.coords].shape)
        MonoLayerGeometry.update_all(eptm)

        for orientation in ['vertical', 'horizontal']:
            print(orientation)
            daughter = cell_division(eptm, 1, orientation=orientation)
            eptm.reset_topo()
            eptm.reset_index()
            MonoLayerGeometry.update_all(eptm)
            print(f'Valid division for {orientation}:', end="\t")
            print(eptm.validate()) 


        self.eptm = eptm
        
        # Trigger a render
        self._on_simulation_update()

    @ensure_main_thread
    def _on_simulation_update(self):
        """
        This function is called after every simulated timestep.
        """
        LOGGER.debug("CellDivision3D._on_simulation_update: timestep")

        specs_kw = {}
        draw_specs = sheet_spec()
        spec_updater(draw_specs, specs_kw)
        coords = ["x", "y", "z"]

        sheet = self.eptm
        meshes = _get_meshes(sheet, coords, draw_specs)
        mesh = meshes[0]
        LOGGER.info(mesh)
        LOGGER.info(
            f"mesh: ({mesh[0].shape}, {mesh[1].shape}, {mesh[2].shape})"
        )

        try:
            # if the layer exists, update the data
            self.viewer.layers["tyssue: cell_division_3d"].data = mesh
        except KeyError:
            # otherwise add it to the viewer
            self.viewer.add_surface(
                mesh,
                colormap="turbo",
                opacity=0.9,
                contrast_limits=[0, 1],
                name="tyssue: cell_division_3d",
            )


if __name__ == "__main__"  or True:
    viewer = napari.Viewer(ndisplay=3)

    LOGGER.setLevel(logging.DEBUG)
    widget = CellDivision3D(viewer)

    widget.start_simulation()

