import os

from copernicus_api.misc import settings


class FileStatus:

    def __init__(self,directory):
        self._files = {f:True for f in os.listdir(directory) if
                       os.path.isfile(directory + os.sep + f) and not f.startswith(".") and f.endswith(".grib")}

    def add_file(self, file_name):
        self._files[file_name]=False

    def mark_available(self,file_name,directory):
        if os.path.isfile(directory + os.sep + file_name):
            self._files[file_name]=True

    def get_available_files(self):
        return [f for f in self._files if self.is_available(f) is True]

    def in_files(self,file_name):
        return file_name in self._files

    def is_available(self,file_name):
        if self.in_files(file_name):
            return self._files[file_name]
        else:
            return None

file_status = FileStatus(settings.directory)
