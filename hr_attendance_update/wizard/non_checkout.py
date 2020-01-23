# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMoveReversal(models.TransientModel):
    _name = 'hr.attendance.checkout'
    _description = 'Non checkout list'

    from_date=fields.Datetime("From date", required=True)
    to_date=fields.Datetime("To date", required=True)

    def non_checkout_users(self):
       print(1)
