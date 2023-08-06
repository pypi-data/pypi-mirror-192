"""
A set of Category Code values.

https://schema.org/CategoryCodeSet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CategoryCodeSetInheritedProperties(TypedDict):
    """A set of Category Code values.

    References:
        https://schema.org/CategoryCodeSet
    Note:
        Model Depth 4
    Attributes:
        hasDefinedTerm: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A Defined Term contained in this term set.
    """

    hasDefinedTerm: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class CategoryCodeSetProperties(TypedDict):
    """A set of Category Code values.

    References:
        https://schema.org/CategoryCodeSet
    Note:
        Model Depth 4
    Attributes:
        hasCategoryCode: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A Category code contained in this code set.
    """

    hasCategoryCode: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#CategoryCodeSetInheritedPropertiesTd = CategoryCodeSetInheritedProperties()
#CategoryCodeSetPropertiesTd = CategoryCodeSetProperties()


class AllProperties(CategoryCodeSetInheritedProperties , CategoryCodeSetProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CategoryCodeSetProperties, CategoryCodeSetInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CategoryCodeSet"
    return model
    

CategoryCodeSet = create_schema_org_model()