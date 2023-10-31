# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.
#
# BAML version: 0.0.1
# Generated Date: 2023-10-30 19:47:25.045780 -07:00
# Generated by: vbv

from ..._impl.functions import BaseBAMLFunction
from ..types.classes.cls_inputtype import InputType
from ..types.classes.cls_inputtype2 import InputType2
from ..types.classes.cls_outputtype import OutputType
from ..types.enums.enm_sentiment import Sentiment
from typing import Protocol, runtime_checkable


@runtime_checkable
class IFooB(Protocol):
    """
    This is the interface for a function.

    Args:
        arg: InputType

    Returns:
        OutputType
    """

    async def __call__(self, arg: InputType, /) -> OutputType:
        ...


class IBAMLFooB(BaseBAMLFunction[OutputType]):
    def __init__(self) -> None:
        super().__init__(
            "FooB",
            IFooB,
            ["FooImpl"],
        )

BAMLFooB = IBAMLFooB()

__all__ = [ "BAMLFooB" ]
