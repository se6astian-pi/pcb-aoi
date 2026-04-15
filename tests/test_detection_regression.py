import sys
import os
import cv2
import pytest

# Add python directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from pcb_processing import (
    process_image_pipeline, parse_mnt_file, parse_pcb_config,
    generate_overlay_data, compare_pcbs, fiducialBoardPositions
)

def test_component_detection_regression():
    ref_image_path = "test_images/pcb.tif"
    target_image_path = "test_images/pcb_bad.tif"
    template_path = "python/templates/fiducial.tif"
    cfg_path = "test_images/pcb.cfg"
    mnt_path = "test_images/pcb.mnt"

    board_cfg = parse_pcb_config(cfg_path)
    components = parse_mnt_file(mnt_path)
    # fiducialBoardPositions is populated by parse_mnt_file

    template = cv2.imread(template_path, 0)

    # Process reference image
    img_ref, _, _, img_ref_warped, _, warped_w, warped_h = process_image_pipeline(
        ref_image_path, template, board_cfg, fiducialBoardPositions
    )
    img_ref_warped_gray = cv2.cvtColor(img_ref_warped, cv2.COLOR_BGR2GRAY)

    overlay_points_ref, _, _, pixel_per_mm = generate_overlay_data(
        components, board_cfg['pcb_width'], board_cfg['pcb_height'], warped_w, warped_h
    )

    # Process target image (pcb_bad.tif)
    img_target, _, _, img_target_warped, _, warped_w_t, warped_h_t = process_image_pipeline(
        target_image_path, template, board_cfg, fiducialBoardPositions
    )
    img_target_warped_gray = cv2.cvtColor(img_target_warped, cv2.COLOR_BGR2GRAY)

    overlay_points_target, _, _, _ = generate_overlay_data(
        components, board_cfg['pcb_width'], board_cfg['pcb_height'], warped_w_t, warped_h_t
    )

    # Compare
    results = compare_pcbs(
        img_ref_warped_gray, img_target_warped_gray,
        components, overlay_points_ref, overlay_points_target, pixel_per_mm
    )

    assert len(results) > 0

    # Check for mismatches in pcb_bad.tif
    mismatches = [res[0] for res in results if not res[1]]
    print(f"Detected mismatches: {mismatches}")

    # We expect some mismatches in pcb_bad.tif
    assert len(mismatches) > 0, "Regression failed: No mismatches detected in pcb_bad.tif"

    # Example: Check for a specific known mismatch if possible
    # For now, just ensuring that the comparison logic works and finds *something* wrong.
