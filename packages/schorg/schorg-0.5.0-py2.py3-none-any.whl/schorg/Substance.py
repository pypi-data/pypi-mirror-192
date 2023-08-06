"""
Any matter of defined composition that has discrete existence, whose origin may be biological, mineral or chemical.

https://schema.org/Substance
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SubstanceInheritedProperties(TypedDict):
    """Any matter of defined composition that has discrete existence, whose origin may be biological, mineral or chemical.

    References:
        https://schema.org/Substance
    Note:
        Model Depth 3
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
    


class SubstanceProperties(TypedDict):
    """Any matter of defined composition that has discrete existence, whose origin may be biological, mineral or chemical.

    References:
        https://schema.org/Substance
    Note:
        Model Depth 3
    Attributes:
        activeIngredient: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An active ingredient, typically chemical compounds and/or biologic substances.
        maximumIntake: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Recommended intake of this supplement for a given population as defined by a specific recommending authority.
    """

    activeIngredient: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    maximumIntake: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#SubstanceInheritedPropertiesTd = SubstanceInheritedProperties()
#SubstancePropertiesTd = SubstanceProperties()


class AllProperties(SubstanceInheritedProperties , SubstanceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SubstanceProperties, SubstanceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Substance"
    return model
    

Substance = create_schema_org_model()