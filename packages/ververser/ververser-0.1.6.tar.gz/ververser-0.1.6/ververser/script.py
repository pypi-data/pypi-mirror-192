from pathlib import Path
from runpy import run_path

from ververser.global_game_window import get_global_game_window


class Script:

    def __init__( self, file_path : Path ):
        self.file_path = file_path
        self.data_module = run_path( str( file_path ) )

    def __getattr__( self, name ):
        return self.data_module.get( name )


def load_script( script_path : Path ) -> Script:
    return Script( script_path )


def import_script( script_path : str ) -> Script:
    return get_global_game_window().asset_manager.load( script_path )
