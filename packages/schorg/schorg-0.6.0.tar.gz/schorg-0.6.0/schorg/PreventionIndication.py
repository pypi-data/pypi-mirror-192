"""
An indication for preventing an underlying condition, symptom, etc.

https://schema.org/PreventionIndication
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PreventionIndicationInheritedProperties(TypedDict):
    """An indication for preventing an underlying condition, symptom, etc.

    References:
        https://schema.org/PreventionIndication
    Note:
        Model Depth 4
    Attributes:
    """

    


class PreventionIndicationProperties(TypedDict):
    """An indication for preventing an underlying condition, symptom, etc.

    References:
        https://schema.org/PreventionIndication
    Note:
        Model Depth 4
    Attributes:
    """

    

#PreventionIndicationInheritedPropertiesTd = PreventionIndicationInheritedProperties()
#PreventionIndicationPropertiesTd = PreventionIndicationProperties()


class AllProperties(PreventionIndicationInheritedProperties , PreventionIndicationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PreventionIndicationProperties, PreventionIndicationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PreventionIndication"
    return model
    

PreventionIndication = create_schema_org_model()