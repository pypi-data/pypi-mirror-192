"""
A description of an action that is supported.

https://schema.org/PotentialActionStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PotentialActionStatusInheritedProperties(TypedDict):
    """A description of an action that is supported.

    References:
        https://schema.org/PotentialActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    


class PotentialActionStatusProperties(TypedDict):
    """A description of an action that is supported.

    References:
        https://schema.org/PotentialActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    

#PotentialActionStatusInheritedPropertiesTd = PotentialActionStatusInheritedProperties()
#PotentialActionStatusPropertiesTd = PotentialActionStatusProperties()


class AllProperties(PotentialActionStatusInheritedProperties , PotentialActionStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PotentialActionStatusProperties, PotentialActionStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PotentialActionStatus"
    return model
    

PotentialActionStatus = create_schema_org_model()