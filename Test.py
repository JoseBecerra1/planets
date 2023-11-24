import unittest
import os
from datetime import datetime
import numpy as np
import pandas as pd
from my_module import read_raster, parse_filename

class TestMyFunctions(unittest.TestCase):
    def test_read_raster(self):
        # Specify the path to a test GeoTIFF file
        test_file_path = '/data/evivoni/NLDAS_SaltVerde/Geotiff_GEO/1980/NLDAS_GEO_19800101.0000_TMP.tif'
        # Assuming the file exists and has appropriate content
        result = read_raster(test_file_path)
        # Perform assertions based on the expected properties of the raster data
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (expected_rows, expected_columns))  # replace with actual values

    def test_parse_filename(self):
        # Specify a test filename
        test_filename = 'NLDAS_GEO_19800101.0000_TMP.tif'
        # Assuming the filename follows the expected format
        result = parse_filename(test_filename)
        # Perform assertions based on the expected output of parse_filename
        # expected_result = (expected_year, expected_month, expected_day, expected_hour, expected_variable)
        expected_result = (1980, 1, 1, 0, 'TMP')  # replace with actual values
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
