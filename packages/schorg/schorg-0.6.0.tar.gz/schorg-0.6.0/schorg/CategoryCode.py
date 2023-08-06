"""
A Category Code.

https://schema.org/CategoryCode
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CategoryCodeInheritedProperties(TypedDict):
    """A Category Code.

    References:
        https://schema.org/CategoryCode
    Note:
        Model Depth 4
    Attributes:
        inDefinedTermSet: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A [[DefinedTermSet]] that contains this term.
        termCode: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A code that identifies this [[DefinedTerm]] within a [[DefinedTermSet]]
    """

    inDefinedTermSet: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    termCode: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class CategoryCodeProperties(TypedDict):
    """A Category Code.

    References:
        https://schema.org/CategoryCode
    Note:
        Model Depth 4
    Attributes:
        codeValue: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A short textual code that uniquely identifies the value.
        inCodeSet: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A [[CategoryCodeSet]] that contains this category code.
    """

    codeValue: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    inCodeSet: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    

#CategoryCodeInheritedPropertiesTd = CategoryCodeInheritedProperties()
#CategoryCodePropertiesTd = CategoryCodeProperties()


class AllProperties(CategoryCodeInheritedProperties , CategoryCodeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CategoryCodeProperties, CategoryCodeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CategoryCode"
    return model
    

CategoryCode = create_schema_org_model()