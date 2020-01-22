# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions, _


class HrAttendanceShift(models.Model):    
    _name = "hr.attendance.shift"
    
    name=fields.Char("Shift Name", required=True)
    in_time=fields.Float(string='In Time', required=True)
    out_time=fields.Float(string='Out Time', required=True)
    
    
    @api.constrains('in_time', 'out_time')
    def _check_validity_in_time_out_time(self):
        for shift in self:
            if shift.in_time and shift.out_time:
                if shift.out_time < shift.in_time:
                    raise exceptions.ValidationError(_('"Out" time cannot be earlier than "In" time.'))
                if shift.out_time >= 24.00:
                    raise exceptions.ValidationError(_('"Out" time cannot be grater than 23:59.'))
                     
            hr_shift = self.env['hr.attendance.shift'].search([
                ('in_time', '>=', shift.in_time),
                ('in_time', '<=', shift.out_time),   
                ('id', '!=', shift.id),
            ],limit=1)
                        
            if hr_shift:
                raise exceptions.ValidationError(_('In/Out time is conflicting with other Shift'))
                
                
            hr_shift = self.env['hr.attendance.shift'].search([
                ('out_time', '>=', shift.in_time),
                ('out_time', '<=', shift.out_time),
                ('id', '!=', shift.id),
            ],limit=1)            
            if hr_shift:
                raise exceptions.ValidationError(_('In/Out time is conflicting with  other Shift'))


