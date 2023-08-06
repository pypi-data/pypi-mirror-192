"""
Data Preparation in Vantage with Views
============================
tdprepview (speak T-D-prep-view) is a package for fitting
and transforming re-usable data preparation pipelines that are
saved in view definitions. Hence, no other permanent database objects
are required.
"""

__author__ = """Martin Hillebrand"""
__email__ = 'martin.hillebrand@teradata.com'
__version__ = '0.1.3'

from ._pipeline import Pipeline
from .preprocessing._preprocessing import (
    Impute,
    ImputeText,
    TryCast,
    Scale,
    CutOff,
    FixedWidthBinning,
    ThresholdBinarizer,
    ListBinarizer,
    VariableWidthBinning,
    LabelEncoder,
    CustomTransformer
)

__all__ = [
    "Pipeline",
    "Impute",
    "ImputeText",
    "TryCast",
    "Scale",
    "CutOff",
    "FixedWidthBinning",
    "ThresholdBinarizer",
    "ListBinarizer",
    "VariableWidthBinning",
    "LabelEncoder",
    "CustomTransformer"
]
