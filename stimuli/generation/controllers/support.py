import sys, os
from argparse import ArgumentParser
import h5py
import json
import copy
import importlib
import numpy as np
from enum import Enum
import random
from typing import List, Dict, Tuple
from weighted_collection import WeightedCollection
from tdw.tdw_utils import TDWUtils
from tdw.librarian import ModelRecord, MaterialLibrarian
from tdw.output_data import OutputData, Transforms
from tdw_physics.rigidbodies_dataset import (RigidbodiesDataset,
                                             get_random_xyz_transform,
                                             get_range,
                                             handle_random_transform_args)
from tdw_physics.util import (MODEL_LIBRARIES,
                              get_parser,
                              xyz_to_arr, arr_to_xyz, str_to_xyz,
                              none_or_str, none_or_int, int_or_bool)

from tdw_physics.target_controllers.dominoes import Dominoes, MultiDominoes, get_args
from tdw_physics.postprocessing.labels import is_trial_valid

MODEL_NAMES = [r.name for r in MODEL_LIBRARIES['models_flex.json'].records]
PRIMITIVE_NAMES = [r.name for r in MODEL_LIBRARIES['models_flex.json'].records]
FULL_NAMES = [r.name for r in MODEL_LIBRARIES['models_full.json'].records if not r.do_not_use]
M = MaterialLibrarian()
MATERIAL_TYPES = M.get_material_types()
MATERIAL_NAMES = {mtype: [m.name for m in M.get_all_materials_of_type(mtype)] \
                  for mtype in MATERIAL_TYPES}

'''
The tower controller generats stims in which the target object is
    amongst a set of stacked objects. A probe object is launched at the base
    and *may* knock over the tower
'''

'''
Arguments:
  Tower objects (all but cap will be cube)
    --num_blocks: 2,3,4,5
    --mscale: "[0.4,0.4]","[0.5,0.5]", "[0.6,0.6]"
    --spacing_jitter: 0.2,0.5,0.7
    --tower_cap: "bowl", "torus", "cube", "triangular_prism"
  Probe
    --fscale: "5.0", "7.0", "9.0"
  Target:
    (still need to figure out what to do about this one...)
'''

def get_tower_args(dataset_dir: str, parse=True):
    """
    Combine Tower-specific args with general Dominoes args
    """
    common = get_parser(dataset_dir, get_help=False)
    domino, domino_postproc = get_args(dataset_dir, parse=False)
    parser = ArgumentParser(parents=[common, domino], conflict_handler='resolve', fromfile_prefix_chars='@')

    parser.add_argument("--remove_target",
                        type=int_or_bool,
                        default=1,
                        help="Whether to remove the target object")
    parser.add_argument("--ramp",
                        type=int,
                        default=0,
                        help="Whether to place the probe object on the top of a ramp")
    parser.add_argument("--rheight",
                        type=none_or_str,
                        default="0",
                        help="Height of the ramp base")
    parser.add_argument("--collision_axis_length",
                        type=float,
                        default=3.0,
                        help="How far to put the probe and target")
    parser.add_argument("--num_blocks",
                        type=int,
                        default=2,
                        help="Number of rectangular blocks to build the tower base with")
    parser.add_argument("--mscale",
                        type=str,
                        default="[0.4,0.5]",
                        help="Scale or scale range for rectangular blocks to sample from")
    parser.add_argument("--mgrad",
                        type=float,
                        default=0.0,
                        help="Size of block scale gradient going from top to bottom of tower")
    parser.add_argument("--tower_cap",
                        type=none_or_str,
                        default="sphere",
                        help="Object types to use as a capper on the tower")
    parser.add_argument("--spacing_jitter",
                        type=float,
                        default=0.3,
                        help="jitter in how to space middle objects, as a fraction of uniform spacing")
    parser.add_argument("--mrot",
                        type=str,
                        default="[-45,45]",
                        help="comma separated list of initial middle object rotation values")
    parser.add_argument("--mmass",
                        type=str,
                        default="2.0",
                        help="comma separated list of initial middle object rotation values")
    parser.add_argument("--target",
                        type=none_or_str,
                        default="cube",
                        help="comma-separated list of possible middle objects")    
    parser.add_argument("--middle",
                        type=none_or_str,
                        default="cube",
                        help="comma-separated list of possible middle objects")
    parser.add_argument("--probe",
                        type=none_or_str,
                        default="sphere",
                        help="comma-separated list of possible target objects")
    parser.add_argument("--pmass",
                        type=str,
                        default="3.0",
                        help="scale of probe objects")
    parser.add_argument("--pscale",
                        type=str,
                        default="0.3",
                        help="scale of probe objects")
    parser.add_argument("--tscale",
                        type=str,
                        default="[0.4,0.4]",
                        help="scale of target objects")
    parser.add_argument("--zone",
                        type=none_or_str,
                        default="cube",
                        help="type of zone object")
    parser.add_argument("--zscale",
                        type=str,
                        default="3.0,0.01,3.0",
                        help="scale of target zone")
    parser.add_argument("--fscale",
                        type=str,
                        default="4.0",
                        help="range of scales to apply to push force")
    parser.add_argument("--frot",
                        type=str,
                        default="[-0,0]",
                        help="range of angles in xz plane to apply push force")
    parser.add_argument("--foffset",
                        type=str,
                        default="0.0,0.5,0.0",
                        help="offset from probe centroid from which to apply force, relative to probe scale")
    parser.add_argument("--fjitter",
                        type=float,
                        default=0.0,
                        help="jitter around object centroid to apply force")
    parser.add_argument("--fwait",
                        type=none_or_str,
                        default="[15,15]",
                        help="How many frames to wait before applying the force")
    parser.add_argument("--camera_distance",
                        type=float,
                        default=3.0,
                        help="radial distance from camera to centerpoint")
    parser.add_argument("--camera_min_angle",
                        type=float,
                        default=0,
                        help="minimum angle of camera rotation around centerpoint")
    parser.add_argument("--camera_max_angle",
                        type=float,
                        default=90,
                        help="maximum angle of camera rotation around centerpoint")

    # for toy towers
    parser.add_argument("--toys",
                        action="store_true",
                        help="Whether to make a tower of toys")
    parser.add_argument("--probe_categories",
                        type=none_or_str,
                        default=None,
                        help="Allowable probe categories")
    parser.add_argument("--target_categories",
                        type=none_or_str,
                        default=None,
                        help="Allowable target categories")
    parser.add_argument("--middle_categories",
                        type=none_or_str,
                        default=None,
                        help="Allowable middle categories")
    parser.add_argument("--invert_blocks",
                        action="store_true",
                        help="whether to invert each block")
    
    

    # for generating training data without zones, targets, caps, and at lower resolution
    parser.add_argument("--training_data_mode",
                        action="store_true",
                        help="Overwrite some parameters to generate training data without target objects, zones, etc.")

    def postprocess(args):

        if args.toys:
            if args.probe is None:
                args.probe = ','.join(FULL_NAMES)
            if args.middle is None:
                args.middle = ','.join(FULL_NAMES)
            if args.target is None:
                args.tower = ','.join(FULL_NAMES)
            args.tower_cap = args.target                
        

        # parent postprocess
        args = domino_postproc(args)

        # ramp height
        args.rheight = handle_random_transform_args(args.rheight)

        # whether to use a cap object on the tower
        if args.tower_cap is not None:
            cap_list = args.tower_cap.split(',')
            assert all([t in MODEL_NAMES for t in cap_list]), \
                "All target object names must be elements of %s" % MODEL_NAMES
            args.tower_cap = cap_list
        else:
            args.tower_cap = []


        return args

    if not parse:
        return (parser, postprocess)

    args = parser.parse_args()
    # args = domino_postproc(args)
    args = postprocess(args)

    return args

class Tower(MultiDominoes):

    STANDARD_BLOCK_SCALE = {"x": 0.5, "y": 0.5, "z": 0.5}
    STANDARD_MASS_FACTOR = 1.0 # cubes

    def __init__(self,
                 port: int = None,
                 num_blocks=3,
                 middle_scale_range=[0.5,0.5],
                 middle_scale_gradient=0.0,
                 tower_cap=[],
                 use_ramp=True,
                 invert_blocks=False,
                 **kwargs):

        super().__init__(port=port, middle_scale_range=middle_scale_range, **kwargs)

        self.use_ramp = use_ramp

        # probe and target different colors
        self.match_probe_and_target_color = False

        # how many blocks in tower, sans cap
        self.num_blocks = self.num_middle_objects = num_blocks

        # how to scale the blocks
        self.middle_scale_gradient = middle_scale_gradient

        # flip blocks upside down
        self.invert_blocks = invert_blocks

        # whether to use a cap
        if len(tower_cap):
            self.use_cap = True
            self._cap_types = self.get_types(tower_cap)
        else:
            self._cap_types = self._middle_types
            self.use_cap = False

    def clear_static_data(self) -> None:
        super().clear_static_data()

        self.cap_type = None
        self.did_fall = None
        self.fall_frame = None
        self.tower_height = 0.0

    def _write_static_data(self, static_group: h5py.Group) -> None:
        super()._write_static_data(static_group)

        static_group.create_dataset("cap_type", data=self.cap_type)
        static_group.create_dataset("use_cap", data=self.use_cap)
        static_group.create_dataset("num_blocks", data=self.num_blocks)

    @staticmethod
    def get_controller_label_funcs(classname = "Tower"):
        funcs = Dominoes.get_controller_label_funcs(classname)

        def num_middle_objects(f):
            try:
                return int(np.array(f['static']['num_blocks']))
            except KeyError:
                return int(len(f['static']['mass'] - 3))

        def did_tower_fall(f):
            return is_trial_valid(f, valid_key='did_fall')

        funcs += [num_middle_objects, did_tower_fall]

        return funcs

    def _write_frame_labels(self,
                            frame_grp: h5py.Group,
                            resp: List[bytes],
                            frame_num: int,
                            sleeping: bool) -> Tuple[h5py.Group, List[bytes], int, bool]:

        labels, resp, frame_num, done = super()._write_frame_labels(
            frame_grp, resp, frame_num, sleeping)

        if frame_num >= 30:
            labels.create_dataset("did_fall", data=bool(self.did_fall))
        else:
            labels.create_dataset("did_fall", data=False)

        return labels, resp, frame_num, done

    # def _get_zone_location(self, scale):
    #     bottom_block_width = get_range(self.middle_scale_range)[1]
    #     bottom_block_width += (self.num_blocks / 2.0) * np.abs(self.middle_scale_gradient)
    #     probe_width = get_range(self.probe_scale_range)[1]
    #     return {
    #         "x": 0.0,
    #         "y": 0.0,
    #         "z": -(0.5 + probe_width) * scale["z"] + bottom_block_width + 0.1,
    #     }

    def _get_zone_location(self, scale):
        return {"x": 0.0, "y": 0.0, "z": 0.0}

    def _set_tower_height_now(self, resp: List[bytes]) -> None:
        top_obj_id = self.object_ids[-1]
        for r in resp[:-1]:
            r_id = OutputData.get_data_type_id(r)
            if r_id == "tran":
                tr = Transforms(r)
                for i in range(tr.get_num()):
                    if tr.get_id(i) == top_obj_id:
                        self.tower_height = tr.get_position(i)[1]

    def get_per_frame_commands(self, resp: List[bytes], frame: int) -> List[dict]:

        cmds = super().get_per_frame_commands(resp, frame)

        # check if tower fell
        self.did_fall = False
        if frame == self.force_wait:
            self._set_tower_height_now(resp)
            self.init_height = self.tower_height + 0.
        elif frame > self.force_wait:
            self._set_tower_height_now(resp)
            self.did_fall = (self.tower_height < 0.5 * self.init_height)
            if (self.fall_frame is None) and (self.did_fall == True):
                self.fall_frame = frame

        return cmds

    def _build_intermediate_structure(self) -> List[dict]:
        print("middle color", self.middle_color)
        if self.randomize_colors_across_trials:
            self.middle_color = self.random_color(exclude=self.target_color) if self.monochrome else None
        self.cap_color = self.target_color
        commands = []

        commands.extend(self._build_stack())
        commands.extend(self._add_cap())

        # set camera params
        camera_y_aim = 0.5 * self.tower_height
        self.camera_aim = arr_to_xyz([0.,camera_y_aim,0.])

        return commands

    def _get_block_position(self, scale, y):
        jitter = lambda: random.uniform(-self.spacing_jitter, self.spacing_jitter)
        jx, jz = [scale["x"]*jitter(), scale["z"]*jitter()]
        return {"x": jx, "y": y, "z": jz}

    def _get_block_scale(self, offset) -> dict:
        print("scale range", self.middle_scale_range)
        scale = get_random_xyz_transform(self.middle_scale_range)
        scale = {k:v+offset for k,v in scale.items()}

        return scale

    def _build_stack(self) -> List[dict]:
        commands = []
        height = self.tower_height
        height += self.zone_scale['y'] if not self.remove_zone else 0.0

        # build the block scales
        mid = self.num_blocks / 2.0
        grad = self.middle_scale_gradient
        self.block_scales = [self._get_block_scale(offset=grad*(mid-i)) for i in range(self.num_blocks)]
        self.blocks = []

        # place the blocks
        for m in range(self.num_blocks):
            record, data = self.random_primitive(
                self._middle_types,
                scale=self.block_scales[m],
                color=self.middle_color,
                exclude_color=self.target_color)
            self.middle_type = data["name"]
            o_id, scale, rgb = [data[k] for k in ["id", "scale", "color"]]
            block_pos = self._get_block_position(scale, height)
            block_rot = self.get_y_rotation(self.middle_rotation_range)

            if self.invert_blocks:
                _,by,_ = self.get_record_dimensions(record)
                block_rot['z'] = 180.
                block_pos['y'] += by + 0.25

            # scale the mass to give each block a uniform density
            block_mass = random.uniform(*get_range(self.middle_mass_range))
            block_mass *= (np.prod(xyz_to_arr(scale)) / np.prod(xyz_to_arr(self.STANDARD_BLOCK_SCALE)))
            block_mass *= self.STANDARD_MASS_FACTOR

            ## master
            # commands.extend(
            #     self.add_physics_object(
            #         record=record,
            #         position=block_pos,
            #         rotation=block_rot,
            #         mass=block_mass,
            #         dynamic_friction=random.uniform(0, 0.9),
            #         static_friction=random.uniform(0, 0.9),
            #         bounciness=random.uniform(0, 1),
            #         o_id=o_id))


            commands.extend(
                self.add_primitive(
                    record=record,
                    position=block_pos,
                    rotation=block_rot,
                    scale=scale,
                    material=self.middle_material,
                    color=rgb,
                    scale_mass=False,
                    o_id=o_id,
                    apply_texture=(True if (record.name in PRIMITIVE_NAMES) or (self.middle_material is not None) else False)
                ))

            # Set the block object material
            # commands.extend(
            #     self.get_object_material_commands(
            #         record, o_id, self.get_material_name(self.middle_material)))


            # # Scale the object and set its color.
            # commands.extend([
            #     {"$type": "set_color",
            #      "color": {"r": rgb[0], "g": rgb[1], "b": rgb[2], "a": 1.},
            #      "id": o_id},
            #     {"$type": "scale_object",
            #      "scale_factor": scale,
            #      "id": o_id}])

            print("placed middle object %s" % str(m+1))

            # update height
            _y = record.bounds['top']['y'] if self.middle_type != 'bowl' else (record.bounds['bottom']['y'] + 0.1)
            height += scale["y"] * _y

            data.update({'position': block_pos, 'rotation': block_rot, 'mass': block_mass})
            print("middle object data", data)
            self.blocks.append((record, data))
            self.tower_height = height

        return commands

    def _add_cap(self) -> List[dict]:
        commands = []

        # the cap becomes the target
        record, data = self.random_primitive(
            self._cap_types,
            scale=self.target_scale_range,
            color=self.target_color,
            add_data=self.use_cap
        )
        o_id, scale, rgb = [data[k] for k in ["id", "scale", "color"]]
        self.cap  = record
        self.cap_type = data["name"]
        if self.use_cap:
            self._replace_target_with_object(record, data)

        mass = random.uniform(*get_range(self.middle_mass_range))
        mass *= (np.prod(xyz_to_arr(scale)) / np.prod(xyz_to_arr(self.STANDARD_BLOCK_SCALE)))
        mass *= self.STANDARD_MASS_FACTOR

        commands.extend(
            self.add_physics_object(
                record=record,
                position={
                    "x": 0.,
                    "y": self.tower_height,
                    "z": 0.
                },
                rotation={"x":0.,"y":0.,"z":0.},
                mass=mass,
                dynamic_friction=0.5,
                static_friction=0.5,
                bounciness=0,
                o_id=o_id,
                add_data=self.use_cap
            ))

        # Set the cap object material
        commands.extend(
            self.get_object_material_commands(
                record, o_id, self.get_material_name(self.target_material)))

        # Scale the object and set its color.
        commands.extend([
            {"$type": "set_color",
             "color": {"r": rgb[0], "g": rgb[1], "b": rgb[2], "a": 1.},
             "id": o_id},
            {"$type": "scale_object",
             "scale_factor": scale,
             "id": o_id}])

        if not self.use_cap:
            commands.append(
                {"$type": self._get_destroy_object_command_name(o_id),
                 "id": int(o_id)})
            self.object_ids = self.object_ids[:-1]
        else:
            self.tower_height += scale["y"]

        return commands

    def is_done(self, resp: List[bytes], frame: int) -> bool:
        return frame > 600
        # return (frame > 750) or (self.fall_frame is not None and ((frame - 60) > self.fall_frame))


class ToyTower(Tower):

    def __init__(self, port=1071,
                 probe_categories=None,
                 target_categories=None,
                 middle_categories=None,
                 size_min=0.1,
                 size_max=2.0,
                 **kwargs):

        self.probe_categories = probe_categories
        self.target_categories = target_categories
        self.middle_categories = middle_categories
        self.size_min, self.size_max = [size_min, size_max]

        super().__init__(port=port, **kwargs)

    def get_types(self, objlist, categories=None, **kwargs):
        libs = ["models_full.json", "models_flex.json", "models_special.json"]
        tlist = super().get_types(
            objlist,
            libraries=libs,
            categories=categories,
            flex_only=False,
            size_min=self.size_min,
            size_max=self.size_max)
        return tlist

    def set_zone_types(self, olist):
        self._zone_types = self.get_types(olist, None)

    def set_probe_types(self, olist):
        self._probe_types = self.get_types(olist, self.probe_categories)

    def set_target_types(self, olist):
        self._target_types = self.get_types(olist, self.target_categories)

    def set_middle_types(self, olist):
        self._middle_types = self.get_types(olist, self.middle_categories)

if __name__ == "__main__":

    args = get_tower_args("towers")

    import platform
    if platform.system() == 'Linux':
        if args.gpu is not None:
            os.environ["DISPLAY"] = ":0." + str(args.gpu)
        else:
            os.environ["DISPLAY"] = ":0"

    if args.toys:
        TC = ToyTower
    else:
        TC = Tower

    TC = Tower(
        port=args.port,
        # toy tower
        probe_categories=args.probe_categories,
        target_categories=args.target_categories,
        middle_categories=args.middle_categories,
        invert_blocks=args.invert_blocks,
        # tower specific
        num_blocks=args.num_blocks,
        tower_cap=args.tower_cap,
        spacing_jitter=args.spacing_jitter,
        middle_rotation_range=args.mrot,
        middle_scale_range=args.mscale,
        middle_mass_range=args.mmass,
        middle_scale_gradient=args.mgrad,
        # domino specific
        target_zone=args.zone,
        zone_location=args.zlocation,
        zone_scale_range=args.zscale,
        zone_color=args.zcolor,
        zone_friction=args.zfriction,
        target_objects=args.target,
        probe_objects=args.probe,
        middle_objects=args.middle,
        target_scale_range=args.tscale,
        target_rotation_range=args.trot,
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
        remove_target=bool(args.remove_target),
        remove_zone=bool(args.remove_zone),
        ## not scenario-specific
        room=args.room,
        randomize=args.random,
        seed=args.seed,
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
        zone_material=args.zmaterial,
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
        ramp_base_height_range=args.rheight,
        flex_only=args.only_use_flex_objects,
        no_moving_distractors=args.no_moving_distractors,
        use_test_mode_colors=args.use_test_mode_colors
    )

    if bool(args.run):
        TC.run(num=args.num,
               output_dir=args.dir,
               temp_path=args.temp,
               width=args.width,
               height=args.height,
               framerate=args.framerate,
               write_passes=args.write_passes.split(','),
               save_passes=args.save_passes.split(','),
               save_movies=args.save_movies,
               save_labels=args.save_labels,
               save_meshes=args.save_meshes,
               args_dict=vars(args)
        )
    else:
        TC.communicate({"$type": "terminate"})
