git submodule add https://github.com/PARK4139/pk_system.git assets/pk_system
echo Setting pk_system submodule to read-only...
attrib +R "assets\pk_system\*.*" /S
git config submodule."assets/pk_system".ignore all
echo Done.
timeout 10