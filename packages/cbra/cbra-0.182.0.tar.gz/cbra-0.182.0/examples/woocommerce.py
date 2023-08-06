"""Example webhook implementation for WooCommerce webhook
event messages.
"""
import cbra

from cbra.ext import woocommerce


class WooCommerceWebhook(woocommerce.WebhookEndpoint):
    echo: bool = True

    def get_hmac_secret(self) -> bytes:
        return b'foo'


def get_asgi_application():
    app = cbra.Application()
    app.add(WooCommerceWebhook)
    return app


app = get_asgi_application()
if __name__ == '__main__':
    cbra.run('__main__:app', reload=True)
