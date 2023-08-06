"""
Represents the manufacturer suggested retail price ("MSRP") of an offered product.

https://schema.org/MSRP
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MSRPInheritedProperties(TypedDict):
    """Represents the manufacturer suggested retail price ("MSRP") of an offered product.

    References:
        https://schema.org/MSRP
    Note:
        Model Depth 5
    Attributes:
    """

    


class MSRPProperties(TypedDict):
    """Represents the manufacturer suggested retail price ("MSRP") of an offered product.

    References:
        https://schema.org/MSRP
    Note:
        Model Depth 5
    Attributes:
    """

    

#MSRPInheritedPropertiesTd = MSRPInheritedProperties()
#MSRPPropertiesTd = MSRPProperties()


class AllProperties(MSRPInheritedProperties , MSRPProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MSRPProperties, MSRPInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MSRP"
    return model
    

MSRP = create_schema_org_model()