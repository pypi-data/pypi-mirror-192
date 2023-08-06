"""
The act of granting permission to an object.

https://schema.org/AuthorizeAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AuthorizeActionInheritedProperties(TypedDict):
    """The act of granting permission to an object.

    References:
        https://schema.org/AuthorizeAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class AuthorizeActionProperties(TypedDict):
    """The act of granting permission to an object.

    References:
        https://schema.org/AuthorizeAction
    Note:
        Model Depth 5
    Attributes:
        recipient: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The participant who is at the receiving end of the action.
    """

    recipient: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#AuthorizeActionInheritedPropertiesTd = AuthorizeActionInheritedProperties()
#AuthorizeActionPropertiesTd = AuthorizeActionProperties()


class AllProperties(AuthorizeActionInheritedProperties , AuthorizeActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AuthorizeActionProperties, AuthorizeActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AuthorizeAction"
    return model
    

AuthorizeAction = create_schema_org_model()