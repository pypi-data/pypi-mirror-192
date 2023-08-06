"""
The act of forming a personal connection with someone (object) mutually/bidirectionally/symmetrically.Related actions:* [[FollowAction]]: Unlike FollowAction, BefriendAction implies that the connection is reciprocal.

https://schema.org/BefriendAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BefriendActionInheritedProperties(TypedDict):
    """The act of forming a personal connection with someone (object) mutually/bidirectionally/symmetrically.Related actions:* [[FollowAction]]: Unlike FollowAction, BefriendAction implies that the connection is reciprocal.

    References:
        https://schema.org/BefriendAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class BefriendActionProperties(TypedDict):
    """The act of forming a personal connection with someone (object) mutually/bidirectionally/symmetrically.Related actions:* [[FollowAction]]: Unlike FollowAction, BefriendAction implies that the connection is reciprocal.

    References:
        https://schema.org/BefriendAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#BefriendActionInheritedPropertiesTd = BefriendActionInheritedProperties()
#BefriendActionPropertiesTd = BefriendActionProperties()


class AllProperties(BefriendActionInheritedProperties , BefriendActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BefriendActionProperties, BefriendActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BefriendAction"
    return model
    

BefriendAction = create_schema_org_model()