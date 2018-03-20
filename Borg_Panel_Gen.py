
from solid.utils import *
import Borg_Panel_Gen_fcns as Brg
import random as rnd
import numpy as np

use("BorgStructs.scad")


class Panel:

    # Initializer/Instance attributes
    def __init__(self, physical_size, fill_pct, probs=None):

        if probs is None:
            probs = [.05, .8, .15]

        self.phys_size = physical_size
        self.fill_pct = fill_pct
        self.probability = probs
        self.rooms = []
        self.scad = []

        # Generate the rooms and the OpenSCAD code for the given panel
        self.generate_panel()
        self.render_panel()

    # Generate geometric structures to fill the panel
    def generate_panel(self):

        # Set the generic coordinates the 'rooms' will try to spawn
        x_rand, y_rand = Brg.quasirandom(self.fill_pct)

        # Scale the coordinates to the actual physical size
        x_coords = (x_rand/x_rand.max())*self.phys_size[0]
        y_coords = (y_rand/y_rand.max())*self.phys_size[1]

        # Round off the decimal places
        x_coords = x_coords.round(2)
        y_coords = y_coords.round(2)

        # Define the limits of the structure placement
        xmax = self.phys_size[0]
        ymax = self.phys_size[1]

        # Begin generating 'rooms'
        for idx, v in enumerate(x_coords):

            # Size the rooms
            # Aspect ratio of the overall panel
            panel_aspect = self.phys_size[0]/self.phys_size[1]
            if panel_aspect < .5:  # Tall, thin panels
                aspect_ratio = round(rnd.uniform(1, .25/panel_aspect), 2)
                x_size = round(rnd.uniform(1, .5 * xmax), 2)
                y_size = x_size * aspect_ratio
                rot_lim = 0
            elif panel_aspect > 3:  # wide, short panels
                aspect_ratio = round(rnd.uniform(1, .25 * panel_aspect), 2)
                y_size = round(rnd.uniform(1, .5 * ymax), 2)
                x_size = y_size * aspect_ratio
                rot_lim = 0
            else:
                aspect_ratio = round(rnd.uniform(0, 2.5), 2)
                y_size = round(rnd.uniform(1, .125 * ymax), 2)
                x_size = y_size * aspect_ratio
                rot_lim = 90

            # Selection of Z heights; shortens print time by minimizing "too close" height differences
            z_size = self.phys_size[2]
            sel_struct = np.random.choice([1, 2, 3], p=self.probability)

            if sel_struct == 1:
                self.rooms.append(Diamond([v, y_coords[idx], 0], rnd.choice([0, rot_lim]), [x_size, y_size, z_size],
                                          self.phys_size))
            elif sel_struct == 2:
                self.rooms.append(Siding([v, y_coords[idx], 0], rnd.choice([0, rot_lim]), [x_size, y_size, z_size],
                                         self.phys_size))
            else:
                self.rooms.append(Stairway([v, y_coords[idx], 0], rnd.choice([0, rot_lim]), [x_size, y_size, z_size],
                                           self.phys_size))

    # Render panel in defined openSCAD file

    def render_panel(self):
        for rm in self.rooms:
            self.scad.append(translate(rm.position)(rotate(rm.rotation)(rm.scad)))


# Define the Room parent class for the structures
class Room:

    def __init__(self, position, rotation, size, panel_lims):
        self.position = position
        self.rotation = rotation
        self.size = size
        self.panel_lims = panel_lims
        self.extent = []

    def bound_checking(self):
        # Coordinates within the panel space
        x_panel = round(self.extent[0]+self.position[0], 2)
        y_panel = round(self.extent[1]+self.position[1], 2)

        # Ensure the far corner is within the building area
        # X Position
        if x_panel < 0:
            self.position[0] = self.position[0] - (x_panel-0)
        elif x_panel > self.panel_lims[0]:
            self.position[0] = self.position[0] - (x_panel-self.panel_lims[0])

        # Y Position
        if y_panel < 0:
            self.position[1] = max(self.position[1] - (y_panel - 0), 0)
        elif y_panel > self.panel_lims[1]:
            self.position[1] = min(self.position[1] - (y_panel - self.panel_lims[1]), self.panel_lims[1])

        # Ensure the given starting corner is within the build area
        # X Position
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > self.panel_lims[0]:
            self.position[0] = self.panel_lims[0]

        # Y Position
        if self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] > self.panel_lims[1]:
            self.position[1] = self.panel_lims[1]


# Child class structures
class Diamond(Room):
    def __init__(self, position, rotation, size, panel_size):
        super().__init__(position, rotation, size, panel_size)
        self.scad = struct_1(self.size[0], self.size[1], self.size[2])

        # Sloppy coding; only works for rotation options of 0 or 90 degrees
        if self.rotation > 10:
            self.extent = [-1.85*self.size[1], 1.85*self.size[0]]
        else:
            self.extent = [1.85*self.size[0], 1.85*self.size[1]]

        super().bound_checking()


class Siding(Room):
    def __init__(self, position, rotation, size, panel_size):
        super().__init__(position, rotation, size, panel_size)
        self.scad = struct_2(self.size[0], self.size[1], self.size[2])

        if self.rotation > 10:
            self.extent = [-max(2*self.size[1], self.size[0]), max(2.33*self.size[0], self.size[1])]
        else:
            self.extent = [max(2.33*self.size[0], self.size[1]), max(2*self.size[1], self.size[0])]

        super().bound_checking()


class Stairway(Room):
    def __init__(self, position, rotation, size, panel_size):
        super().__init__(position, rotation, size, panel_size)
        self.scad = struct_3(self.size[0], self.size[1], self.size[2])

        if self.rotation > 10:
            self.extent = [-3*self.size[1], 2*self.size[1]+self.size[0]]
        else:
            self.extent = [2*self.size[1]+self.size[0], 3*self.size[1]]

        super().bound_checking()


# Print size in mm
length = 100.
width = 100.
thk = 2.

# List of the layers to be combined. Generally, 1 is sufficient
# layers = [Panel((length-4*thk, width-4*thk), 50, (1., thk)), Panel((length, thk), 10, (1., thk))]
layers = [Panel((length-4*thk, width-4*thk, thk), 50), Panel((length, 2*thk, .5), 10, probs=[0, 1, 0]),
          Panel((2*thk, width, .5), 10, probs=[0, 1, 0]), Panel((length, 2*thk, .5), 10, probs=[0, 1, 0]),
          Panel((2*thk, width, .5), 10, probs=[0, 1, 0])]
# Define the edge structure to give a starting SCAD object
full_panel = edges(length,  width, thk)

# Combine all of the layers.
full_panel = full_panel+translate([2*thk, 2*thk, 0])(layers[0].scad) + \
             translate([0, 0, thk])(layers[1].scad) + \
             translate([0, 0, thk])(layers[2].scad) + \
             translate([length, width, thk])(rotate([0, 0, 180])(layers[3].scad)) + \
             translate([length, width, thk])(rotate([0, 0, 180])(layers[4].scad))

# Render to openSCAD file
scad_render_to_file(full_panel, 'BorgPanel.scad')
