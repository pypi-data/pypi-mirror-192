"""
Represents the suggested retail price ("SRP") of an offered product.

https://schema.org/SRP
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SRPInheritedProperties(TypedDict):
    """Represents the suggested retail price ("SRP") of an offered product.

    References:
        https://schema.org/SRP
    Note:
        Model Depth 5
    Attributes:
    """

    


class SRPProperties(TypedDict):
    """Represents the suggested retail price ("SRP") of an offered product.

    References:
        https://schema.org/SRP
    Note:
        Model Depth 5
    Attributes:
    """

    

#SRPInheritedPropertiesTd = SRPInheritedProperties()
#SRPPropertiesTd = SRPProperties()


class AllProperties(SRPInheritedProperties , SRPProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SRPProperties, SRPInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SRP"
    return model
    

SRP = create_schema_org_model()