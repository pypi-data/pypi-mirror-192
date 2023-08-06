"""
The act of organizing tasks/objects/events by associating resources to it.

https://schema.org/AllocateAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AllocateActionInheritedProperties(TypedDict):
    """The act of organizing tasks/objects/events by associating resources to it.

    References:
        https://schema.org/AllocateAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class AllocateActionProperties(TypedDict):
    """The act of organizing tasks/objects/events by associating resources to it.

    References:
        https://schema.org/AllocateAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#AllocateActionInheritedPropertiesTd = AllocateActionInheritedProperties()
#AllocateActionPropertiesTd = AllocateActionProperties()


class AllProperties(AllocateActionInheritedProperties , AllocateActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AllocateActionProperties, AllocateActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AllocateAction"
    return model
    

AllocateAction = create_schema_org_model()