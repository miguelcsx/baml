# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.
#
# BAML version: 0.0.1
# Generated Date: 2023-10-30 19:47:25.045780 -07:00
# Generated by: vbv

from ...._impl.deserializer import register_deserializer
from enum import Enum


@register_deserializer()
class Sentiment(str, Enum):
    SAD = "SAD"
    HAPPY = "HAPPY"
