####################
Best Practices
####################


.. _freeze-your-cart:

********************
Freeze your cart
********************

A shopping cart should be freezed when a payment session is initialized sothat
the customer can't empty his cart or modify the cart which changes the total
amount payable. A cutomer can do so if he inadvertedly gets into the cart page
pressing browser's back button (trust me they do that a lot). Letting the
customer modify the cart during an ongoing transaction may result in
catestrophic results. SSLCOMMERZ SDK prevents such catestrophys by raising a
:code:`TotalAmountTamperedException` exception and thus stopping the customer
from proceeding to checkout when payable amount is altered during an ongoing
transaction which will present a 500 server error to the customer.

The shopping cart should be unfreezed when the payment fails or the customer
cancels the transaction so that he can modify the cart.

Checkout `Next Steps`_.


.. _Next Steps: https://github.com/monim67/sslcommerz-sdk#next-steps
