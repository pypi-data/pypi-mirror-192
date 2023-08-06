"""
A notary.

https://schema.org/Notary
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NotaryInheritedProperties(TypedDict):
    """A notary.

    References:
        https://schema.org/Notary
    Note:
        Model Depth 5
    Attributes:
    """

    


class NotaryProperties(TypedDict):
    """A notary.

    References:
        https://schema.org/Notary
    Note:
        Model Depth 5
    Attributes:
    """

    

#NotaryInheritedPropertiesTd = NotaryInheritedProperties()
#NotaryPropertiesTd = NotaryProperties()


class AllProperties(NotaryInheritedProperties , NotaryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NotaryProperties, NotaryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Notary"
    return model
    

Notary = create_schema_org_model()