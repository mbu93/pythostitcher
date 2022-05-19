import numpy as np
import os
import warnings
import pickle
from skimage.transform import resize
from skimage.io import imread

from .get_resname import get_resname


def preprocess(quadrant_A, quadrant_B, quadrant_C, quadrant_D):
    """
    Function to load and preprocess all the quadrant images.

    Input:
        - Quadrant class with basic info

    Output:
        - Quadrant class with all loaded images
    """

    # Make directories for later saving
    dirnames = [f"../results",
                f"../results/{quadrant_D.patient_idx}",
                f"../results/{quadrant_D.patient_idx}/{quadrant_D.slice_idx}",
                f"../results/{quadrant_D.patient_idx}/{quadrant_D.slice_idx}/{quadrant_D.res_name}"]

    for name in dirnames:
        if not os.path.isdir(name):
            os.mkdir(name)

    # Verify whether preprocessed quadrants are available
    filepath = f"../results/{quadrant_D.patient_idx}/{quadrant_D.slice_idx}/{quadrant_D.res_name}/quadrant_{quadrant_D.quadrant_name}"
    file_exists = os.path.isfile(filepath)

    # Preprocess all images if they are not yet available
    if not file_exists:

        # Load images
        quadrant_A.read_image()
        quadrant_B.read_image()
        quadrant_C.read_image()
        quadrant_D.read_image()

        # Preprocess (resize+pad) gray images
        quadrant_A.preprocess_gray_image()
        quadrant_B.preprocess_gray_image()
        quadrant_C.preprocess_gray_image()
        quadrant_D.preprocess_gray_image()

        # Preprocess (resize+pad) colour images
        quadrant_A.preprocess_colour_image()
        quadrant_B.preprocess_colour_image()
        quadrant_C.preprocess_colour_image()
        quadrant_D.preprocess_colour_image()

        # Segment tissue. This basically loads in the stored segmentations
        quadrant_A.segment_tissue()
        quadrant_B.segment_tissue()
        quadrant_C.segment_tissue()
        quadrant_D.segment_tissue()

        # Apply mask to both gray and colour image
        quadrant_A.apply_masks()
        quadrant_B.apply_masks()
        quadrant_C.apply_masks()
        quadrant_D.apply_masks()

        # Save the quadrant class for later use
        quadrant_A.save_quadrant()
        quadrant_B.save_quadrant()
        quadrant_C.save_quadrant()
        quadrant_D.save_quadrant()

    # Else just load them from a previous run
    else:
        basepath_load = f"../results/{quadrant_D.patient_idx}/{quadrant_D.slice_idx}/{quadrant_D.res_name}"

        # Load quadrant objects
        with open(f"{basepath_load}/quadrant_{quadrant_A.quadrant_name}", "rb") as loadfile:
            quadrant_A = pickle.load(loadfile)
        with open(f"{basepath_load}/quadrant_{quadrant_B.quadrant_name}", "rb") as loadfile:
            quadrant_B = pickle.load(loadfile)
        with open(f"{basepath_load}/quadrant_{quadrant_C.quadrant_name}", "rb") as loadfile:
            quadrant_C = pickle.load(loadfile)
        with open(f"{basepath_load}/quadrant_{quadrant_D.quadrant_name}", "rb") as loadfile:
            quadrant_D = pickle.load(loadfile)

        # Load all images separately
        quadrant_A.load_images()
        quadrant_B.load_images()
        quadrant_C.load_images()
        quadrant_D.load_images()

    return quadrant_A, quadrant_B, quadrant_C, quadrant_D

