# -*- coding: utf-8 -*-
# PyInstaller hook for SpeechBrain

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all SpeechBrain submodules
hiddenimports = collect_submodules('speechbrain')

# Collect all data files
datas = collect_data_files('speechbrain')

# Add specific SpeechBrain dependencies
hiddenimports += [
    'speechbrain.dataio',
    'speechbrain.utils',
    'speechbrain.processing',
    'speechbrain.lobes',
    'speechbrain.core',
    'speechbrain.pretrained',
    'speechbrain.decoders',
    'speechbrain.lm',
    'speechbrain.nnet',
    'speechbrain.speechbrain',
]
