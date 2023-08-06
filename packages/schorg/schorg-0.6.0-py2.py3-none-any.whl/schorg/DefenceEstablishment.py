"""
A defence establishment, such as an army or navy base.

https://schema.org/DefenceEstablishment
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DefenceEstablishmentInheritedProperties(TypedDict):
    """A defence establishment, such as an army or navy base.

    References:
        https://schema.org/DefenceEstablishment
    Note:
        Model Depth 5
    Attributes:
    """

    


class DefenceEstablishmentProperties(TypedDict):
    """A defence establishment, such as an army or navy base.

    References:
        https://schema.org/DefenceEstablishment
    Note:
        Model Depth 5
    Attributes:
    """

    

#DefenceEstablishmentInheritedPropertiesTd = DefenceEstablishmentInheritedProperties()
#DefenceEstablishmentPropertiesTd = DefenceEstablishmentProperties()


class AllProperties(DefenceEstablishmentInheritedProperties , DefenceEstablishmentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DefenceEstablishmentProperties, DefenceEstablishmentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DefenceEstablishment"
    return model
    

DefenceEstablishment = create_schema_org_model()