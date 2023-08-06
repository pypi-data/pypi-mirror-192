"""
An enumeration of several kinds of Map.

https://schema.org/MapCategoryType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MapCategoryTypeInheritedProperties(TypedDict):
    """An enumeration of several kinds of Map.

    References:
        https://schema.org/MapCategoryType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MapCategoryTypeProperties(TypedDict):
    """An enumeration of several kinds of Map.

    References:
        https://schema.org/MapCategoryType
    Note:
        Model Depth 4
    Attributes:
    """

    

#MapCategoryTypeInheritedPropertiesTd = MapCategoryTypeInheritedProperties()
#MapCategoryTypePropertiesTd = MapCategoryTypeProperties()


class AllProperties(MapCategoryTypeInheritedProperties , MapCategoryTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MapCategoryTypeProperties, MapCategoryTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MapCategoryType"
    return model
    

MapCategoryType = create_schema_org_model()