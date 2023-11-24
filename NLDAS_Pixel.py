{\rtf1\ansi\ansicpg1252\cocoartf2757
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;}
{\colortbl;\red255\green255\blue255;\red191\green100\blue38;\red0\green0\blue0;\red153\green168\blue186;
\red254\green187\blue91;\red86\green132\blue173;\red88\green118\blue71;\red117\green114\blue185;\red109\green109\blue109;
\red152\green54\blue29;\red32\green32\blue32;}
{\*\expandedcolortbl;;\csgenericrgb\c74902\c39216\c14902;\csgray\c0\c0;\csgenericrgb\c60000\c65882\c72941;
\csgenericrgb\c99608\c73333\c35686;\csgenericrgb\c33725\c51765\c67843;\csgenericrgb\c34510\c46275\c27843;\csgenericrgb\c45882\c44706\c72549;\csgenericrgb\c42745\c42745\c42745;
\csgenericrgb\c59608\c21176\c11373;\csgenericrgb\c12549\c12549\c12549;}
\margl1440\margr1440\vieww29200\viewh17260\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\fs26 \cf2 \cb3 import \cf4 os\
\cf2 from \cf4 osgeo \cf2 import \cf4 gdal\
\cf2 import \cf4 numpy \cf2 as \cf4 np\
\cf2 import \cf4 pandas \cf2 as \cf4 pd\
\cf2 from \cf4 datetime \cf2 import \cf4 datetime\
\
\cf2 def \cf5 read_raster\cf4 (file_path):\
    dataset = gdal.Open(file_path)\
    band = dataset.GetRasterBand(\cf6 1\cf4 )\
    raster_array = band.ReadAsArray()\
    \cf2 return \cf4 raster_array\
\
\cf2 def \cf5 parse_filename\cf4 (filename):\
    parts = filename.split(\cf7 '_'\cf4 )\
    date_str = parts[\cf6 2\cf4 ]\
    variable = parts[\cf6 3\cf4 ]\
\
    year = \cf8 int\cf4 (date_str[:\cf6 4\cf4 ])\
    month = \cf8 int\cf4 (date_str[\cf6 4\cf4 :\cf6 6\cf4 ])\
    day = \cf8 int\cf4 (date_str[\cf6 6\cf4 :\cf6 8\cf4 ])\
    hour = \cf8 int\cf4 (date_str[\cf6 9\cf4 :\cf6 11\cf4 ])\
\
    \cf2 return \cf4 year\cf2 , \cf4 month\cf2 , \cf4 day\cf2 , \cf4 hour\cf2 , \cf4 variable\
\
\cf9 # Specify the path to the specific GeoTIFF file\
\cf4 file_to_process = \cf7 '/data/evivoni/NLDAS_SaltVerde/Geotiff_GEO/1980/NLDAS_GEO_19800101.0000_TMP.tif'\
\
\cf9 # Extract information from the filename using parse_filename\
\cf4 year\cf2 , \cf4 month\cf2 , \cf4 day\cf2 , \cf4 hour\cf2 , \cf4 _ = parse_filename(os.path.basename(file_to_process))\
\
\cf9 # Create datetime object\
\cf4 timestamp = datetime(year\cf2 , \cf4 month\cf2 , \cf4 day\cf2 , \cf4 hour)\
\
\cf9 # Read raster data\
\cf4 raster_data = read_raster(file_to_process)\
\
\cf9 # Replace the pixel coordinates with the actual coordinates you're interested in\
\cf4 selected_pixel_coordinates = (\cf6 12\cf2 , \cf6 16\cf4 )\
\
\cf9 # Extract values for selected pixels\
\cf4 selected_pixel_values = raster_data[selected_pixel_coordinates[\cf6 0\cf4 ]\cf2 , \cf4 selected_pixel_coordinates[\cf6 1\cf4 ]]\
\
\cf9 # Create a DataFrame from the extracted data\
\cf4 data = \{\
    \cf7 'year'\cf4 : [year]\cf2 ,\
    \cf7 'month'\cf4 : [month]\cf2 ,\
    \cf7 'day'\cf4 : [day]\cf2 ,\
    \cf7 'hour'\cf4 : [hour]\cf2 ,\
    \cf7 'TMP'\cf4 : [selected_pixel_values]\
\}\
\
result_df = pd.DataFrame(data)\
\
\cf9 # Display the result\
\cf8 print\cf4 (result_df)\
\
\cf9 # Specify the output directory and save the DataFrame to a CSV file\
\cf4 output_directory = \cf7 '/data/evivoni/Jabecer/NLDAS/NLDAS_Cragin/GeoTIFF_Rasters/'\
\cf4 output_csv_filename = \cf7 'Station_test_single_file.csv'\
\cf4 output_csv_path = os.path.join(output_directory\cf2 , \cf4 output_csv_filename)\
result_df.to_csv(output_csv_path\cf2 , \cf10 index\cf4 =\cf2 False\cf4 )\
\cb11 \
}