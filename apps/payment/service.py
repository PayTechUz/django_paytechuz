from django.conf import settings

from paytechuz.gateways.payme import PaymeGateway
from paytechuz.gateways.click import ClickGateway
from paytechuz.gateways.atmos import AtmosGateway

from paytechuz.integrations.django.models import PaymentTransaction

from apps.payment.models import Invoice


class PaymentService:
    def create_payment(self, order_id, amount, provider):
        """
        Generate payment link based on order's payment type.
        """
        paytechuz_settings = settings.PAYTECHUZ

        if provider == 'payme':
            payme = PaymeGateway(
                payme_id=paytechuz_settings['PAYME']['PAYME_ID'],
                payme_key=paytechuz_settings['PAYME']['PAYME_KEY'],
                is_test_mode=paytechuz_settings['PAYME']['IS_TEST_MODE'],
            )
            return payme.create_payment(
                id=order_id,
                amount=float(amount),
                return_url="https://example.com/return"
            )

        if provider == 'click':
            click = ClickGateway(
                service_id=paytechuz_settings['CLICK']['SERVICE_ID'],
                merchant_id=paytechuz_settings['CLICK']['MERCHANT_ID'],
                merchant_user_id=paytechuz_settings['CLICK']['MERCHANT_USER_ID'],
                secret_key=paytechuz_settings['CLICK']['SECRET_KEY'],
                is_test_mode=paytechuz_settings['CLICK']['IS_TEST_MODE']
            )
            result = click.create_payment(
                id=order_id,
                amount=float(amount),
                return_url="https://example.com/return"
            )
            return result.get("payment_url")

        if provider == 'atmos':
            try:
                paytechuz_config = getattr(settings, 'PAYTECHUZ', {})
                atmos_config = paytechuz_config.get('ATMOS', {})

                atmos_gateway = AtmosGateway(
                    consumer_key=atmos_config.get('CONSUMER_KEY'),
                    consumer_secret=atmos_config.get('CONSUMER_SECRET'),
                    store_id=atmos_config.get('STORE_ID'),
                    terminal_id=atmos_config.get('TERMINAL_ID'),
                    is_test_mode=atmos_config.get('IS_TEST_MODE', True)
                )

                payment_result = atmos_gateway.create_payment(
                    account_id=order_id,
                    amount=float(amount)
                )
                PaymentTransaction.create_transaction(
                    gateway=PaymentTransaction.ATMOS,
                    transaction_id=payment_result['transaction_id'],
                    account_id=str(order_id),
                    amount=amount
                )

                return payment_result['payment_url']

            except Exception as e:
                raise ValueError(f"Atmos payment error: {str(e)}")

        raise ValueError(f"Unsupported payment type: {provider}")

    def process_payment(self, order, status):
        """
        Update order and invoice status.
        """
        order.status = status
        order.save(update_fields=['status'])
        
        Invoice.objects.filter(order=order).update(status=status)
