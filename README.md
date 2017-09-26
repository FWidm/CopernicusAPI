# Copernicus Sample API

Is an example for a simple API that has two main tasks:
 1. Retrieve grib files from the ECMWF server for specific dates 
 2. Allow parsing of the files by specifying the file, location and timestamp to retrieve all kinds of atmospheric information
 
Subgoals:
 1. Structured
 2. Simple
 3. Extendable

## Acknowledgements
- Receives and returns data by using and modifying Copernicus Atmosphere Monitoring Service Information 2017 -  ongoing

## Requirements
- Python 2.7
- Installed ECWMFAPI and ECCodes
    - can be done by using conda with the following packages: 
        - eccodes: https://anaconda.org/conda-forge/python-eccodes
        - ecmwf-api: `source activate <env name>` 
        followed by `pip install https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz`
   - calling the api from another scripting language can be done
        - refer to [Info.md](/doc/info.md)
- Installed https://github.com/FWidm/CopernicusRetrieval (thus the requirements above)
        


## Documentation
- Swagger: [doc](doc/CopernicusAPI_swagger.yaml)
- Postman: 
    - [collection](doc/Copernicus%20API.postman_collection.json)
    - [env](doc/Copernicus%20API.postman_environment.json)
    
## Usage 
- List of available files: `http://{{host}}:{{port}}/list`
  ```json
  {
    "files": [
        "an-2017-09-18.grib"
    ]
  }
  ```
- Retrieve files: `http://{{host}}:{{port}}/retrieve?timestamp={{timestamp}}` with timestamp=`2017-09-18T15:21:20%2B00:00`
  ```json
  {
    "file_name": "an-2017-09-18.grib"
  }
  ```
- Parse files: `http://{{host}}:{{port}}/parse/{{file_name}}?timestamp={{timestamp}}&lat={{lat}}&lon={{lon}}` with file_name=`an2017-09-18.grib`, timestamp=`2017-09-18T15:21:20%2B00:00`, lat=`48.3984` and lon=`9.59155
` 
  ```json
  {
      "TWO_METRE_TEMPERATURE": [
        {
            "index": 45047,
            "description": {
                "dataTime": 1200,
                "name": "2 metre temperature",
                "date": 20170918,
                "step": 0,
                "units": "K",
                "shortName": "2t",
                "paramId": 167,
                "convertedUnit": "C"
            },
            "classification": "Temperature",
            "distance": 13.558712398993372,
            "longitude": 9.5,
            "date": "2017-09-18T12:00:00+00:00",
            "value": 284.29498291015625,
            "latitude": 48.29265233053008,
            "type": "2 metre temperature"
        },
        {
            "index": 45047,
            "description": {
                "dataTime": 1800,
                "name": "2 metre temperature",
                "date": 20170918,
                "step": 0,
                "units": "K",
                "shortName": "2t",
                "paramId": 167,
                "convertedUnit": "C"
            },
            "classification": "Temperature",
            "distance": 13.558712398993372,
            "longitude": 9.5,
            "date": "2017-09-18T18:00:00+00:00",
            "value": 281.47601318359375,
            "latitude": 48.29265233053008,
            "type": "2 metre temperature"
        }
    ],
  ...
  }
  ``` 
## Tasks
- Integrate to an SQLite in memory db
- OAuth for production
- Swap Cache for production
- Allow the user to configure which parameters should be parsed instead of parsing all of them
- Maybe: Customize retrieval to save bandwidth - which will in turn make data management harder.

