"""
The act of conveying information to another person via a communication medium (instrument) such as speech, email, or telephone conversation.

https://schema.org/CommunicateAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CommunicateActionInheritedProperties(TypedDict):
    """The act of conveying information to another person via a communication medium (instrument) such as speech, email, or telephone conversation.

    References:
        https://schema.org/CommunicateAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class CommunicateActionProperties(TypedDict):
    """The act of conveying information to another person via a communication medium (instrument) such as speech, email, or telephone conversation.

    References:
        https://schema.org/CommunicateAction
    Note:
        Model Depth 4
    Attributes:
        about: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The subject matter of the content.
        recipient: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The participant who is at the receiving end of the action.
        language: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The language used on this action.
        inLanguage: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The language of the content or performance or used in an action. Please use one of the language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also [[availableLanguage]].
    """

    about: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    recipient: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    language: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    inLanguage: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#CommunicateActionInheritedPropertiesTd = CommunicateActionInheritedProperties()
#CommunicateActionPropertiesTd = CommunicateActionProperties()


class AllProperties(CommunicateActionInheritedProperties , CommunicateActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CommunicateActionProperties, CommunicateActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CommunicateAction"
    return model
    

CommunicateAction = create_schema_org_model()