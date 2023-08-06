from enum import Enum


class PispgatewayPaymentContextPaymentContextCode(str, Enum):
    PARTYTOPARTY = "PARTYTOPARTY"
    ECOMMERCEGOODS = "ECOMMERCEGOODS"
    Bill_Payment = "BillPayment"
    BILLPAYMENT = "BILLPAYMENT"
    ECOMMERCESERVICES = "ECOMMERCESERVICES"
    OTHER = "OTHER"
    Party_To_Party = "PartyToParty"
    Ecommerce_Goods = "EcommerceGoods"
    Ecommerce_Services = "EcommerceServices"
    Other = "Other"

    def __str__(self) -> str:
        return str(self.value)
