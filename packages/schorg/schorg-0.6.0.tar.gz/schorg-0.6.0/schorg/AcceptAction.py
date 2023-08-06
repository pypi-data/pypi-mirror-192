"""
The act of committing to/adopting an object.Related actions:* [[RejectAction]]: The antonym of AcceptAction.

https://schema.org/AcceptAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AcceptActionInheritedProperties(TypedDict):
    """The act of committing to/adopting an object.Related actions:* [[RejectAction]]: The antonym of AcceptAction.

    References:
        https://schema.org/AcceptAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class AcceptActionProperties(TypedDict):
    """The act of committing to/adopting an object.Related actions:* [[RejectAction]]: The antonym of AcceptAction.

    References:
        https://schema.org/AcceptAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#AcceptActionInheritedPropertiesTd = AcceptActionInheritedProperties()
#AcceptActionPropertiesTd = AcceptActionProperties()


class AllProperties(AcceptActionInheritedProperties , AcceptActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AcceptActionProperties, AcceptActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AcceptAction"
    return model
    

AcceptAction = create_schema_org_model()