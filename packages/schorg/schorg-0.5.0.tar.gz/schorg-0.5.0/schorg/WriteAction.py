"""
The act of authoring written creative content.

https://schema.org/WriteAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WriteActionInheritedProperties(TypedDict):
    """The act of authoring written creative content.

    References:
        https://schema.org/WriteAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class WriteActionProperties(TypedDict):
    """The act of authoring written creative content.

    References:
        https://schema.org/WriteAction
    Note:
        Model Depth 4
    Attributes:
        language: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The language used on this action.
        inLanguage: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The language of the content or performance or used in an action. Please use one of the language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also [[availableLanguage]].
    """

    language: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    inLanguage: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#WriteActionInheritedPropertiesTd = WriteActionInheritedProperties()
#WriteActionPropertiesTd = WriteActionProperties()


class AllProperties(WriteActionInheritedProperties , WriteActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WriteActionProperties, WriteActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WriteAction"
    return model
    

WriteAction = create_schema_org_model()