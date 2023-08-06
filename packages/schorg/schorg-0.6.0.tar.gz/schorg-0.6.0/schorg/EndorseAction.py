"""
An agent approves/certifies/likes/supports/sanctions an object.

https://schema.org/EndorseAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EndorseActionInheritedProperties(TypedDict):
    """An agent approves/certifies/likes/supports/sanctions an object.

    References:
        https://schema.org/EndorseAction
    Note:
        Model Depth 5
    Attributes:
    """

    


class EndorseActionProperties(TypedDict):
    """An agent approves/certifies/likes/supports/sanctions an object.

    References:
        https://schema.org/EndorseAction
    Note:
        Model Depth 5
    Attributes:
        endorsee: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The person/organization being supported.
    """

    endorsee: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#EndorseActionInheritedPropertiesTd = EndorseActionInheritedProperties()
#EndorseActionPropertiesTd = EndorseActionProperties()


class AllProperties(EndorseActionInheritedProperties , EndorseActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EndorseActionProperties, EndorseActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EndorseAction"
    return model
    

EndorseAction = create_schema_org_model()