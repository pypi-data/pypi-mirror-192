"""
A medical device used for therapeutic purposes.

https://schema.org/Therapeutic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TherapeuticInheritedProperties(TypedDict):
    """A medical device used for therapeutic purposes.

    References:
        https://schema.org/Therapeutic
    Note:
        Model Depth 6
    Attributes:
    """

    


class TherapeuticProperties(TypedDict):
    """A medical device used for therapeutic purposes.

    References:
        https://schema.org/Therapeutic
    Note:
        Model Depth 6
    Attributes:
    """

    

#TherapeuticInheritedPropertiesTd = TherapeuticInheritedProperties()
#TherapeuticPropertiesTd = TherapeuticProperties()


class AllProperties(TherapeuticInheritedProperties , TherapeuticProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TherapeuticProperties, TherapeuticInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Therapeutic"
    return model
    

Therapeutic = create_schema_org_model()