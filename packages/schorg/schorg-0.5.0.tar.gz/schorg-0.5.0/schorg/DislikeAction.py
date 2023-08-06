"""
The act of expressing a negative sentiment about the object. An agent dislikes an object (a proposition, topic or theme) with participants.

https://schema.org/DislikeAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DislikeActionInheritedProperties(TypedDict):
    """The act of expressing a negative sentiment about the object. An agent dislikes an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/DislikeAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class DislikeActionProperties(TypedDict):
    """The act of expressing a negative sentiment about the object. An agent dislikes an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/DislikeAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#DislikeActionInheritedPropertiesTd = DislikeActionInheritedProperties()
#DislikeActionPropertiesTd = DislikeActionProperties()


class AllProperties(DislikeActionInheritedProperties , DislikeActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DislikeActionProperties, DislikeActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DislikeAction"
    return model
    

DislikeAction = create_schema_org_model()