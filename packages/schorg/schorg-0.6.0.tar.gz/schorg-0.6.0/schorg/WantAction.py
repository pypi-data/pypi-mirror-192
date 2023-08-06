"""
The act of expressing a desire about the object. An agent wants an object.

https://schema.org/WantAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WantActionInheritedProperties(TypedDict):
    """The act of expressing a desire about the object. An agent wants an object.

    References:
        https://schema.org/WantAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class WantActionProperties(TypedDict):
    """The act of expressing a desire about the object. An agent wants an object.

    References:
        https://schema.org/WantAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#WantActionInheritedPropertiesTd = WantActionInheritedProperties()
#WantActionPropertiesTd = WantActionProperties()


class AllProperties(WantActionInheritedProperties , WantActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WantActionProperties, WantActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WantAction"
    return model
    

WantAction = create_schema_org_model()