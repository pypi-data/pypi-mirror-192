"""
The basic data types such as Integers, Strings, etc.

https://schema.org/DataType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DataTypeInheritedProperties(TypedDict):
    """The basic data types such as Integers, Strings, etc.

    References:
        https://schema.org/DataType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DataTypeProperties(TypedDict):
    """The basic data types such as Integers, Strings, etc.

    References:
        https://schema.org/DataType
    Note:
        Model Depth 4
    Attributes:
    """

    

#DataTypeInheritedPropertiesTd = DataTypeInheritedProperties()
#DataTypePropertiesTd = DataTypeProperties()


class AllProperties(DataTypeInheritedProperties , DataTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DataTypeProperties, DataTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DataType"
    return model
    

DataType = create_schema_org_model()