"""
Beauty salon.

https://schema.org/BeautySalon
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BeautySalonInheritedProperties(TypedDict):
    """Beauty salon.

    References:
        https://schema.org/BeautySalon
    Note:
        Model Depth 5
    Attributes:
    """

    


class BeautySalonProperties(TypedDict):
    """Beauty salon.

    References:
        https://schema.org/BeautySalon
    Note:
        Model Depth 5
    Attributes:
    """

    

#BeautySalonInheritedPropertiesTd = BeautySalonInheritedProperties()
#BeautySalonPropertiesTd = BeautySalonProperties()


class AllProperties(BeautySalonInheritedProperties , BeautySalonProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BeautySalonProperties, BeautySalonInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BeautySalon"
    return model
    

BeautySalon = create_schema_org_model()