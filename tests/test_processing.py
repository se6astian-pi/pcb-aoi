import sys
import os
import cv2
import numpy as np
import pytest

# Add python directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from pcb_processing import find_all_fiducials, apply_perspective_transform, parse_pcb_config

def test_fiducial_detection():
    image_path = "test_images/pcb.tif"
    template_path = "python/templates/fiducial.tif"

    img = cv2.imread(image_path, 0)
    template = cv2.imread(template_path, 0)

    assert img is not None, "Failed to load test image"
    assert template is not None, "Failed to load fiducial template"

    fiducials = find_all_fiducials(img, template)
    assert len(fiducials) == 4
    for pos in fiducials:
        assert isinstance(pos[0], int)
        assert isinstance(pos[1], int)

def test_perspective_transform():
    image_path = "test_images/pcb.tif"
    img = cv2.imread(image_path)

    # Mock fiducial positions in pixels (approximate for pcb.tif)
    # Based on pcb.mnt and board size, they should be near quadrants
    h, w = img.shape[:2]
    src_points = [
        (w//10, h//10),    # top-left
        (w//10, 9*h//10),  # bottom-left
        (9*w//10, 9*h//10),# bottom-right
        (9*w//10, h//10)   # top-right
    ]

    # Board dimensions from pcb.cfg
    board_cfg = {'pcb_width': 101.60, 'pcb_height': 57.15}
    # Fiducial positions in mm from pcb.mnt
    fiducial_pos_mm = {
        'FID1': (-49.53, 27.305),
        'FID2': (49.53, 27.305),
        'FID3': (49.53, -27.305),
        'FID4': (-49.53, -27.305)
    }

    warped, M, out_w, out_h = apply_perspective_transform(
        img, src_points,
        pcb_width=board_cfg['pcb_width'],
        pcb_height=board_cfg['pcb_height'],
        fiducial_positions_mm=fiducial_pos_mm
    )

    assert warped is not None
    assert out_w > 0
    assert out_h > 0
    assert warped.shape[1] == out_w
    assert warped.shape[0] == out_h
