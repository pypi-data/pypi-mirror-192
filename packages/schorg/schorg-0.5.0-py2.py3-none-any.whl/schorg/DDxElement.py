"""
An alternative, closely-related condition typically considered later in the differential diagnosis process along with the signs that are used to distinguish it.

https://schema.org/DDxElement
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DDxElementInheritedProperties(TypedDict):
    """An alternative, closely-related condition typically considered later in the differential diagnosis process along with the signs that are used to distinguish it.

    References:
        https://schema.org/DDxElement
    Note:
        Model Depth 4
    Attributes:
    """

    


class DDxElementProperties(TypedDict):
    """An alternative, closely-related condition typically considered later in the differential diagnosis process along with the signs that are used to distinguish it.

    References:
        https://schema.org/DDxElement
    Note:
        Model Depth 4
    Attributes:
        distinguishingSign: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): One of a set of signs and symptoms that can be used to distinguish this diagnosis from others in the differential diagnosis.
        diagnosis: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): One or more alternative conditions considered in the differential diagnosis process as output of a diagnosis process.
    """

    distinguishingSign: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    diagnosis: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#DDxElementInheritedPropertiesTd = DDxElementInheritedProperties()
#DDxElementPropertiesTd = DDxElementProperties()


class AllProperties(DDxElementInheritedProperties , DDxElementProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DDxElementProperties, DDxElementInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DDxElement"
    return model
    

DDxElement = create_schema_org_model()