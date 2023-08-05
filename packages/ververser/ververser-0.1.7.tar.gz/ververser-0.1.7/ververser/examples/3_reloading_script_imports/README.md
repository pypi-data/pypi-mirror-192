# Ververser Example 3: Reloading Script Imports

The python import system is relatively complex. 
It does some clever caching, but does not allow us to easily unload modules. 
This is a problem when loading modules in ververser;
When reloading a script, not all logic might be refreshed due to caching. 
Ververser therefore wraps scripts as objects when importing them. 
When reloading a script, the imported script objects will be removed by the garbage collection, 
and replaced with new instances, effectively doing a proper reload of the module. 

Note that ververser intentionally does not try to do anything clever for reloading modules. 
Ververser is not aware of dependencies between scripts/modules. 
Simply, when a python file is changed, the entire program as served by ververser is re-initialised. 
This might mean your entire program reboots while you only meant to change a minor thing.
This is something that might be tackled in later versions of ververser.

Also Note that the note above, talks specifically about reloading scripts. 
Reloading other types of assets will never result in a full reload. 
