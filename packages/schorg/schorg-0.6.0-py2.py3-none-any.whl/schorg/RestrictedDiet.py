"""
A diet restricted to certain foods or preparations for cultural, religious, health or lifestyle reasons. 

https://schema.org/RestrictedDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RestrictedDietInheritedProperties(TypedDict):
    """A diet restricted to certain foods or preparations for cultural, religious, health or lifestyle reasons. 

    References:
        https://schema.org/RestrictedDiet
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class RestrictedDietProperties(TypedDict):
    """A diet restricted to certain foods or preparations for cultural, religious, health or lifestyle reasons. 

    References:
        https://schema.org/RestrictedDiet
    Note:
        Model Depth 4
    Attributes:
    """

    

#RestrictedDietInheritedPropertiesTd = RestrictedDietInheritedProperties()
#RestrictedDietPropertiesTd = RestrictedDietProperties()


class AllProperties(RestrictedDietInheritedProperties , RestrictedDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RestrictedDietProperties, RestrictedDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RestrictedDiet"
    return model
    

RestrictedDiet = create_schema_org_model()