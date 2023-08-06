"""
The act of applying an object to its intended purpose.

https://schema.org/UseAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UseActionInheritedProperties(TypedDict):
    """The act of applying an object to its intended purpose.

    References:
        https://schema.org/UseAction
    Note:
        Model Depth 4
    Attributes:
        actionAccessibilityRequirement: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A set of requirements that must be fulfilled in order to perform an Action. If more than one value is specified, fulfilling one set of requirements will allow the Action to be performed.
        expectsAcceptanceOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An Offer which must be accepted before the user can perform the Action. For example, the user may need to buy a movie before being able to watch it.
    """

    actionAccessibilityRequirement: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    expectsAcceptanceOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class UseActionProperties(TypedDict):
    """The act of applying an object to its intended purpose.

    References:
        https://schema.org/UseAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#UseActionInheritedPropertiesTd = UseActionInheritedProperties()
#UseActionPropertiesTd = UseActionProperties()


class AllProperties(UseActionInheritedProperties , UseActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UseActionProperties, UseActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UseAction"
    return model
    

UseAction = create_schema_org_model()