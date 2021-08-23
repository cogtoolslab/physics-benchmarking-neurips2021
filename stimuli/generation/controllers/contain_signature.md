# Containment signature

**Note**: The `Containment.py` controller subclasses off of the Towers controller. In essence, each scenario is a base (container) with 
middle objects (one of which is the target) stacked and falling into the container.

Values that make sense to change over are marked in **bold**.
I would recommend only changing the vlaues below that are specific to containment, as most of the rest are all generic to towers or mulitdominoes.

*Key arguments specific to containment:*
| Argument | Description | Sensible value | Comment | Suggested range |
--- | --- | --- | --- | ---
|**`middle`** | The contained objects | `'sphere'` | --- | `'sphere', 'cube'`
|**`mscale`** | Size of contained objects | `"0.3,0.3,0.3"` | --- | `"0.1,0.1,0.1", "0.3,0.3,0.3", "0.5,0.5,0.5"`
|**`num_middle_range`** | Range for number of middle objects | `[1,6]` | will randomly sample within range | `[1,6]`
|**`spacing_jitter`** | jitter of contained objects | `0.5` | as a fraction of uniform spacing | `0.5,1,1.5`
|**`attachment`** | The contained container (e.g. bowl stacked on bowl) | `None` | --- | `None, "bowl", "torus"`
|**`ascale`** | Size on contained container | `"0.5,0.5,0.5"` | --- | `"0.5,0.5,0.5", "0.7,0.7,0.7", "0.9,0.9,0.9"`
|**`base`** | Base Container | `'bowl'` | --- | `"bowl", "torus"`
|**`bscale`** | Size on base container | `"0.7,0.7,0.7"` | --- | `"0.5,0.5,0.5", "0.7,0.7,0.7", "0.9,0.9,0.9"`
|**`fscale`** | Force applied to probe | `"5.0"` | In my experience >7 can knock over the bowls | `"5.0", "7.0", "9.0"`

*inherited from `Tower`:*
| Argument | Description | Sensible value | Comment | Suggested range |
--- | --- | --- | --- | ---
| **`room`** | Room   | 'box'  | | `'box', 'tdw', 'house'`
| `target_zone` | Target zone object | `['cube']` 
| `zone_color` | Target zone color | `[1.0,1.0,0.0]` |  Yellow is default
| `zone_location` | Location of target zone | `None` | Set by controllers
| `zone_scale_range` | Dimensions of target zone | `[0.5,0.01,0.5]` 
| `zone_friction` | Friction of target zone | `0.1`
| `probe_objects` | List the probe object is chosen from | `cube`
| `target_objects` | List the target object is chosen from | `cube`
| `probe_scale_range` | Range the scaling factor of the probe object is uniformly sampled from | `[0.2, 0.3]`
| `probe_mass_range` | Range the mass of the probe object is uniformly sampled from | `[2.,7.]`
| `probe_color` | RGB color of the probe object | `None` | `None` for random selection that excludes target and zone color
| `probe_rotation_range` | Range the rotation of the probe object is uniformly sampled from  | `[0,0]`
| `target_scale_range` | Range the scaling factor of the target object is uniformly sampled from | `[0.2, 0.3]`
| `target_rotation_range` | Range the rotation of the target object is uniformly sampled from | `[0,0]`
| `target_color` | Color of the target object | `[1.0,0.0,0.0]` | Red is default target color
| `target_motion_thresh` | Threshold for target motion  | `0.01`
| **`collision_axis_length`** | Distance from probe to target object | `1.` | | `[1.0,2.0]`
| `force_scale_range` | Range the scaling factor of the force applied to the probe object is uniformly sampled from | `[0.,8.]`
| **`force_angle_range`** | Range the angle of the force applied to the probe object is uniformly sampled from | `[-60,60]`
| **`force_offset`** | Offset of the force applied to the probe object | `{"x":0.,"y":0.5,"z":0.0}` | | 
| `force_offset_jitter` | Jitter of the force applied to the probe object | `0.1`
| `force_wait` | Delay before the force is applied to the probe object | `0.0`
| `remove_target` | Should the target object be removed from the scene? | `False`
| `remove_zone` | Should the target zone be removed from the scene? | `False`
| `camera_radius` | Camera radius | `1.0`
| `camera_min_angle` | Camera min angle | `0`
| `camera_max_angle` | Camera max angle | `360`
| `camera_min_height` | Camera min height | `1./3`
| `camera_max_height` | Camera max height | `2./3`
| `material_types` | Which class of materials to sample material names from | `['Wood','Metal','Plastic']`
| `target_material` | Material of the target object | `parquet_wood_red_cedar`
| `probe_material` | Material of the probe object | `parquet_wood_red_cedar`
| `zone_material` | Material of the target zone | `wood_european_ash`
| `distractor_types` | The names or library of distractor objects to use | `core`
| `distractor_categories` | The categories of distractors to choose from | `None`
| **`num_distractors`** | The number of background distractor objects to place | `0` | | `[0,3]`
| `occluder_types` | The names or library of occluder objects to use | `core`
| `occluder_categories` | The categories of occluders to choose from (comma-separated) | `None`
| **`num_occluders`** | The number of foreground occluder objects to place | `0` | | `[0,3]`
| `occlusion_scale` | The height of the occluders as a proportion of camera height | `0.6`
| `use_ramp` | Should a ramp be placed under the probe object? | `False`
| `ramp_scale` | Scaling factor of the ramp | `None`
| `ramp_color` | Color of the ramp | `None`
| `ramp_base_height_range` | Height of the base of the ramp? | `0`
| 'monochrome' | Should all objects share a color? | `True` | 

<!---
*specific to `MultiDominoes`*:
| Argument | Description | Sensible value | Comment | Suggested range |
--- | --- | --- | --- | ---
| `middle_objects` | Types of the middle objects  |` None` | Defaults to type of the target object
| **`num_middle_objects`** |  How many middle objects to insert? |` 1` | | `[1,3]`
| `middle_color` | Color of the middle objects in RGB |` None` |
| **`middle_scale_range`** | Scale or scale range (uniformly sampled) for middle objects |` 0.5` | | ?
| **`middle_rotation_range`** | Rotation or rotation range (uniformly sampled) for middle objects |` [-30,30]` |
| `middle_mass_range` | Mass or mass range (uniformly sampled) for middle objects |` 2.0` |
| `horizontal` | Whether to rotate middle objects horizontally  |` False` |
| **`spacing_jitter`** | jitter in how to space middle objects, as a fraction of uniform spacing |` 0.2` | | `[0.0,0.2]`
| **`lateral_jitter`** | lateral jitter in how to space middle objects, as a fraction of object width |` 
-->
