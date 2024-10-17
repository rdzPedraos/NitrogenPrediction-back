import os
import glob
import pytest
from micasense.image import Image
from micasense.panel import Panel

def test_load_image():
    image_path = os.path.join('storage', '0')
    image_pattern = os.path.join(image_path, '1.tif')
    image_files = glob.glob(image_pattern)
    assert len(image_files) > 0, f"No image files found matching pattern {image_pattern}"
    image_name = image_files[0]

    img = Image(image_name)
    assert img is not None, "Failed to load image"
    assert img.raw().size > 0, "Image data is empty"


def test_panel_detection():
    image_path = os.path.join('storage', '0')
    panel_pattern = os.path.join(image_path, 'panel_1.tif')
    panel_files = glob.glob(panel_pattern)
    assert len(panel_files) > 0, f"No panel images found matching pattern {panel_pattern}"
    panel_name = panel_files[0]

    img = Image(panel_name)
    panel = Panel(img)

    assert panel.panel_detected(), "Panel not detected"

    print(f"Detected panel serial: {panel.serial}")
    mean, std, num, sat_count = panel.raw()
    print("Extracted Panel Statistics:")
    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")
    print(f"Panel Pixel Count: {num}")
    print(f"Saturated Pixel Count: {sat_count}")

    assert num > 0, "No pixels detected in panel"
