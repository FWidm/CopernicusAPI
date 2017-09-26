# Copernicus Sample API

Retrieves data from the copernicus server.

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
        

## Usage
- Swagger: [doc](doc/CopernicusAPI_swagger.yaml)
- Postman: 
    - [collection](doc/Copernicus%20API.postman_collection.json)
    - [env](doc/Copernicus%20API.postman_environment.json)

## Tasks
- Integrate to an SQLite in memory db
    - save which requested files are currently available
    - mark files as being actively retrieved to remove race conditions
    - OAuth for production
    

