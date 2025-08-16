# -*- coding: utf-8 -*-
# PyInstaller hook for Lightning and Lightning Fabric

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all Lightning submodules (only if available)
hiddenimports = []
datas = []

try:
    # Collect all Lightning submodules
    hiddenimports.extend(collect_submodules('lightning'))
    datas.extend(collect_data_files('lightning'))
except ImportError:
    pass

try:
    hiddenimports.extend(collect_submodules('lightning_fabric'))
    datas.extend(collect_data_files('lightning_fabric'))
except ImportError:
    pass

try:
    hiddenimports.extend(collect_submodules('lightning.pytorch'))
    datas.extend(collect_data_files('lightning.pytorch'))
except ImportError:
    pass

# Add specific Lightning dependencies (only if available)
lightning_modules = [
    'lightning.fabric',
    'lightning.fabric.accelerators',
    'lightning.fabric.callbacks',
    'lightning.fabric.loggers',
    'lightning.fabric.plugins',
    'lightning.fabric.strategies',
    'lightning.fabric.utilities',
    'lightning.pytorch.accelerators',
    'lightning.pytorch.callbacks',
    'lightning.pytorch.core',
    'lightning.pytorch.demos',
    'lightning.pytorch.loggers',
    'lightning.pytorch.plugins',
    'lightning.pytorch.strategies',
    'lightning.pytorch.trainer',
    'lightning.pytorch.utilities',
    'lightning.utilities',
    'lightning.utilities.argparse',
    'lightning.utilities.cloud_io',
    'lightning.utilities.data',
    'lightning.utilities.device_dtype_mixin',
    'lightning.utilities.distributed',
    'lightning.utilities.enums',
    'lightning.utilities.exceptions',
    'lightning.utilities.imports',
    'lightning.utilities.memory',
    'lightning.utilities.model_helpers',
    'lightning.utilities.parsing',
    'lightning.utilities.seed',
    'lightning.utilities.warnings',
]

# Test each module before adding to hiddenimports
for module in lightning_modules:
    try:
        __import__(module)
        hiddenimports.append(module)
    except ImportError:
        # Skip modules that can't be imported
        pass
