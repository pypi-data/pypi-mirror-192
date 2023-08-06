"""
Studies carried out on pre-existing data (usually from 'snapshot' surveys), such as that collected by the Census Bureau. Sometimes called Prevalence Studies.

https://schema.org/CrossSectional
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CrossSectionalInheritedProperties(TypedDict):
    """Studies carried out on pre-existing data (usually from 'snapshot' surveys), such as that collected by the Census Bureau. Sometimes called Prevalence Studies.

    References:
        https://schema.org/CrossSectional
    Note:
        Model Depth 6
    Attributes:
    """

    


class CrossSectionalProperties(TypedDict):
    """Studies carried out on pre-existing data (usually from 'snapshot' surveys), such as that collected by the Census Bureau. Sometimes called Prevalence Studies.

    References:
        https://schema.org/CrossSectional
    Note:
        Model Depth 6
    Attributes:
    """

    

#CrossSectionalInheritedPropertiesTd = CrossSectionalInheritedProperties()
#CrossSectionalPropertiesTd = CrossSectionalProperties()


class AllProperties(CrossSectionalInheritedProperties , CrossSectionalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CrossSectionalProperties, CrossSectionalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CrossSectional"
    return model
    

CrossSectional = create_schema_org_model()