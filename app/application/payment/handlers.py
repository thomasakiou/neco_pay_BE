from typing import List
from app.application.payment.commands import CreatePaymentCommand
from app.domain.payment import Payment
from app.application.interfaces import IPaymentRepository
from app.application.payment.dtos import PaymentDTO

class CreatePaymentHandler:
    def __init__(self, repository: IPaymentRepository):
        self.repository = repository

    def handle(self, command: CreatePaymentCommand) -> PaymentDTO:
        # Create domain entity (Simplified, normally ID generation or complex logic here)
        # We pass a dummy ID/Status as Repository/DB will handle creation mostly
        
        # NOTE: In a pure DDD, the ID might be generated before persistence, or by the DB.
        # We treat 'Payment' as a pure Data Class here for transport, but logic resides here.
        
        payment = Payment(
            id=0, # Placeholder
            amount=command.amount,
            currency=command.currency,
            status="pending",
            description=command.description,
            created_at=None # Placeholder
        )
        
        saved_payment = self.repository.save(payment)
        return PaymentDTO(
            id=saved_payment.id,
            amount=saved_payment.amount,
            currency=saved_payment.currency,
            status=saved_payment.status,
            description=saved_payment.description,
            created_at=saved_payment.created_at
        )

class GetPaymentHandler:
    def __init__(self, repository: IPaymentRepository):
        self.repository = repository

    def handle(self, payment_id: int) -> PaymentDTO:
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
        return PaymentDTO(
           id=payment.id,
           amount=payment.amount,
           currency=payment.currency,
           status=payment.status,
           description=payment.description,
           created_at=payment.created_at
        )
        
class ListPaymentsHandler:
    def __init__(self, repository: IPaymentRepository):
        self.repository = repository
        
    def handle(self, skip: int, limit: int) -> List[PaymentDTO]:
        payments = self.repository.list(skip, limit)
        return [
            PaymentDTO(
                id=p.id,
                amount=p.amount,
                currency=p.currency,
                status=p.status,
                description=p.description,
                created_at=p.created_at
            ) for p in payments
        ]
