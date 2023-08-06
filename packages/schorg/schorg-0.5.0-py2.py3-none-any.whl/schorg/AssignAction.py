"""
The act of allocating an action/event/task to some destination (someone or something).

https://schema.org/AssignAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AssignActionInheritedProperties(TypedDict):
    """The act of allocating an action/event/task to some destination (someone or something).

    References:
        https://schema.org/AssignAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class AssignActionProperties(TypedDict):
    """The act of allocating an action/event/task to some destination (someone or something).

    References:
        https://schema.org/AssignAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#AssignActionInheritedPropertiesTd = AssignActionInheritedProperties()
#AssignActionPropertiesTd = AssignActionProperties()


class AllProperties(AssignActionInheritedProperties , AssignActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AssignActionProperties, AssignActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AssignAction"
    return model
    

AssignAction = create_schema_org_model()