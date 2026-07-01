from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PaymentRegisterValidation(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.constrains('amount', 'payment_difference')
    def validate_payment_amount(self):
        for payment in self:
            # Odoo 19 Best Practice: Use compare_amounts to handle float precision safely.
            # compare_amounts(amount1, amount2) returns:
            #  1 if amount1 > amount2
            #  0 if amount1 == amount2
            # -1 if amount1 < amount2
            # We check if payment_difference is strictly less than 0.0 (-1).
            if payment.payment_type == 'outbound' and payment.currency_id.compare_amounts(payment.payment_difference, 0.0) < 0:
                raise UserError(_('Paying amount is greater than the amount to be paid. You cannot proceed with this payment.'))