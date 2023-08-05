import copy
import os
import subprocess
import typing
from pathlib import Path
from typing import Optional

import skimage.io
from skimage import img_as_ubyte
from skimage.morphology import skeletonize, medial_axis

from maphis.common.common import Info
from maphis.common.label_image import RegionProperty, PropertyType
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache, Region
from maphis.common.units import Value
from maphis.common.user_params import UserParam
from maphis.plugins.maphis.properties.geodesic_utils import compute_longest_geodesic, \
    compute_longest_geodesic_perf


class GeodesicLength:
    """
    GROUP: Length & area measurements
    NAME: Geodesic length(cpp)
    DESCRIPTION: Geodesic length (px or mm)
    KEY: geodesic_length2
    """

    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names) -> \
            typing.List[RegionProperty]:
        # lab_img = photo['Labels'].label_image
        props: typing.List[RegionProperty] = []
        for label in region_labels:
            # _, length = get_longest_geodesic(lab_img, label)
            if label not in regions_cache.regions:
                continue
            region_obj = regions_cache.regions[label]
            # length, _, _ = compute_longest_geodesic(region_obj.mask)
            # skeleton = skeletonize(region_obj.mask)
            # length = compute_longest_geodesic_perf(skeleton)
            # skimage.io.imsave('C:/Users/radoslav/Desktop/body_region.png', region_obj.mask)
            # compute_longest_geodesic(lab_img == label)
            bin_path = Path(__file__).parent / 'bin/geodesic_length.exe'
            reg_path = Path(__file__).parent / f'body_region_{photo.image_name}.png'
            skimage.io.imsave(str(reg_path), img_as_ubyte(region_obj.mask), check_contrast=False)
            out_path = Path(__file__).parent / f'result_{photo.image_name}.txt'
            args = [
                str(bin_path),
                str(reg_path),
                str(out_path)
            ]
            return_obj = subprocess.run(args, cwd=str(bin_path.parent))
            if return_obj.returncode != 0:
                continue
            with open(out_path) as f:
                length = float(f.readlines()[0].strip())
            if length < 0:
                os.remove(reg_path)
                os.remove(out_path)
                continue
            prop = RegionProperty()
            prop.label = int(label)
            prop.info = copy.deepcopy(self.info)
            value = Value(float(length), self._px_unit)
            if photo.image_scale is not None:
                # prop.unit = 'mm'
                prop.value = value / photo.image_scale
            else:
                prop.value = value
            prop.val_names = ['Geodesic length2']
            prop.num_vals = 1
            props.append(prop)
            os.remove(reg_path)
            os.remove(out_path)
        return props

    @property
    def user_params(self) -> typing.List[UserParam]:
        return super().user_params

    @property
    def region_restricted(self) -> bool:
        return super().region_restricted

    @property
    def computes(self) -> typing.Dict[str, Info]:
        return {self.info.key: self.info}

    def example(self, prop_name: str) -> RegionProperty:
        prop = RegionProperty()
        prop.label = 0
        prop.info = copy.deepcopy(self.info)
        prop.value = None
        prop.num_vals = 1
        prop.prop_type = PropertyType.Scalar
        prop.val_names = []
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return super(GeodesicLength, self).target_worksheet(self.info.key)

    @property
    def group(self) -> str:
        return super().group
