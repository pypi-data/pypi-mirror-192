"""
A value indicating a special usage of a car, e.g. commercial rental, driving school, or as a taxi.

https://schema.org/CarUsageType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CarUsageTypeInheritedProperties(TypedDict):
    """A value indicating a special usage of a car, e.g. commercial rental, driving school, or as a taxi.

    References:
        https://schema.org/CarUsageType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class CarUsageTypeProperties(TypedDict):
    """A value indicating a special usage of a car, e.g. commercial rental, driving school, or as a taxi.

    References:
        https://schema.org/CarUsageType
    Note:
        Model Depth 4
    Attributes:
    """

    

#CarUsageTypeInheritedPropertiesTd = CarUsageTypeInheritedProperties()
#CarUsageTypePropertiesTd = CarUsageTypeProperties()


class AllProperties(CarUsageTypeInheritedProperties , CarUsageTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CarUsageTypeProperties, CarUsageTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CarUsageType"
    return model
    

CarUsageType = create_schema_org_model()