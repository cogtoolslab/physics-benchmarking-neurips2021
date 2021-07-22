import sys, os, copy
from typing import List, Dict, Tuple, Optional
from pathlib import Path

import random
import numpy as np
import h5py

from tdw.librarian import ModelRecord, MaterialLibrarian, ModelLibrarian
from tdw.tdw_utils import TDWUtils
from tdw_physics.target_controllers.dominoes import Dominoes, get_args, ArgumentParser
from tdw_physics.flex_dataset import FlexDataset, FlexParticles
from tdw_physics.rigidbodies_dataset import RigidbodiesDataset
from tdw_physics.util import MODEL_LIBRARIES, get_parser, none_or_str

from tdw_physics.postprocessing.labels import get_all_label_funcs

# fluid
from tdw.flex.fluid_types import FluidTypes

MODEL_NAMES = [r.name for r in MODEL_LIBRARIES['models_flex.json'].records]
MODEL_CORE = [r.name for r in MODEL_LIBRARIES['models_core.json'].records]

def get_flex_args(dataset_dir: str, parse=True):

    common = get_parser(dataset_dir, get_help=False)
    domino, domino_postproc = get_args(dataset_dir, parse=False)
    parser = ArgumentParser(parents=[common, domino], conflict_handler='resolve', fromfile_prefix_chars='@')

    parser.add_argument("--all_flex_objects",
                        type=int,
                        default=1,
                        help="Whether all rigid objects should be FLEX")
    parser.add_argument("--step_physics",
                        type=int,
                        default=100,
                        help="How many physics steps to run forward after adding a solid FLEX object")
    parser.add_argument("--cloth",
                        action="store_true",
                        help="Demo: whether to drop a cloth")
    parser.add_argument("--squishy",
                        action="store_true",
                        help="Demo: whether to drop a squishy ball")
    parser.add_argument("--fluid",
                        action="store_true",
                        help="Demo: whether to drop fluid")
    parser.add_argument("--fwait",
                        type=none_or_str,
                        default="30",
                        help="How many frames to wait before applying the force")
    parser.add_argument("--collision_label_threshold",
                        type=float,
                        default=0.1,
                        help="Euclidean distance at which target and zone are said to be touching")
    parser.add_argument("--min_distance_ratio",
                        type=float,
                        default=0.5,
                        help="minimum ratio of distance between the anchor and target zone")
    parser.add_argument("--max_distance_ratio",
                        type=float,
                        default=0.5,
                        help="maximum ratio of distance between the anchor and target zone")
    parser.add_argument("--min_anchorloc",
                        type=float,
                        default=-0.4,
                        help="minimum of the two anchor x-locations")
    parser.add_argument("--max_anchorloc",
                        type=float,
                        default=0.4,
                        help="maximum of the two anchor x-locations")
    parser.add_argument("--anchor_height",
                        type=float,
                        default=0.5,
                        help="anchor height")
    parser.add_argument("--anchor_jitter",
                        type=float,
                        default=0.0,
                        help="jitter in anchor locations")
    parser.add_argument("--height_jitter",
                        type=float,
                        default=0.0,
                        help="jitter in anchor heights")

    def postprocess(args):

        args = domino_postproc(args)
        args.all_flex_objects = bool(int(args.all_flex_objects))

        return args

    if not parse:
        return (parser, postproccess)

    args = parser.parse_args()
    args = postprocess(args)

    return args


class ClothSagging(Dominoes, FlexDataset):

    FLEX_RECORDS = ModelLibrarian(os.path.join(os.path.dirname(__file__), 'flex.json')).records
    CLOTH_RECORD = MODEL_LIBRARIES["models_special.json"].get_record("cloth_square")
    SOFT_RECORD = MODEL_LIBRARIES["models_flex.json"].get_record("sphere")
    RECEPTACLE_RECORD = MODEL_LIBRARIES["models_special.json"].get_record("fluid_receptacle1x1")
    FLUID_TYPES = FluidTypes()

    def __init__(self, port: int = 1071,
                 all_flex_objects=True,
                 use_cloth=False,
                 use_squishy=False,
                 use_fluid=False,
                 step_physics=False,
                 tether_stiffness_range = [0.0, 1.0],
                 bend_stiffness_range = [0.0, 1.0],#[0.0, 1.0],
                 stretch_stiffness_range = [0.0, 1.0],
                 min_distance_ratio = 0.5,
                 max_distance_ratio = 0.5,
                 min_anchorloc = -0.4,
                 max_anchorloc = 0.4,
                 anchor_height = 0.5,
                 anchor_jitter = 0.2,#0.2,
                 height_jitter = 0.2,#0.3,
                 collision_label_threshold=0.1,
                 **kwargs):

        Dominoes.__init__(self, port=port, **kwargs)
        self._clear_flex_data()

        self.all_flex_objects = all_flex_objects
        self._set_add_physics_object()

        self.step_physics = step_physics
        self.use_cloth = use_cloth
        self.use_squishy = use_squishy
        self.use_fluid = use_fluid

        if self.use_fluid:
            self.ft_selection = random.choice(self.FLUID_TYPES.fluid_type_names)

        self.tether_stiffness_range = tether_stiffness_range
        self.bend_stiffness_range = bend_stiffness_range
        self.stretch_stiffness_range = stretch_stiffness_range
        self.min_distance_ratio = min_distance_ratio
        self.max_distance_ratio = max_distance_ratio
        self.min_anchorloc = min_anchorloc
        self.max_anchorloc = max_anchorloc
        self.anchor_height = anchor_height
        self.anchor_jitter = anchor_jitter
        self.height_jitter = height_jitter

        # for detecting collisions
        self.collision_label_thresh = collision_label_threshold

    def _set_add_physics_object(self):
        if self.all_flex_objects:
            self.add_physics_object = self.add_flex_solid_object
            self.add_primitive = self.add_flex_solid_object
        else:
            self.add_physics_object = self.add_rigid_physics_object


    def get_scene_initialization_commands(self) -> List[dict]:

        commands = Dominoes.get_scene_initialization_commands(self)
        commands[0].update({'convexify': True})
        create_container = {
            "$type": "create_flex_container",
            # "collision_distance": 0.001,
            "collision_distance": 0.025,
            "static_friction": 1.0,
            "dynamic_friction": 1.0,
            "radius": 0.1875,
            'max_particles': 50000}
            # 'max_particles': 200000}

        if self.use_fluid:
            create_container.update({
                'viscosity': self.FLUID_TYPES.fluid_types[self.ft_selection].viscosity,
                'adhesion': self.FLUID_TYPES.fluid_types[self.ft_selection].adhesion,
                'cohesion': self.FLUID_TYPES.fluid_types[self.ft_selection].cohesion,
                'fluid_rest': 0.05,
                'damping': 0.01,
                'subsetp_count': 5,
                'iteration_count': 8,
                'buoyancy': 1.0})

        commands.append(create_container)

        if self.use_fluid:
            commands.append({"$type": "set_time_step", "time_step": 0.005})

        return commands

    def get_trial_initialization_commands(self) -> List[dict]:

        # clear the flex data
        FlexDataset.get_trial_initialization_commands(self)
        return Dominoes.get_trial_initialization_commands(self)

    def _get_send_data_commands(self) -> List[dict]:
        commands = Dominoes._get_send_data_commands(self)
        commands.extend(FlexDataset._get_send_data_commands(self))
        return commands

    def add_rigid_physics_object(self, *args, **kwargs):
        """
        Make sure controller knows to treat probe, zone, target, etc. as non-flex objects
        """

        o_id = kwargs.get('o_id', None)
        if o_id is None:
            o_id: int = self.get_unique_id()
            kwargs['o_id'] = o_id

        commands = Dominoes.add_physics_object(self, *args, **kwargs)
        self.non_flex_objects.append(o_id)

        print("Add rigid physics object", o_id)

        return commands

    def add_flex_solid_object(self,
                              record: ModelRecord,
                              position: Dict[str, float],
                              rotation: Dict[str, float],
                              mesh_expansion: float = 0,
                              particle_spacing: float = 0.035,
                              mass: float = 1,
                              scale: Optional[Dict[str, float]] = {"x": 0.1, "y": 0.5, "z": 0.25},
                              material: Optional[str] = None,
                              color: Optional[list] = None,
                              exclude_color: Optional[list] = None,
                              o_id: Optional[int] = None,
                              add_data: Optional[bool] = True,
                              **kwargs) -> List[dict]:

        # so objects don't get stuck in each other -- an unfortunate feature of FLEX
        position = {'x': position['x'], 'y': position['y'] + 0.1, 'z': position['z']}

        commands = FlexDataset.add_solid_object(
            self,
            record = record,
            position = position,
            rotation = rotation,
            scale = scale,
            mesh_expansion = mesh_expansion,
            particle_spacing = particle_spacing,
            mass_scale = 1,
            o_id = o_id)

        # set mass
        commands.append({"$type": "set_flex_object_mass",
                         "mass": mass,
                         "id": o_id})

        # set material and color
        commands.extend(
            self.get_object_material_commands(
                record, o_id, self.get_material_name(material)))

        color = color if color is not None else self.random_color(exclude=exclude_color)
        commands.append(
            {"$type": "set_color",
             "color": {"r": color[0], "g": color[1], "b": color[2], "a": 1.},
             "id": o_id})

        # step physics
        if bool(self.step_physics):
            print("stepping physics forward", self.step_physics)
            commands.append({"$type": "step_physics",
                             "frames": self.step_physics})

        # add data
        print("Add FLEX physics object", o_id)
        if add_data:
            self._add_name_scale_color(record, {'color': color, 'scale': scale, 'id': o_id})
            self.masses = np.append(self.masses, mass)

        return commands

    def _get_push_cmd(self, o_id, position_or_particle=None):
        if not self.all_flex_objects:
            return Dominoes._get_push_cmd(self, o_id, position_or_particle)
        cmd = {"$type": "apply_force_to_flex_object",
               "force": self.push_force,
               "id": o_id,
               "particle": -1}
        print("PUSH CMD FLEX")
        print(cmd)
        return cmd

    def drop_cloth(self) -> List[dict]:

        self.cloth = self.CLOTH_RECORD
        self.cloth_id = self._get_next_object_id()
        self.cloth_position = {"x": random.uniform(-0.2,0.2), "y": random.uniform(1.3,1.5), "z":random.uniform(-0.6,-0.4)}
        self.cloth_color = self.target_color if self.target_color is not None else self.random_color()
        self.cloth_scale = {'x': 1.0, 'y': 1.0, 'z': 1.0}
        self.cloth_mass = 0.5
        self.cloth_data = {"name": self.cloth.name, "color": self.cloth_color, "scale": self.cloth_scale, "id": self.cloth_id}

        commands = self.add_cloth_object(
            record = self.cloth,
            position = self.cloth_position,
            rotation = {k:0 for k in ['x','y','z']},
            scale=self.cloth_scale,
            mass_scale = 1,
            mesh_tesselation = 1,
            tether_stiffness = random.uniform(self.tether_stiffness_range[0], self.tether_stiffness_range[1]), # doesn't do much visually!
            bend_stiffness = random.uniform(self.bend_stiffness_range[0], self.bend_stiffness_range[1]), #changing this will lead to visible changes in cloth deformability
            stretch_stiffness = random.uniform(self.stretch_stiffness_range[0], self.stretch_stiffness_range[1]), # doesn't do much visually!
            o_id = self.cloth_id)

        # replace the target w the cloth
        self._replace_target_with_object(self.cloth, self.cloth_data)

        # set mass
        commands.append({"$type": "set_flex_object_mass",
                         "mass": self.cloth_mass,
                         "id": self.cloth_id})

        # color cloth
        commands.append(
            {"$type": "set_color",
             "color": {"r": self.cloth_color[0], "g": self.cloth_color[1], "b": self.cloth_color[2], "a": 1.},
             "id": self.cloth_id})

        self._add_name_scale_color(
            self.cloth, {'color': self.cloth_color, 'scale': self.cloth_scale, 'id': self.cloth_id})
        self.masses = np.append(self.masses, self.cloth_mass)

        self._replace_target_with_object(self.cloth, self.cloth_data)

        return commands

    def _place_ramp_under_probe(self) -> List[dict]:

        cmds = Dominoes._place_ramp_under_probe(self)
        self.non_flex_objects.append(self.ramp_id)
        if self.ramp_base_height >= 0.01:
            self.non_flex_objects.append(self.ramp_base_id)
        return cmds

    def _place_and_push_probe_object(self):
        return []

    def _get_zone_location(self, scale):
        dratio = random.uniform(self.min_distance_ratio, self.max_distance_ratio)
        dist = self.max_anchorloc - self.min_anchorloc
        zonedist =  dratio * dist
        return {
            "x": self.max_anchorloc-zonedist,
            "y": 0.0 if not self.remove_zone else 10.0,
            "z": random.uniform(-0.2,0.4) if not self.remove_zone else 10.0
        }

    def is_done(self, resp: List[bytes], frame: int) -> bool:
        return frame >= 150

    def _build_intermediate_structure(self) -> List[dict]:

        commands = []

        # anchor object list
        anchor_list = ["cone","cube","cylinder","pyramid","triangular_prism"]

        # add two objects on each side of a target object
        self.objrec1 = MODEL_LIBRARIES["models_flex.json"].get_record(random.choice(anchor_list))
        self.objrec1_id = self._get_next_object_id()
        self.objrec1_position = {'x': self.min_anchorloc-random.uniform(0.0,self.anchor_jitter), 'y': 0., 'z': 0.}
        self.objrec1_rotation = {k:0 for k in ['x','y','z']}#{'x': 0, 'y': 0, 'z': 0},
        self.objrec1_scale = {'x': random.uniform(0.1,0.3), 'y': self.anchor_height+random.uniform(-self.height_jitter,self.height_jitter), 'z': random.uniform(0.2,0.5)}
        self.objrec1_mass = 25.0
        commands.extend(self.add_flex_solid_object(
                              record = self.objrec1,
                              position = self.objrec1_position,
                              rotation = self.objrec1_rotation,
                              mesh_expansion = 0.0,
                              particle_spacing = 0.035,
                              mass = self.objrec1_mass,
                              scale = self.objrec1_scale,
                              o_id = self.objrec1_id,
                              ))

        self.objrec2 = MODEL_LIBRARIES["models_flex.json"].get_record(random.choice(anchor_list))
        self.objrec2_id = self._get_next_object_id()
        self.objrec2_position = {'x': self.max_anchorloc+random.uniform(0.0,self.anchor_jitter), 'y': 0., 'z': 0.}
        self.objrec2_rotation = {k:0 for k in ['x','y','z']}#{'x': 0, 'y': 0, 'z': 0},
        self.objrec2_scale = {'x': random.uniform(0.1,0.3), 'y': self.anchor_height+0.1+random.uniform(-self.height_jitter,self.height_jitter), 'z': random.uniform(0.2,0.5)}
        self.objrec2_mass = 25.0
        commands.extend(self.add_flex_solid_object(
                               record = self.objrec2,
                               position = self.objrec2_position,
                               rotation = self.objrec2_rotation,
                               mesh_expansion = 0.0,
                               particle_spacing = 0.035,
                               mass = self.objrec2_mass,
                               scale = self.objrec2_scale,
                               o_id = self.objrec2_id,
                               ))

        # drape object
        drape_list = ["alma_floor_lamp","buddah","desk_lamp","linbrazil_diz_armchair"]

        #drape_list = ["linbrazil_diz_armchair"]
        self.drape_object = random.choice(drape_list)
        self.objrec3 = MODEL_LIBRARIES["models_core.json"].get_record(self.drape_object)
        self.objrec3_id = self._get_next_object_id()
        self.objrec3_rotation = {k:0 for k in ['x','y','z']}#{'x': 0, 'y': random.uniform(0,45), 'z': 0},#
        self.objrec3_mass = 100.0

        print("drape object: ",self.drape_object)
        if self.drape_object == "alma_floor_lamp":
            self.objrec3_position = {'x': 0., 'y': 0., 'z': -1.1}
            self.objrec3_scale = {'x': 1.0, 'y': 0.8, 'z': 1.0}
        elif self.drape_object == "linbrazil_diz_armchair":
            self.objrec3_position = {'x': 0., 'y': 0., 'z': -1.4}
            self.objrec3_scale = {'x': 1.2, 'y': 1.2, 'z': 1.0}
        elif self.drape_object == "buddah":
            self.objrec3_position = {'x': 0., 'y': 0., 'z': -1.3}
            self.objrec3_scale = {'x': 1.2, 'y': 1.2, 'z': 1.2}
        elif self.drape_object == "desk_lamp":
            self.objrec3_position = {'x': 0., 'y': 0., 'z': -1.1}
            self.objrec3_scale = {'x': 1.2, 'y': 1.2, 'z': 1.2}


        commands.extend(self.add_flex_solid_object(
                               record = self.objrec3,
                               position = self.objrec3_position,
                               rotation = self.objrec3_rotation,
                               mesh_expansion = 0.0,
                               particle_spacing = 0.035,
                               mass = self.objrec3_mass,
                               scale = self.objrec3_scale,
                               o_id = self.objrec3_id,
                               ))

        # additional anchor
        if random.uniform(0.0,1.0)>0.3:
            self.objrec4 = MODEL_LIBRARIES["models_flex.json"].get_record(random.choice(anchor_list))
            self.objrec4_id = self._get_next_object_id()
            takeloc = random.choice([self.min_anchorloc-0.5,self.max_anchorloc+0.5])
            self.objrec4_position = {'x': takeloc-random.uniform(0.0,self.anchor_jitter), 'y': 0., 'z': 0.}
            self.objrec4_rotation = {k:0 for k in ['x','y','z']}#{'x': 0, 'y': 0, 'z': 0},
            self.objrec4_scale = {'x': random.uniform(0.1,0.3), 'y': 0.5+random.uniform(-self.height_jitter,self.height_jitter), 'z': random.uniform(0.2,0.5)}
            self.objrec4_mass = 25.0
            commands.extend(self.add_flex_solid_object(
                                   record = self.objrec4,
                                   position = self.objrec4_position,
                                   rotation = self.objrec4_rotation,
                                   mesh_expansion = 0.0,
                                   particle_spacing = 0.035,
                                   mass = self.objrec4_mass,
                                   scale = self.objrec4_scale,
                                   o_id = self.objrec4_id,
                                   ))

        commands.extend(self.drop_cloth() if self.use_cloth else [])

        return commands

    @staticmethod
    def get_flex_object_collision(flex, obj1, obj2, collision_thresh=0.15):
        '''
        flex: FlexParticles Data
        '''
        collision = False
        p1 = p2 = None
        for n in range(flex.get_num_objects()):
            if flex.get_id(n) == obj1:
                p1 = flex.get_particles(n)
            elif flex.get_id(n) == obj2:
                p2 = flex.get_particles(n)

        if (p1 is not None) and (p2 is not None):

            p1 = np.array(p1)[:,0:3]
            p2 = np.array(p2)[:,0:3]

            dists = np.sqrt(np.square(p1[:,None] - p2[None,:]).sum(-1))
            collision = (dists < collision_thresh).max()
            min_dist = dists.min()
            print(obj1, p1.shape, obj2, p2.shape, "min_dist", min_dist, "colliding?", collision)

        return (min_dist, collision)

    def _write_frame_labels(self,
                            frame_grp: h5py.Group,
                            resp: List[bytes],
                            frame_num: int,
                            sleeping: bool) -> Tuple[h5py.Group, List[bytes], int, bool]:

        labels, resp, grame_num, done = RigidbodiesDataset._write_frame_labels(self, frame_grp, resp, frame_num, sleeping)

        has_target = (not self.remove_target) or self.replace_target
        has_zone = not self.remove_zone
        labels.create_dataset("has_target", data=has_target)
        labels.create_dataset("has_zone", data=has_zone)
        if not (has_target or has_zone):
            return labels, resp, frame_num, done

        print("frame num", frame_num)
        flex = None
        for r in resp[:-1]:
            if FlexParticles.get_data_type_id(r) == "flex":
                flex = FlexParticles(r)

        if has_target and has_zone and (flex is not None):
            min_dist, are_touching = self.get_flex_object_collision(flex,
                                                          obj1=self.target_id,
                                                          obj2=self.zone_id,
                                                          collision_thresh=self.collision_label_thresh)
            labels.create_dataset("minimum_distance_target_to_zone", data=min_dist)
            labels.create_dataset("target_contacting_zone", data=are_touching)

        return labels, resp, frame_num, done

    @staticmethod
    def get_controller_label_funcs(classname = 'ClothSagging'):

        funcs = super(ClothSagging, ClothSagging).get_controller_label_funcs(classname)
        funcs += get_all_label_funcs()

        def minimum_distance_target_to_zone(f):
            frames = list(f['frames'].keys())
            min_dists = np.stack([
                np.array(f['frames'][fr]['labels']['minimum_distance_target_to_zone'])
                for fr in frames], axis=0)
            return float(min_dists.min())

        funcs += [minimum_distance_target_to_zone]

        return funcs

    def _set_occlusion_attributes(self) -> None:

        self.occluder_angular_spacing = 10
        self.occlusion_distance_fraction = [0.6, 0.8]
        self.occluder_rotation_jitter = 30.
        self.occluder_min_z = self.middle_scale['z'] + 0.25
        self.occluder_min_size = 0.8
        self.occluder_max_size = 1.2
        self.rescale_occluder_height = True

    def _set_distractor_attributes(self) -> None:

        self.distractor_angular_spacing = 15
        self.distractor_distance_fraction = [0.4,1.0]
        self.distractor_rotation_jitter = 30
        self.distractor_min_z = self.middle_scale['z'] + 0.25
        self.distractor_min_size = 0.8
        self.distractor_max_size = 1.2

if __name__ == '__main__':
    import platform, os

    args = get_flex_args("flex_dominoes")

    import platform
    if platform.system() == 'Linux':
        if args.gpu is not None:
            os.environ["DISPLAY"] = ":0." + str(args.gpu)
        else:
            os.environ["DISPLAY"] = ":0"

    C = ClothSagging(
        port=args.port,
        all_flex_objects=args.all_flex_objects,
        use_cloth=args.cloth,
        use_squishy=args.squishy,
        use_fluid=args.fluid,
        step_physics=args.step_physics,
        room=args.room,
        num_middle_objects=args.num_middle_objects,
        randomize=args.random,
        seed=args.seed,
        target_zone=args.zone,
        zone_location=args.zlocation,
        zone_scale_range=args.zscale,
        zone_color=args.zcolor,
        zone_material=args.zmaterial,
        zone_friction=args.zfriction,
        target_objects=args.target,
        probe_objects=args.probe,
        middle_objects=args.middle,
        target_scale_range=args.tscale,
        target_rotation_range=args.trot,
        probe_rotation_range=args.prot,
        probe_scale_range=args.pscale,
        probe_mass_range=args.pmass,
        target_color=args.color,
        probe_color=args.pcolor,
        middle_color=args.mcolor,
        collision_axis_length=args.collision_axis_length,
        force_scale_range=args.fscale,
        force_angle_range=args.frot,
        force_offset=args.foffset,
        force_offset_jitter=args.fjitter,
        force_wait=args.fwait,
        spacing_jitter=args.spacing_jitter,
        lateral_jitter=args.lateral_jitter,
        middle_scale_range=args.mscale,
        middle_rotation_range=args.mrot,
        middle_mass_range=args.mmass,
        horizontal=args.horizontal,
        remove_target=bool(args.remove_target),
        remove_zone=bool(args.remove_zone),
        ## not scenario-specific
        camera_radius=args.camera_distance,
        camera_min_angle=args.camera_min_angle,
        camera_max_angle=args.camera_max_angle,
        camera_min_height=args.camera_min_height,
        camera_max_height=args.camera_max_height,
        monochrome=args.monochrome,
        material_types=args.material_types,
        target_material=args.tmaterial,
        probe_material=args.pmaterial,
        middle_material=args.mmaterial,
        distractor_types=args.distractor,
        distractor_categories=args.distractor_categories,
        num_distractors=args.num_distractors,
        occluder_types=args.occluder,
        occluder_categories=args.occluder_categories,
        num_occluders=args.num_occluders,
        occlusion_scale=args.occlusion_scale,
        remove_middle=args.remove_middle,
        use_ramp=bool(args.ramp),
        ramp_color=args.rcolor,
        flex_only=args.only_use_flex_objects,
        no_moving_distractors=args.no_moving_distractors,
        collision_label_threshold=args.collision_label_threshold,
        max_distance_ratio = args.max_distance_ratio,
        min_distance_ratio = args.min_distance_ratio,
        max_anchorloc = args.max_anchorloc,
        min_anchorloc = args.min_anchorloc,
        anchor_height = args.anchor_height,
        anchor_jitter = args.anchor_jitter,
        height_jitter = args.height_jitter,
        use_test_mode_colors=args.use_test_mode_colors
    )

    if bool(args.run):
        C.run(num=args.num,
             output_dir=args.dir,
             temp_path=args.temp,
             width=args.width,
             height=args.height,
             write_passes=args.write_passes.split(','),
             save_passes=args.save_passes.split(','),
             save_movies=args.save_movies,
             save_labels=args.save_labels,
              save_meshes=args.save_meshes,
             args_dict=vars(args))
    else:
        end = C.communicate({"$type": "terminate"})
        print([OutputData.get_data_type_id(r) for r in end])
