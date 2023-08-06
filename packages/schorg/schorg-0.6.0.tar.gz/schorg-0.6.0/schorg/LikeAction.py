"""
The act of expressing a positive sentiment about the object. An agent likes an object (a proposition, topic or theme) with participants.

https://schema.org/LikeAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LikeActionInheritedProperties(TypedDict):
    """The act of expressing a positive sentiment about the object. An agent likes an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/LikeAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class LikeActionProperties(TypedDict):
    """The act of expressing a positive sentiment about the object. An agent likes an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/LikeAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#LikeActionInheritedPropertiesTd = LikeActionInheritedProperties()
#LikeActionPropertiesTd = LikeActionProperties()


class AllProperties(LikeActionInheritedProperties , LikeActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LikeActionProperties, LikeActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LikeAction"
    return model
    

LikeAction = create_schema_org_model()