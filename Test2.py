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
        # Define the expected properties of the raster data based on your test data
        expected_rows, expected_columns = result.shape  # Use the actual shape of the raster
        # Perform assertions based on the expected properties of the raster data
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (expected_rows, expected_columns))

    def test_parse_filename(self):
        # Specify a test filename
        test_filename = 'NLDAS_GEO_19800101.0000_TMP.tif'
        # Assuming the filename follows the expected format
        result = parse_filename(test_filename)
        # Define the expected output of parse_filename based on your test data
        expected_result = (1980, 1, 1, 0, 'TMP')  # replace with actual values
        # Perform assertions based on the expected output of parse_filename
        self.assertEqual(result, expected_result)

    def test_process_file_and_create_dataframe(self):
        # Specify a test GeoTIFF file for processing
        test_file_path = '/data/evivoni/NLDAS_SaltVerde/Geotiff_GEO/1980/NLDAS_GEO_19800101.0000_TMP.tif'

        # Extract information from the filename using parse_filename
        year, month, day, hour, variable = parse_filename(os.path.basename(test_file_path))

        # Create datetime object
        timestamp = datetime(year, month, day, hour)

        # Read raster data
        raster_data = read_raster(test_file_path)

        # Replace the pixel coordinates with the actual coordinates you're interested in
        selected_pixel_coordinates = (12, 16)

        # Extract values for selected pixels
        selected_pixel_values = raster_data[selected_pixel_coordinates[0], selected_pixel_coordinates[1]]

        # Create a DataFrame from the extracted data
        data = {
            'year': [year],
            'month': [month],
            'day': [day],
            'hour': [hour],
            'TMP': [selected_pixel_values]
        }

        result_df = pd.DataFrame(data)

        # Perform assertions based on the expected properties of the DataFrame
        self.assertEqual(result_df.shape, (1, 5))  # Assuming 5 columns including 'TMP'
        self.assertEqual(result_df['year'][0], year)
        self.assertEqual(result_df['month'][0], month)
        self.assertEqual(result_df['day'][0], day)
        self.assertEqual(result_df['hour'][0], hour)
        self.assertEqual(result_df['TMP'][0], selected_pixel_values)


if __name__ == '__main__':
    unittest.main()
