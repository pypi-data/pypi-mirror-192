"""
Something relating to or practicing dermatology.

https://schema.org/Dermatologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DermatologicInheritedProperties(TypedDict):
    """Something relating to or practicing dermatology.

    References:
        https://schema.org/Dermatologic
    Note:
        Model Depth 6
    Attributes:
    """

    


class DermatologicProperties(TypedDict):
    """Something relating to or practicing dermatology.

    References:
        https://schema.org/Dermatologic
    Note:
        Model Depth 6
    Attributes:
    """

    

#DermatologicInheritedPropertiesTd = DermatologicInheritedProperties()
#DermatologicPropertiesTd = DermatologicProperties()


class AllProperties(DermatologicInheritedProperties , DermatologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DermatologicProperties, DermatologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Dermatologic"
    return model
    

Dermatologic = create_schema_org_model()