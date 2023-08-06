"""
The act of marrying a person.

https://schema.org/MarryAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MarryActionInheritedProperties(TypedDict):
    """The act of marrying a person.

    References:
        https://schema.org/MarryAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class MarryActionProperties(TypedDict):
    """The act of marrying a person.

    References:
        https://schema.org/MarryAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#MarryActionInheritedPropertiesTd = MarryActionInheritedProperties()
#MarryActionPropertiesTd = MarryActionProperties()


class AllProperties(MarryActionInheritedProperties , MarryActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MarryActionProperties, MarryActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MarryAction"
    return model
    

MarryAction = create_schema_org_model()