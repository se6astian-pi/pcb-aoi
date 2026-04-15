import sys
import os
import tkinter as tk
import pytest
from PIL import Image, ImageTk

# Add python directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from pcb_processing import launch_image_viewer, launch_mnt_viewer, parse_mnt_file
from packages_config import create_packages_config_gui

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

def test_image_viewer_init(root):
    # Test initialization with a dummy image or actual test image
    image_path = "test_images/pcb.tif"
    viewer = launch_image_viewer(image_path, master=root)
    assert viewer is not None
    assert "set_image" in viewer
    assert "refresh" in viewer
    root.update() # Process events

def test_mnt_viewer_init(root):
    mnt_path = "test_images/pcb.mnt"
    components = parse_mnt_file(mnt_path)
    launch_mnt_viewer(mnt_path, master=root, components=components)
    root.update()

def test_packages_config_gui_init(root):
    mnt_path = "test_images/pcb.mnt"
    components = parse_mnt_file(mnt_path)
    gui = create_packages_config_gui(master=root, components=components)
    assert gui is not None
    assert 'root' in gui
    root.update()
