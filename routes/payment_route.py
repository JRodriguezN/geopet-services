from fastapi import APIRouter
from pydantic import BaseModel
import stripe
from config import STRIPE_API_KEY

payment_route = APIRouter()

stripe.api_key = STRIPE_API_KEY

class PagoPublicacion(BaseModel):
    amount: float  # Monto en centavos
    currency: str  # Moneda, por ejemplo 'usd'

@payment_route.post("/create-payment-intent")
async def crear_pago_publicacion(pago: PagoPublicacion):
    try:
        amount = int(pago.amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=pago.currency,
            payment_method_types=["card"],
        )
        return {"client_secret": intent.client_secret, "id": intent.id}
    except Exception as e:
        return {"error": str(e)}


@payment_route.post("/crear-recompensa")
async def crear_pago_recompensa(pago: PagoPublicacion):
    amount = int(pago.amount * 100)
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=pago.currency,
        automatic_payment_methods={"enabled": True},
    )
    return {"client_secret": intent.client_secret, "id": intent.id}
