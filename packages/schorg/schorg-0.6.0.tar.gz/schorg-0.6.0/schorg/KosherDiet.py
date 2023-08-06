"""
A diet conforming to Jewish dietary practices.

https://schema.org/KosherDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class KosherDietInheritedProperties(TypedDict):
    """A diet conforming to Jewish dietary practices.

    References:
        https://schema.org/KosherDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class KosherDietProperties(TypedDict):
    """A diet conforming to Jewish dietary practices.

    References:
        https://schema.org/KosherDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#KosherDietInheritedPropertiesTd = KosherDietInheritedProperties()
#KosherDietPropertiesTd = KosherDietProperties()


class AllProperties(KosherDietInheritedProperties , KosherDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[KosherDietProperties, KosherDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "KosherDiet"
    return model
    

KosherDiet = create_schema_org_model()