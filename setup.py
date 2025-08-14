"""
Setup script voor Magic Time Studio
Installeert het package in development mode
"""

from setuptools import setup, find_packages

setup(
    name="magic_time_studio",
    version="3.0.0",
    description="Magic Time Studio - Audio/Video Processing Tool",
    author="Magic Time Studio Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.0.0",
        "numpy",
        "librosa",
        # Torch wordt handmatig geïnstalleerd met CUDA support
        # "torch",  # Verwijderd - gebruik torch==2.5.1+cu121
        "whisperx",  # Enige ondersteunde Whisper implementatie
        "soundfile",
        "av",
        "requests",
        "numba",
        "llvmlite",
        "ctranslate2",
        "tokenizers",
        "pynvml",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
