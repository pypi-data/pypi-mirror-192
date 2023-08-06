"""
GovernmentBenefitsType enumerates several kinds of government benefits to support the COVID-19 situation. Note that this structure may not capture all benefits offered.

https://schema.org/GovernmentBenefitsType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GovernmentBenefitsTypeInheritedProperties(TypedDict):
    """GovernmentBenefitsType enumerates several kinds of government benefits to support the COVID-19 situation. Note that this structure may not capture all benefits offered.

    References:
        https://schema.org/GovernmentBenefitsType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class GovernmentBenefitsTypeProperties(TypedDict):
    """GovernmentBenefitsType enumerates several kinds of government benefits to support the COVID-19 situation. Note that this structure may not capture all benefits offered.

    References:
        https://schema.org/GovernmentBenefitsType
    Note:
        Model Depth 4
    Attributes:
    """

    

#GovernmentBenefitsTypeInheritedPropertiesTd = GovernmentBenefitsTypeInheritedProperties()
#GovernmentBenefitsTypePropertiesTd = GovernmentBenefitsTypeProperties()


class AllProperties(GovernmentBenefitsTypeInheritedProperties , GovernmentBenefitsTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GovernmentBenefitsTypeProperties, GovernmentBenefitsTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GovernmentBenefitsType"
    return model
    

GovernmentBenefitsType = create_schema_org_model()