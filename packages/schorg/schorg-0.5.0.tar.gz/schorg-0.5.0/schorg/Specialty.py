"""
Any branch of a field in which people typically develop specific expertise, usually after significant study, time, and effort.

https://schema.org/Specialty
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SpecialtyInheritedProperties(TypedDict):
    """Any branch of a field in which people typically develop specific expertise, usually after significant study, time, and effort.

    References:
        https://schema.org/Specialty
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class SpecialtyProperties(TypedDict):
    """Any branch of a field in which people typically develop specific expertise, usually after significant study, time, and effort.

    References:
        https://schema.org/Specialty
    Note:
        Model Depth 4
    Attributes:
    """

    

#SpecialtyInheritedPropertiesTd = SpecialtyInheritedProperties()
#SpecialtyPropertiesTd = SpecialtyProperties()


class AllProperties(SpecialtyInheritedProperties , SpecialtyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SpecialtyProperties, SpecialtyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Specialty"
    return model
    

Specialty = create_schema_org_model()