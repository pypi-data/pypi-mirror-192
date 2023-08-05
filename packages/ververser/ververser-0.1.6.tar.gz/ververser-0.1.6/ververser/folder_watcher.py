import os.path
from pathlib import Path


class FolderWatcher:

    def __init__( self, folder_path: Path, postfix : str ):
        self.folder_path = folder_path
        self.postfix = postfix
        self.last_seen_time_modified = None

    def get_last_time_modified( self ):
        all_file_paths = self.folder_path.rglob(f'*{self.postfix}')
        all_modification_times = [ os.path.getmtime( file_path ) for file_path in all_file_paths ]
        modification_time = max( all_modification_times )
        return modification_time

    def is_folder_updated( self ) -> bool:
        last_time_modified = self.get_last_time_modified()
        is_updated = False
        if last_time_modified != self.last_seen_time_modified:
            is_updated = True
            self.last_seen_time_modified = last_time_modified
            print(f'Folder was updated for extension {self.postfix}! - {self.folder_path} - Timestamp: {self.last_seen_time_modified}')
        return is_updated
