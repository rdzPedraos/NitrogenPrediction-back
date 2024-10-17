import pytest
import cv2  # OpenCV
import exiftool
import os
import glob
import numpy as np
import pyzbar.pyzbar as pyzbar
import matplotlib.pyplot as plt
import mapboxgl

def test_imports():
    print("Successfully imported all required libraries.")

def test_exiftool():
    if os.name == 'nt':
        exiftool_path = os.environ.get('exiftoolpath')
        assert exiftool_path is not None, "Set the exiftoolpath environment variable as described above"
        assert os.path.isfile(exiftool_path), "The provided exiftoolpath isn't a file, check the settings"
    try:
        with exiftool.ExifTool(os.environ.get('exiftoolpath')) as exift:
            print('Successfully executed exiftool.')
    except Exception as e:
        print("Exiftool isn't working. Double-check that you've followed the instructions above.")
        print("The exception text below may help to find the source of the problem:")
        print(e)
        pytest.fail("Exiftool failed to execute.")
