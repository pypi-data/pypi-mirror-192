"""
The act of dressing oneself in clothing.

https://schema.org/WearAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearActionInheritedProperties(TypedDict):
    """The act of dressing oneself in clothing.

    References:
        https://schema.org/WearAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class WearActionProperties(TypedDict):
    """The act of dressing oneself in clothing.

    References:
        https://schema.org/WearAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#WearActionInheritedPropertiesTd = WearActionInheritedProperties()
#WearActionPropertiesTd = WearActionProperties()


class AllProperties(WearActionInheritedProperties , WearActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearActionProperties, WearActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearAction"
    return model
    

WearAction = create_schema_org_model()