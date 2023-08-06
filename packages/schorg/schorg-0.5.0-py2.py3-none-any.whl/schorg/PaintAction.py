"""
The act of producing a painting, typically with paint and canvas as instruments.

https://schema.org/PaintAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaintActionInheritedProperties(TypedDict):
    """The act of producing a painting, typically with paint and canvas as instruments.

    References:
        https://schema.org/PaintAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class PaintActionProperties(TypedDict):
    """The act of producing a painting, typically with paint and canvas as instruments.

    References:
        https://schema.org/PaintAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#PaintActionInheritedPropertiesTd = PaintActionInheritedProperties()
#PaintActionPropertiesTd = PaintActionProperties()


class AllProperties(PaintActionInheritedProperties , PaintActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaintActionProperties, PaintActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaintAction"
    return model
    

PaintAction = create_schema_org_model()