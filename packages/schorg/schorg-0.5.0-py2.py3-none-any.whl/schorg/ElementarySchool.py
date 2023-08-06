"""
An elementary school.

https://schema.org/ElementarySchool
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ElementarySchoolInheritedProperties(TypedDict):
    """An elementary school.

    References:
        https://schema.org/ElementarySchool
    Note:
        Model Depth 4
    Attributes:
        alumni: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Alumni of an organization.
    """

    alumni: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ElementarySchoolProperties(TypedDict):
    """An elementary school.

    References:
        https://schema.org/ElementarySchool
    Note:
        Model Depth 4
    Attributes:
    """

    

#ElementarySchoolInheritedPropertiesTd = ElementarySchoolInheritedProperties()
#ElementarySchoolPropertiesTd = ElementarySchoolProperties()


class AllProperties(ElementarySchoolInheritedProperties , ElementarySchoolProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ElementarySchoolProperties, ElementarySchoolInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ElementarySchool"
    return model
    

ElementarySchool = create_schema_org_model()