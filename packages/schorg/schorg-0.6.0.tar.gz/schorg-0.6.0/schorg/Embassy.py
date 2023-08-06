"""
An embassy.

https://schema.org/Embassy
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EmbassyInheritedProperties(TypedDict):
    """An embassy.

    References:
        https://schema.org/Embassy
    Note:
        Model Depth 5
    Attributes:
    """

    


class EmbassyProperties(TypedDict):
    """An embassy.

    References:
        https://schema.org/Embassy
    Note:
        Model Depth 5
    Attributes:
    """

    

#EmbassyInheritedPropertiesTd = EmbassyInheritedProperties()
#EmbassyPropertiesTd = EmbassyProperties()


class AllProperties(EmbassyInheritedProperties , EmbassyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EmbassyProperties, EmbassyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Embassy"
    return model
    

Embassy = create_schema_org_model()