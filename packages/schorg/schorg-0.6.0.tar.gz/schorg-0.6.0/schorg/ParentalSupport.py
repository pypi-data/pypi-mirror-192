"""
ParentalSupport: this is a benefit for parental support.

https://schema.org/ParentalSupport
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ParentalSupportInheritedProperties(TypedDict):
    """ParentalSupport: this is a benefit for parental support.

    References:
        https://schema.org/ParentalSupport
    Note:
        Model Depth 5
    Attributes:
    """

    


class ParentalSupportProperties(TypedDict):
    """ParentalSupport: this is a benefit for parental support.

    References:
        https://schema.org/ParentalSupport
    Note:
        Model Depth 5
    Attributes:
    """

    

#ParentalSupportInheritedPropertiesTd = ParentalSupportInheritedProperties()
#ParentalSupportPropertiesTd = ParentalSupportProperties()


class AllProperties(ParentalSupportInheritedProperties , ParentalSupportProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ParentalSupportProperties, ParentalSupportInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ParentalSupport"
    return model
    

ParentalSupport = create_schema_org_model()