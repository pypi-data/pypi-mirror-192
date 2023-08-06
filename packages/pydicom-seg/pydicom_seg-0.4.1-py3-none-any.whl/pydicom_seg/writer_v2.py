from dataclasses import dataclass
from typing import List, Mapping, Optional, Set, Union

import numpy as np
import pydicom
import SimpleITK as sitk

from pydicom_seg.typing import FSPath


@dataclass
class OptimizationOptions:
    inplane_cropping: bool = False
    skip_empty_slices: bool = True
    skip_missing_segment: bool = False
    rle_compression: bool = False


def write_volume_labelmap(
    segmentation: sitk.Image,
    source_dicoms: List[Union[pydicom.Dataset, FSPath]],
    template: pydicom.Dataset,
    optimization_options: Optional[OptimizationOptions] = None,
) -> pydicom.Dataset:
    return write_volume_labelmaps(
        segmentations=[segmentation],
        source_dicoms=source_dicoms,
        template=template,
        optimization_options=optimization_options,
    )


def write_volume_labelmaps(
    segmentations: List[sitk.Image],
    source_dicoms: List[Union[pydicom.Dataset, FSPath]],
    template: pydicom.Dataset,
    optimization_options: Optional[OptimizationOptions] = None,
) -> pydicom.Dataset:
    # Normalize user input
    if not optimization_options:
        optimization_options = OptimizationOptions()
    normalized_source_dicoms = _normalize_source_images(source_dicoms)

    _assert_volumes(segmentations)
    if len(segmentations) > 1:
        _assert_segments_not_overlapping(segmentations)

    labels_in_volume = [
        set(np.unique(sitk.GetArrayViewFromImage(x))) - {0} for x in segmentations
    ]
    _assert_labels_not_intersecting(labels_in_volume)
    print(labels_in_volume)

    # Check for duplicate segmentation number
    # Check for labelmap overlap


def write_volume_multilabel_from_binary(
    segmentation: Mapping[int, sitk.Image],
    source_dicoms: List[Union[pydicom.Dataset, FSPath]],
    template: pydicom.Dataset,
    optimization_options: Optional[OptimizationOptions] = None,
) -> pydicom.Dataset:
    pass


def write_volume_multilabel_from_labelmaps(
    segmentation: List[sitk.Image],
    source_dicoms: List[Union[pydicom.Dataset, FSPath]],
    template: pydicom.Dataset,
    optimization_options: Optional[OptimizationOptions] = None,
) -> pydicom.Dataset:
    pass


def _assert_volumes(images: List[sitk.Image]):
    for image in images:
        assert len(image.GetSize()) == 3
        assert image.GetNumberOfComponentsPerPixel() == 1


def _assert_segments_not_overlapping(images: List[sitk.Image]):
    pass


def _assert_labels_not_intersecting(label_sets: List[Set[int]]):
    if len(label_sets) == 1:
        return

    label_union = label_sets[0].copy()
    for idx, label_set in enumerate(label_sets[1:], 1):
        label_intersection = label_union & label_set
        if len(label_union & label_set) > 0:
            print(f"input {idx} has duplicate label {label_intersection}")
            raise RuntimeError()
        label_union |= label_set


def _normalize_source_images(
    dcms_or_paths: List[Union[pydicom.Dataset, FSPath]]
) -> List[pydicom.Dataset]:
    """Load DICOM from any given path and normalize the data structure to
    only pydicom Datasets.

    Args:
        dcms_or_paths: A list of `pydicom.Dataset`s and/or filesystem paths.

    Returns:
        A list with only `pydicom.Dataset`s.
    """
    result: List[pydicom.Dataset] = []
    for elem in dcms_or_paths:
        if isinstance(elem, pydicom.Dataset):
            result.append(elem)
        else:
            # TODO Load only required tags for writing DICOM-SEG
            dcm = pydicom.dcmread(elem, stop_before_pixels=True)
            result.append(dcm)
    return result


if __name__ == "__main__":
    seg = sitk.ReadImage(
        "/mnt/Daten/cloud/uk-essen/hierarchical-segmentation-datasets/livo-v2/train/labels/001.nii.gz"
    )

    write_volume_labelmap(seg, [], pydicom.Dataset())
    write_volume_labelmaps([seg, seg], [], pydicom.Dataset())
