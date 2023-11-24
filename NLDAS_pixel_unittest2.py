{\rtf1\ansi\ansicpg1252\cocoartf2757
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;}
{\colortbl;\red255\green255\blue255;\red191\green100\blue38;\red0\green0\blue0;\red153\green168\blue186;
\red254\green187\blue91;\red128\green63\blue122;\red109\green109\blue109;\red88\green118\blue71;\red86\green132\blue173;
\red95\green96\blue103;}
{\*\expandedcolortbl;;\csgenericrgb\c74902\c39216\c14902;\csgray\c0\c0;\csgenericrgb\c60000\c65882\c72941;
\csgenericrgb\c99608\c73333\c35686;\csgenericrgb\c50196\c24706\c47843;\csgenericrgb\c42745\c42745\c42745;\csgenericrgb\c34510\c46275\c27843;\csgenericrgb\c33725\c51765\c67843;
\csgenericrgb\c37255\c37647\c40392;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\fs26 \cf2 \cb3 import \cf4 unittest\
\cf2 import \cf4 os\
\cf2 from \cf4 datetime \cf2 import \cf4 datetime\
\cf2 import \cf4 numpy \cf2 as \cf4 np\
\cf2 import \cf4 pandas \cf2 as \cf4 pd\
\cf2 from \cf4 my_module \cf2 import \cf4 read_raster\cf2 , \cf4 parse_filename\
\
\
\cf2 class \cf4 TestMyFunctions(unittest.TestCase):\
    \cf2 def \cf5 test_read_raster\cf4 (\cf6 self\cf4 ):\
        \cf7 # Specify the path to a test GeoTIFF file\
        \cf4 test_file_path = \cf8 '/data/evivoni/NLDAS_SaltVerde/Geotiff_GEO/1980/NLDAS_GEO_19800101.0000_TMP.tif'\
        \cf7 # Assuming the file exists and has appropriate content\
        \cf4 result = read_raster(test_file_path)\
        \cf7 # Define the expected properties of the raster data based on your test data\
        \cf4 expected_rows\cf2 , \cf4 expected_columns = result.shape  \cf7 # Use the actual shape of the raster\
        # Perform assertions based on the expected properties of the raster data\
        \cf6 self\cf4 .assertIsInstance(result\cf2 , \cf4 np.ndarray)\
        \cf6 self\cf4 .assertEqual(result.shape\cf2 , \cf4 (expected_rows\cf2 , \cf4 expected_columns))\
\
    \cf2 def \cf5 test_parse_filename\cf4 (\cf6 self\cf4 ):\
        \cf7 # Specify a test filename\
        \cf4 test_filename = \cf8 'NLDAS_GEO_19800101.0000_TMP.tif'\
        \cf7 # Assuming the filename follows the expected format\
        \cf4 result = parse_filename(test_filename)\
        \cf7 # Define the expected output of parse_filename based on your test data\
        \cf4 expected_result = (\cf9 1980\cf2 , \cf9 1\cf2 , \cf9 1\cf2 , \cf9 0\cf2 , \cf8 'TMP'\cf4 )  \cf7 # replace with actual values\
        # Perform assertions based on the expected output of parse_filename\
        \cf6 self\cf4 .assertEqual(result\cf2 , \cf4 expected_result)\
\
    \cf2 def \cf5 test_process_file_and_create_dataframe\cf4 (\cf6 self\cf4 ):\
        \cf7 # Specify a test GeoTIFF file for processing\
        \cf4 test_file_path = \cf8 '/data/evivoni/NLDAS_SaltVerde/Geotiff_GEO/1980/NLDAS_GEO_19800101.0000_TMP.tif'\
\
        \cf7 # Extract information from the filename using parse_filename\
        \cf4 year\cf2 , \cf4 month\cf2 , \cf4 day\cf2 , \cf4 hour\cf2 , \cf4 variable = parse_filename(os.path.basename(test_file_path))\
\
        \cf7 # Create datetime object\
        \cf10 timestamp \cf4 = datetime(year\cf2 , \cf4 month\cf2 , \cf4 day\cf2 , \cf4 hour)\
\
        \cf7 # Read raster data\
        \cf4 raster_data = read_raster(test_file_path)\
\
        \cf7 # Replace the pixel coordinates with the actual coordinates you're interested in\
        \cf4 selected_pixel_coordinates = (\cf9 12\cf2 , \cf9 16\cf4 )\
\
        \cf7 # Extract values for selected pixels\
        \cf4 selected_pixel_values = raster_data[selected_pixel_coordinates[\cf9 0\cf4 ]\cf2 , \cf4 selected_pixel_coordinates[\cf9 1\cf4 ]]\
\
        \cf7 # Create a DataFrame from the extracted data\
        \cf4 data = \{\
            \cf8 'year'\cf4 : [year]\cf2 ,\
            \cf8 'month'\cf4 : [month]\cf2 ,\
            \cf8 'day'\cf4 : [day]\cf2 ,\
            \cf8 'hour'\cf4 : [hour]\cf2 ,\
            \cf8 'TMP'\cf4 : [selected_pixel_values]\
        \}\
\
        result_df = pd.DataFrame(data)\
\
        \cf7 # Perform assertions based on the expected properties of the DataFrame\
        \cf6 self\cf4 .assertEqual(result_df.shape\cf2 , \cf4 (\cf9 1\cf2 , \cf9 5\cf4 ))  \cf7 # Assuming 5 columns including 'TMP'\
        \cf6 self\cf4 .assertEqual(result_df[\cf8 'year'\cf4 ][\cf9 0\cf4 ]\cf2 , \cf4 year)\
        \cf6 self\cf4 .assertEqual(result_df[\cf8 'month'\cf4 ][\cf9 0\cf4 ]\cf2 , \cf4 month)\
        \cf6 self\cf4 .assertEqual(result_df[\cf8 'day'\cf4 ][\cf9 0\cf4 ]\cf2 , \cf4 day)\
        \cf6 self\cf4 .assertEqual(result_df[\cf8 'hour'\cf4 ][\cf9 0\cf4 ]\cf2 , \cf4 hour)\
        \cf6 self\cf4 .assertEqual(result_df[\cf8 'TMP'\cf4 ][\cf9 0\cf4 ]\cf2 , \cf4 selected_pixel_values)\
\
\
\cf2 if \cf4 __name__ == \cf8 '__main__'\cf4 :\
    unittest.main()\
}