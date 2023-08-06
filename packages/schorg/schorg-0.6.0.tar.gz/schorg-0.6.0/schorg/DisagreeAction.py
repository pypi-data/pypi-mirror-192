"""
The act of expressing a difference of opinion with the object. An agent disagrees to/about an object (a proposition, topic or theme) with participants.

https://schema.org/DisagreeAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DisagreeActionInheritedProperties(TypedDict):
    """The act of expressing a difference of opinion with the object. An agent disagrees to/about an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/DisagreeAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class DisagreeActionProperties(TypedDict):
    """The act of expressing a difference of opinion with the object. An agent disagrees to/about an object (a proposition, topic or theme) with participants.

    References:
        https://schema.org/DisagreeAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#DisagreeActionInheritedPropertiesTd = DisagreeActionInheritedProperties()
#DisagreeActionPropertiesTd = DisagreeActionProperties()


class AllProperties(DisagreeActionInheritedProperties , DisagreeActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DisagreeActionProperties, DisagreeActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DisagreeAction"
    return model
    

DisagreeAction = create_schema_org_model()