"""
This module implements a plugin that supports the tyssue apoptosis demo.

This module was derived from https://github.com/DamCB/tyssue-demo, a MPLv2
licensed project.
"""
import logging
import sys
import pooch

import napari

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
        # Read pre-recorded datasets

        h5store = pooch.retrieve(
            url="https://github.com/DamCB/tyssue-demo/raw/master/data/small_ellipsoid.hf5",
            known_hash=None,
            progressbar=True,
        )

        datasets = load_datasets(h5store, data_names=["face", "vert", "edge", "cell"])

        specs = config.geometry.bulk_spec()
        monolayer = Monolayer('ell', datasets, specs)
        monolayer_geom.update_all(monolayer)        

        specs = {
            "edge": {
                "line_tension": 0.0,
            },
            "face": {
                "contractility": 0.01,
            },
            "cell": {
                "prefered_vol": monolayer.cell_df['vol'].median(),
                "vol_elasticity": 0.1,
                "prefered_area": monolayer.cell_df['area'].median(),
                "area_elasticity": 0.1,
            },
            "settings": {
                'lumen_prefered_vol': monolayer.settings['lumen_vol'],
                'lumen_vol_elasticity': 1e-2                
            }
        }
        monolayer.update_specs(specs, reset=True)

        solver = QSSolver()
        
        res = solver.find_energy_min(monolayer, monolayer_geom, ClosedMonolayerModel)

        # Division
        mother = 8
        daughter = cell_division(monolayer, mother, 
                                 orientation='vertical')
        monolayer.validate()

        # Another division
        mother = 18
        daughter = cell_division(monolayer, mother, 
                                 orientation='horizontal')
        monolayer.validate()

        # Energy minimization after division
        monolayer.cell_df.loc[[mother, daughter], 'prefered_area'] /= 2
        monolayer.cell_df.loc[[mother, daughter], 'prefered_vol'] /= 3
        monolayer.settings['lumen_prefered_vol'] = monolayer.settings['lumen_vol']
        monolayer.settings['lumen_vol_elasticity'] = 1e-2

        res = solver.find_energy_min(monolayer, monolayer_geom, ClosedMonolayerModel)
        LOGGER.info(res['message'])

        self.monolayer = monolayer


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

        sheet = self.history.retrieve(self.t)
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
    viewer = napari.Viewer()

    LOGGER.setLevel(logging.DEBUG)
    widget = CellDivision3D(viewer)

    widget.start_simulation()

