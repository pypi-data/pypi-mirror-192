"""
The act of expressing a preference from a fixed/finite/structured set of choices/options.

https://schema.org/VoteAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VoteActionInheritedProperties(TypedDict):
    """The act of expressing a preference from a fixed/finite/structured set of choices/options.

    References:
        https://schema.org/VoteAction
    Note:
        Model Depth 5
    Attributes:
        option: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A sub property of object. The options subject to this action.
        actionOption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A sub property of object. The options subject to this action.
    """

    option: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    actionOption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class VoteActionProperties(TypedDict):
    """The act of expressing a preference from a fixed/finite/structured set of choices/options.

    References:
        https://schema.org/VoteAction
    Note:
        Model Depth 5
    Attributes:
        candidate: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of object. The candidate subject of this action.
    """

    candidate: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#VoteActionInheritedPropertiesTd = VoteActionInheritedProperties()
#VoteActionPropertiesTd = VoteActionProperties()


class AllProperties(VoteActionInheritedProperties , VoteActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VoteActionProperties, VoteActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "VoteAction"
    return model
    

VoteAction = create_schema_org_model()