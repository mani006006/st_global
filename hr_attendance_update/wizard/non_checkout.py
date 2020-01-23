# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountMoveReversal(models.TransientModel):
    _name = 'hr.attendance.checkout'
    _description = 'Non checkout list'

    from_date=fields.Datetime("From date", required=True)
    to_date=fields.Datetime("To date", required=True)
# 
#     @api.model
#     def default_get(self, fields):
#         res = super(AccountMoveReversal, self).default_get(fields)
#         move_ids = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.env['account.move']
#         res['refund_method'] = (len(move_ids) > 1 or move_ids.type == 'entry') and 'cancel' or 'refund'
#         res['residual'] = len(move_ids) == 1 and move_ids.amount_residual or 0
#         res['currency_id'] = len(move_ids.currency_id) == 1 and move_ids.currency_id.id or False
#         res['move_type'] = len(move_ids) == 1 and move_ids.type or False
#         return res
# 
#     @api.depends('move_id')
#     def _compute_from_moves(self):
#         move_ids = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.move_id
#         for record in self:
#             record.residual = len(move_ids) == 1 and move_ids.amount_residual or 0
#             record.currency_id = len(move_ids.currency_id) == 1 and move_ids.currency_id or False
#             record.move_type = len(move_ids) == 1 and move_ids.type or False

    def non_checkout_users(self):
        print(self.from_date,self.to_date)
        attendance_ids = self.env['hr.attendance'].search([('check_in','>=',self.from_date),('check_out','<=',self.to_date)])
        print(attendance_ids)
        
        
        return {
            'name': _('Attendances'),
            'view_mode': 'tree,form',
            'res_model': 'hr.attendance',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', attendance_ids.ids)],
        }
        
