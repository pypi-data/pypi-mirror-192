"""
A subclass of Role used to describe roles within organizations.

https://schema.org/OrganizationRole
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrganizationRoleInheritedProperties(TypedDict):
    """A subclass of Role used to describe roles within organizations.

    References:
        https://schema.org/OrganizationRole
    Note:
        Model Depth 4
    Attributes:
        roleName: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A role played, performed or filled by a person or organization. For example, the team of creators for a comic book might fill the roles named 'inker', 'penciller', and 'letterer'; or an athlete in a SportsTeam might play in the position named 'Quarterback'.
        namedPosition: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A position played, performed or filled by a person or organization, as part of an organization. For example, an athlete in a SportsTeam might play in the position named 'Quarterback'.
        startDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
        endDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
    """

    roleName: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    namedPosition: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    startDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    endDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    


class OrganizationRoleProperties(TypedDict):
    """A subclass of Role used to describe roles within organizations.

    References:
        https://schema.org/OrganizationRole
    Note:
        Model Depth 4
    Attributes:
        numberedPosition: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): A number associated with a role in an organization, for example, the number on an athlete's jersey.
    """

    numberedPosition: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#OrganizationRoleInheritedPropertiesTd = OrganizationRoleInheritedProperties()
#OrganizationRolePropertiesTd = OrganizationRoleProperties()


class AllProperties(OrganizationRoleInheritedProperties , OrganizationRoleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrganizationRoleProperties, OrganizationRoleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrganizationRole"
    return model
    

OrganizationRole = create_schema_org_model()