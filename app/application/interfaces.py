from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.payment import Payment

class IPaymentRepository(ABC):
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Payment]:
        pass

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        pass
