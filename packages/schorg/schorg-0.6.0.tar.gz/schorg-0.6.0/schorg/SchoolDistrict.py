"""
A School District is an administrative area for the administration of schools.

https://schema.org/SchoolDistrict
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SchoolDistrictInheritedProperties(TypedDict):
    """A School District is an administrative area for the administration of schools.

    References:
        https://schema.org/SchoolDistrict
    Note:
        Model Depth 4
    Attributes:
    """

    


class SchoolDistrictProperties(TypedDict):
    """A School District is an administrative area for the administration of schools.

    References:
        https://schema.org/SchoolDistrict
    Note:
        Model Depth 4
    Attributes:
    """

    

#SchoolDistrictInheritedPropertiesTd = SchoolDistrictInheritedProperties()
#SchoolDistrictPropertiesTd = SchoolDistrictProperties()


class AllProperties(SchoolDistrictInheritedProperties , SchoolDistrictProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SchoolDistrictProperties, SchoolDistrictInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SchoolDistrict"
    return model
    

SchoolDistrict = create_schema_org_model()