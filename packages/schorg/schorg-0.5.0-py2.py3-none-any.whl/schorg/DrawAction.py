"""
The act of producing a visual/graphical representation of an object, typically with a pen/pencil and paper as instruments.

https://schema.org/DrawAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrawActionInheritedProperties(TypedDict):
    """The act of producing a visual/graphical representation of an object, typically with a pen/pencil and paper as instruments.

    References:
        https://schema.org/DrawAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class DrawActionProperties(TypedDict):
    """The act of producing a visual/graphical representation of an object, typically with a pen/pencil and paper as instruments.

    References:
        https://schema.org/DrawAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#DrawActionInheritedPropertiesTd = DrawActionInheritedProperties()
#DrawActionPropertiesTd = DrawActionProperties()


class AllProperties(DrawActionInheritedProperties , DrawActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrawActionProperties, DrawActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrawAction"
    return model
    

DrawAction = create_schema_org_model()