"""
The most generic type of entity related to health and the practice of medicine.

https://schema.org/MedicalEntity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalEntityInheritedProperties(TypedDict):
    """The most generic type of entity related to health and the practice of medicine.

    References:
        https://schema.org/MedicalEntity
    Note:
        Model Depth 2
    Attributes:
        potentialAction: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Indicates a potential Action, which describes an idealized action in which this thing would play an 'object' role.
        mainEntityOfPage: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See [background notes](/docs/datamodel.html#mainEntityBackground) for details.
        subjectOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A CreativeWork or Event about this Thing.
        url: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): URL of the item.
        alternateName: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An alias for the item.
        sameAs: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): URL of a reference Web page that unambiguously indicates the item's identity. E.g. the URL of the item's Wikipedia page, Wikidata entry, or official website.
        description: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A description of the item.
        disambiguatingDescription: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation.
        identifier: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): The identifier property represents any kind of identifier for any kind of [[Thing]], such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See [background notes](/docs/datamodel.html#identifierBg) for more details.        
        image: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): An image of the item. This can be a [[URL]] or a fully described [[ImageObject]].
        name: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The name of the item.
        additionalType: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the 'typeof' attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally.
    """

    potentialAction: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    mainEntityOfPage: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    subjectOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    url: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    alternateName: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    sameAs: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    description: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    disambiguatingDescription: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    identifier: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    image: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    name: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    additionalType: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class MedicalEntityProperties(TypedDict):
    """The most generic type of entity related to health and the practice of medicine.

    References:
        https://schema.org/MedicalEntity
    Note:
        Model Depth 2
    Attributes:
        recognizingAuthority: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): If applicable, the organization that officially recognizes this entity as part of its endorsed system of medicine.
        relevantSpecialty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): If applicable, a medical specialty in which this entity is relevant.
        medicineSystem: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The system of medicine that includes this MedicalEntity, for example 'evidence-based', 'homeopathic', 'chiropractic', etc.
        funding: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A [[Grant]] that directly or indirectly provide funding or sponsorship for this item. See also [[ownershipFundingInfo]].
        legalStatus: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The drug or supplement's legal status, including any controlled substance schedules that apply.
        study: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical study or trial related to this entity.
        guideline: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical guideline related to this entity.
        code: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical code for the entity, taken from a controlled vocabulary or ontology such as ICD-9, DiseasesDB, MeSH, SNOMED-CT, RxNorm, etc.
    """

    recognizingAuthority: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    relevantSpecialty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    medicineSystem: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    funding: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    legalStatus: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    study: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    guideline: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    code: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MedicalEntityInheritedPropertiesTd = MedicalEntityInheritedProperties()
#MedicalEntityPropertiesTd = MedicalEntityProperties()


class AllProperties(MedicalEntityInheritedProperties , MedicalEntityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalEntityProperties, MedicalEntityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalEntity"
    return model
    

MedicalEntity = create_schema_org_model()