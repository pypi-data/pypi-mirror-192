"""
The act of inserting at the beginning if an ordered collection.

https://schema.org/PrependAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PrependActionInheritedProperties(TypedDict):
    """The act of inserting at the beginning if an ordered collection.

    References:
        https://schema.org/PrependAction
    Note:
        Model Depth 6
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PrependActionProperties(TypedDict):
    """The act of inserting at the beginning if an ordered collection.

    References:
        https://schema.org/PrependAction
    Note:
        Model Depth 6
    Attributes:
    """

    

#PrependActionInheritedPropertiesTd = PrependActionInheritedProperties()
#PrependActionPropertiesTd = PrependActionProperties()


class AllProperties(PrependActionInheritedProperties , PrependActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PrependActionProperties, PrependActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PrependAction"
    return model
    

PrependAction = create_schema_org_model()