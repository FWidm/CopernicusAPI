from copernicus_api.misc.file_status import file_status

def list_files():
    return file_status.get_available_files()