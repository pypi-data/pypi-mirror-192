"""
Withdrawn.

https://schema.org/Withdrawn
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WithdrawnInheritedProperties(TypedDict):
    """Withdrawn.

    References:
        https://schema.org/Withdrawn
    Note:
        Model Depth 6
    Attributes:
    """

    


class WithdrawnProperties(TypedDict):
    """Withdrawn.

    References:
        https://schema.org/Withdrawn
    Note:
        Model Depth 6
    Attributes:
    """

    

#WithdrawnInheritedPropertiesTd = WithdrawnInheritedProperties()
#WithdrawnPropertiesTd = WithdrawnProperties()


class AllProperties(WithdrawnInheritedProperties , WithdrawnProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WithdrawnProperties, WithdrawnInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Withdrawn"
    return model
    

Withdrawn = create_schema_org_model()