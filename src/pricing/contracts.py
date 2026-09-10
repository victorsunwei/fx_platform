from abc import ABC, abstractmethod

class PricingContract(ABC):
    @abstractmethod
    def price(self, request: dict) -> float:
        pass
