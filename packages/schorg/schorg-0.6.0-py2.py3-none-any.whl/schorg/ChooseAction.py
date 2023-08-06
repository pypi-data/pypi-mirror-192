"""
The act of expressing a preference from a set of options or a large or unbounded set of choices/options.

https://schema.org/ChooseAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ChooseActionInheritedProperties(TypedDict):
    """The act of expressing a preference from a set of options or a large or unbounded set of choices/options.

    References:
        https://schema.org/ChooseAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class ChooseActionProperties(TypedDict):
    """The act of expressing a preference from a set of options or a large or unbounded set of choices/options.

    References:
        https://schema.org/ChooseAction
    Note:
        Model Depth 4
    Attributes:
        option: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A sub property of object. The options subject to this action.
        actionOption: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A sub property of object. The options subject to this action.
    """

    option: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    actionOption: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#ChooseActionInheritedPropertiesTd = ChooseActionInheritedProperties()
#ChooseActionPropertiesTd = ChooseActionProperties()


class AllProperties(ChooseActionInheritedProperties , ChooseActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ChooseActionProperties, ChooseActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ChooseAction"
    return model
    

ChooseAction = create_schema_org_model()