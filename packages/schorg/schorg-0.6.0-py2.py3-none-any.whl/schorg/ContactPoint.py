"""
A contact point&#x2014;for example, a Customer Complaints department.

https://schema.org/ContactPoint
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ContactPointInheritedProperties(TypedDict):
    """A contact point&#x2014;for example, a Customer Complaints department.

    References:
        https://schema.org/ContactPoint
    Note:
        Model Depth 4
    Attributes:
    """

    


class ContactPointProperties(TypedDict):
    """A contact point&#x2014;for example, a Customer Complaints department.

    References:
        https://schema.org/ContactPoint
    Note:
        Model Depth 4
    Attributes:
        serviceArea: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The geographic area where the service is provided.
        availableLanguage: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A language someone may use with or at the item, service or place. Please use one of the language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also [[inLanguage]].
        productSupported: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The product or service this support contact point is related to (such as product support for a particular product line). This can be a specific product or product line (e.g. "iPhone") or a general category of products or services (e.g. "smartphones").
        areaServed: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The geographic area where a service or offered item is provided.
        contactOption: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An option available on this contact point (e.g. a toll-free number or support for hearing-impaired callers).
        email: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Email address.
        contactType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A person or organization can have different contact points, for different purposes. For example, a sales contact point, a PR contact point and so on. This property is used to specify the kind of contact point.
        hoursAvailable: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The hours during which this service or contact is available.
        faxNumber: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The fax number.
        telephone: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The telephone number.
    """

    serviceArea: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    availableLanguage: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    productSupported: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    areaServed: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    contactOption: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    email: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    contactType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    hoursAvailable: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    faxNumber: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    telephone: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#ContactPointInheritedPropertiesTd = ContactPointInheritedProperties()
#ContactPointPropertiesTd = ContactPointProperties()


class AllProperties(ContactPointInheritedProperties , ContactPointProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ContactPointProperties, ContactPointInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ContactPoint"
    return model
    

ContactPoint = create_schema_org_model()