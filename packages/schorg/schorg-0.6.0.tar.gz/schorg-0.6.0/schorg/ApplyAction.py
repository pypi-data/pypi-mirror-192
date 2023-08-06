"""
The act of registering to an organization/service without the guarantee to receive it.Related actions:* [[RegisterAction]]: Unlike RegisterAction, ApplyAction has no guarantees that the application will be accepted.

https://schema.org/ApplyAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ApplyActionInheritedProperties(TypedDict):
    """The act of registering to an organization/service without the guarantee to receive it.Related actions:* [[RegisterAction]]: Unlike RegisterAction, ApplyAction has no guarantees that the application will be accepted.

    References:
        https://schema.org/ApplyAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class ApplyActionProperties(TypedDict):
    """The act of registering to an organization/service without the guarantee to receive it.Related actions:* [[RegisterAction]]: Unlike RegisterAction, ApplyAction has no guarantees that the application will be accepted.

    References:
        https://schema.org/ApplyAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#ApplyActionInheritedPropertiesTd = ApplyActionInheritedProperties()
#ApplyActionPropertiesTd = ApplyActionProperties()


class AllProperties(ApplyActionInheritedProperties , ApplyActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ApplyActionProperties, ApplyActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ApplyAction"
    return model
    

ApplyAction = create_schema_org_model()