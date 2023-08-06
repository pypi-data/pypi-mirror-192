"""
The act of stopping or deactivating a device or application (e.g. stopping a timer or turning off a flashlight).

https://schema.org/DeactivateAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DeactivateActionInheritedProperties(TypedDict):
    """The act of stopping or deactivating a device or application (e.g. stopping a timer or turning off a flashlight).

    References:
        https://schema.org/DeactivateAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class DeactivateActionProperties(TypedDict):
    """The act of stopping or deactivating a device or application (e.g. stopping a timer or turning off a flashlight).

    References:
        https://schema.org/DeactivateAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#DeactivateActionInheritedPropertiesTd = DeactivateActionInheritedProperties()
#DeactivateActionPropertiesTd = DeactivateActionProperties()


class AllProperties(DeactivateActionInheritedProperties , DeactivateActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DeactivateActionProperties, DeactivateActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DeactivateAction"
    return model
    

DeactivateAction = create_schema_org_model()