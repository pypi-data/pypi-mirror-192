"""
The act of expressing a consistency of opinion with the object. An agent agrees to/about an object (a proposition, topic or theme) with participants.

https://schema.org/AgreeAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AgreeActionInheritedProperties(TypedDict):
    """The act of expressing a consistency of opinion with the object. An agent agrees to/about an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/AgreeAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class AgreeActionProperties(TypedDict):
    """The act of expressing a consistency of opinion with the object. An agent agrees to/about an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/AgreeAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#AgreeActionInheritedPropertiesTd = AgreeActionInheritedProperties()
#AgreeActionPropertiesTd = AgreeActionProperties()


class AllProperties(AgreeActionInheritedProperties , AgreeActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AgreeActionProperties, AgreeActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AgreeAction"
    return model
    

AgreeAction = create_schema_org_model()