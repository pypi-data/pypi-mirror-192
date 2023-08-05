from pathlib import Path
from typing import Any, Callable

from ververser.reloading_asset import ReloadingAsset, ReloadStatus
from ververser.main_script import load_main_script, MainScript
from ververser.folder_watcher import FolderWatcher
from ververser.script import load_script


AssetLoaderType = Callable[ [ Path ], Any ]

EXPECTED_MAIN_SCRIPT_NAME = Path( 'main.py' )


class AssetManager:

    def __init__( self, asset_folder_path : Path, game_window ):
        self.asset_folder_path = asset_folder_path
        self.game_window = game_window

        self.script_watcher = FolderWatcher( asset_folder_path, '.py' )

        self.asset_loaders : list[ tuple[ str, AssetLoaderType ] ] = []
        self.assets : list[ ReloadingAsset ] = []

        self.register_asset_loader( '.py', load_script )

    def make_asset_path_complete( self, asset_path : Path ) -> Path:
        return self.asset_folder_path / asset_path

    def register_asset_loader( self, postfix : str, f_load_asset : AssetLoaderType ) -> None:
        self.asset_loaders.append( ( postfix, f_load_asset ) )

    def load_main_script( self ) -> MainScript:
        absolute_asset_path = self.make_asset_path_complete( EXPECTED_MAIN_SCRIPT_NAME )
        assert self.exists( absolute_asset_path ), f'Could not load asset. File path: "{EXPECTED_MAIN_SCRIPT_NAME}"'
        main_script = load_main_script( absolute_asset_path, self.game_window )
        return main_script

    def get_asset_loader_for_file( self, file_path : Path ) -> AssetLoaderType:
        # reverse search through all registered loaders
        # this way. newest registered loaders overrule older ones
        for postfix, asset_loader in reversed( self.asset_loaders ):
            if str( file_path ).endswith( postfix ):
                return asset_loader
        assert False, f'No asset loader found for file_path: "{file_path}". Known loaders: {self.asset_loaders}'

    def try_reload( self ) -> ReloadStatus:
        # first check if any script file is outdated
        if self.script_watcher.is_folder_updated():
            self.game_window.init()

        # if scripts are not outdated, also check the other types of assets
        overall_reload_status = ReloadStatus.NOT_CHANGED
        for reloading_asset in self.assets:
            reloading_asset.try_reload()
            reload_status = reloading_asset.reload_status
            if reload_status == ReloadStatus.RELOADED:
                overall_reload_status = ReloadStatus.RELOADED
            if reload_status == ReloadStatus.FAILED:
                return ReloadStatus.FAILED
        return overall_reload_status

    def exists( self, asset_path ) -> bool:
        complete_asset_path = self.make_asset_path_complete( asset_path )
        return complete_asset_path.is_file()

    def load( self, asset_path ) -> ReloadingAsset:
        absolute_asset_path = self.make_asset_path_complete( asset_path.strip() )
        assert self.exists( absolute_asset_path ), f'Could not load asset. File path: "{asset_path}"'
        asset_loader = self.get_asset_loader_for_file( absolute_asset_path )
        reloading_asset = ReloadingAsset(
            f_load_asset = lambda path : asset_loader( path ),
            file_path = absolute_asset_path
        )
        self.assets.append( reloading_asset )
        reloading_asset.try_reload()
        return reloading_asset
