"""
The act of consuming written content.

https://schema.org/ReadAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReadActionInheritedProperties(TypedDict):
    """The act of consuming written content.

    References:
        https://schema.org/ReadAction
    Note:
        Model Depth 4
    Attributes:
        actionAccessibilityRequirement: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A set of requirements that must be fulfilled in order to perform an Action. If more than one value is specified, fulfilling one set of requirements will allow the Action to be performed.
        expectsAcceptanceOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An Offer which must be accepted before the user can perform the Action. For example, the user may need to buy a movie before being able to watch it.
    """

    actionAccessibilityRequirement: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    expectsAcceptanceOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ReadActionProperties(TypedDict):
    """The act of consuming written content.

    References:
        https://schema.org/ReadAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#ReadActionInheritedPropertiesTd = ReadActionInheritedProperties()
#ReadActionPropertiesTd = ReadActionProperties()


class AllProperties(ReadActionInheritedProperties , ReadActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReadActionProperties, ReadActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReadAction"
    return model
    

ReadAction = create_schema_org_model()