"""
A financial product for the loaning of an amount of money, or line of credit, under agreed terms and charges.

https://schema.org/LoanOrCredit
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LoanOrCreditInheritedProperties(TypedDict):
    """A financial product for the loaning of an amount of money, or line of credit, under agreed terms and charges.

    References:
        https://schema.org/LoanOrCredit
    Note:
        Model Depth 5
    Attributes:
        annualPercentageRate: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The annual rate that is charged for borrowing (or made by investing), expressed as a single percentage number that represents the actual yearly cost of funds over the term of a loan. This includes any fees or additional costs associated with the transaction.
        interestRate: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The interest rate, charged or paid, applicable to the financial product. Note: This is different from the calculated annualPercentageRate.
        feesAndCommissionsSpecification: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Description of fees, commissions, and other terms applied either to a class of financial product, or by a financial service organization.
    """

    annualPercentageRate: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    interestRate: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    feesAndCommissionsSpecification: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class LoanOrCreditProperties(TypedDict):
    """A financial product for the loaning of an amount of money, or line of credit, under agreed terms and charges.

    References:
        https://schema.org/LoanOrCredit
    Note:
        Model Depth 5
    Attributes:
        requiredCollateral: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Assets required to secure loan or credit repayments. It may take form of third party pledge, goods, financial instruments (cash, securities, etc.)
        loanType: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): The type of a loan or credit.
        currency: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The currency in which the monetary amount is expressed.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
        renegotiableLoan: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Whether the terms for payment of interest can be renegotiated during the life of the loan.
        gracePeriod: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The period of time after any due date that the borrower has to fulfil its obligations before a default (failure to pay) is deemed to have occurred.
        loanTerm: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The duration of the loan or credit agreement.
        amount: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The amount of money.
        loanRepaymentForm: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A form of paying back money previously borrowed from a lender. Repayment usually takes the form of periodic payments that normally include part principal plus interest in each payment.
        recourseLoan: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): The only way you get the money back in the event of default is the security. Recourse is where you still have the opportunity to go back to the borrower for the rest of the money.
    """

    requiredCollateral: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    loanType: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    currency: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    renegotiableLoan: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    gracePeriod: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    loanTerm: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    amount: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    loanRepaymentForm: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    recourseLoan: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    

#LoanOrCreditInheritedPropertiesTd = LoanOrCreditInheritedProperties()
#LoanOrCreditPropertiesTd = LoanOrCreditProperties()


class AllProperties(LoanOrCreditInheritedProperties , LoanOrCreditProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LoanOrCreditProperties, LoanOrCreditInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LoanOrCredit"
    return model
    

LoanOrCredit = create_schema_org_model()