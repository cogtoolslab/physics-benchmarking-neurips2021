# Drop signature

Note: the *drop* object is the one that is being dropped. However, since we care about whether this object hits the target zone on the ground, it is marked and colored as the target object for the collision calculations.

Most of the variance is in the target objects (bottom) and the drop objects (top), which are chosen randomly by default. Note that most target objects mean that the drop object can just roll off and hit the ground. To produce more negative trials, try fixing this to target objects with a flat top and bottom. 

Values that make sense to change over are marked in **bold**.

*inherited from `Dominoes`:*
| Argument | Description | Sensible value | Comment | Suggested range |
--- | --- | --- | --- | ---
| **`room`** | Room   | 'box'  | | `'box', 'tdw', 'house'`
| *`target_zone`* | Target zone object | `['sphere']` 
| `zone_color` | Target zone color | `[1.0,1.0,0.0]` |  Yellow is default
| *`zone_location`* | Location of target zone | `[0.,0.,0.]]` | 
| *`zone_scale_range`* | Dimensions of target zone | `[2.1,0.01,2.0]` 
| `zone_friction` | Friction of target zone | `0.1`
| `probe_objects` | List the probe object is chosen from | `cube`
| ***`target_objects`*** | List the target object is chosen from | `MODEL_NAMES` | | `['pipe,cube]`
| `probe_scale_range` | Range the scaling factor of the probe object is uniformly sampled from | `[0.2, 0.3]`
| `probe_mass_range` | Range the mass of the probe object is uniformly sampled from | `[2.,7.]`
| `probe_color` | RGB color of the probe object | `None` | `None` for random selection that excludes target and zone color
| `probe_rotation_range` | Range the rotation of the probe object is uniformly sampled from  | `[0,0]`
| *`target_scale_range`* | Range the scaling factor of the target object is uniformly sampled from | `[0.4, 0.6]`
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

*specific to `drop`*:
| Argument | Description | Sensible value | Comment | Suggested range |
--- | --- | --- | --- | ---
**`drop_objects`** | `MODEL_NAMES` | List of objects the drop object is to be sampled from |
`height_range` | `[0.5,1.5]` | Range the drop height is uniformly sampled from |
| `drop_scale_range` | Range the scaling factor of the target object is uniformly sampled from | `[0.2, 0.3]`
| `drop_jitter` | Amount to jitter initial drop object horizontal position across trials | `0.02`
| `drop_rotation_range` | Angle applied to drop object rotation uniformly sampled from range | `None`

