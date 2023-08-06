"""
Something in medical science that pertains to infectious diseases, i.e. caused by bacterial, viral, fungal or parasitic infections.

https://schema.org/Infectious
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InfectiousInheritedProperties(TypedDict):
    """Something in medical science that pertains to infectious diseases, i.e. caused by bacterial, viral, fungal or parasitic infections.

    References:
        https://schema.org/Infectious
    Note:
        Model Depth 6
    Attributes:
    """

    


class InfectiousProperties(TypedDict):
    """Something in medical science that pertains to infectious diseases, i.e. caused by bacterial, viral, fungal or parasitic infections.

    References:
        https://schema.org/Infectious
    Note:
        Model Depth 6
    Attributes:
    """

    

#InfectiousInheritedPropertiesTd = InfectiousInheritedProperties()
#InfectiousPropertiesTd = InfectiousProperties()


class AllProperties(InfectiousInheritedProperties , InfectiousProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InfectiousProperties, InfectiousInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Infectious"
    return model
    

Infectious = create_schema_org_model()