# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
Riocloud Reader — Universal Content Reader
Combines x-reader and DeepReader
"""

__version__ = "1.0.0"
__author__ = "Riocloud"

from .reader import Reader
from .schema import UnifiedContent, SourceType

__all__ = ["Reader", "UnifiedContent", "SourceType"]
