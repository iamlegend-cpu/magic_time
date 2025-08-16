# -*- coding: utf-8 -*-
# PyInstaller hook for pyannote.audio

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all pyannote.audio submodules
hiddenimports = collect_submodules('pyannote.audio')

# Collect all data files
datas = collect_data_files('pyannote.audio')

# Add specific pyannote.audio dependencies that are commonly used
hiddenimports += [
    'pyannote.audio',
    'pyannote.audio.core',
    'pyannote.audio.core.pipeline',
    'pyannote.audio.core.model',
    'pyannote.audio.core.io',
    'pyannote.audio.core.task',
    'pyannote.audio.pipelines',
    'pyannote.audio.pipelines.voice_activity_detection',
    'pyannote.audio.pipelines.speaker_diarization',
    'pyannote.audio.pipelines.overlapped_speech_detection',
    'pyannote.audio.pipelines.utils',
    'pyannote.audio.tasks',
    'pyannote.audio.tasks.segmentation',
    'pyannote.audio.tasks.segmentation.voice_activity_detection',
    'pyannote.audio.tasks.segmentation.speaker_diarization',
    'pyannote.audio.tasks.segmentation.overlapped_speech_detection',
    'pyannote.audio.tasks.segmentation.mixins',
    'pyannote.audio.tasks.embedding',
    'pyannote.audio.tasks.embedding.mixins',
    'pyannote.audio.tasks.separation',
    'pyannote.audio.models',
    'pyannote.audio.utils',
    'pyannote.audio.utils.signal',
    'pyannote.audio.utils.metric',
    'pyannote.audio.utils.permutation',
    'pyannote.audio.utils.random',
    'pyannote.audio.utils.protocol',
    'pyannote.audio.utils.preview',
    'pyannote.audio.utils.preprocessors',
    'pyannote.audio.utils.multi_task',
    'pyannote.audio.torchmetrics',
    'pyannote.audio.torchmetrics.audio',
    'pyannote.audio.torchmetrics.functional',
    'pyannote.audio.torchmetrics.classification',
    'pyannote.audio.torchmetrics.regression',
    'pyannote.audio.torchmetrics.clustering',
    'pyannote.audio.torchmetrics.embedding',
    'pyannote.audio.torchmetrics.segmentation',
    'pyannote.audio.torchmetrics.separation',
]

# Add pyannote base modules
hiddenimports += [
    'pyannote',
    'pyannote.core',
    'pyannote.core.utils',
    'pyannote.core.utils.helper',
    'pyannote.core.feature',
    'pyannote.database',
    'pyannote.database.protocol',
    'pyannote.database.protocol.speaker_diarization',
    'pyannote.database.protocol.segmentation',
    'pyannote.pipeline',
    'pyannote.pipeline.experiment',
]
