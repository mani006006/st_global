# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions, _
import datetime

class HrAttendance(models.Model):
    _inherit = "hr.attendance"
    
    shift_id=fields.Many2one("hr.attendance.shift", string="Shift", compute='_compute_shift_id')
    

                
    @api.constrains('check_in', 'check_out')
    def _check_in_check_out(self):
        for attendance in self:
            if attendance.check_in:                
                time_float=float('%s.%s' % (attendance.check_in.time().hour, str(int(attendance.check_in.time().minute*100/60))))
                     
                hr_shift = self.env['hr.attendance.shift'].search([
                    ('in_time', '>=', time_float),
                    ('in_time', '<=', time_float+1)
                ],limit=1)
                
                if hr_shift:
                    raise exceptions.ValidationError(_('Invalid Shift timing'))
                    
    @api.depends('check_in')
    def _compute_shift_id(self):
        for attendance in self:
            if attendance.check_in:                
                time_float=float('%s.%s' % (attendance.check_in.time().hour, str(int(attendance.check_in.time().minute*100/60))))
                     
                hr_shift = self.env['hr.attendance.shift'].search([
                    ('in_time', '>=', time_float),
                    ('in_time', '<=', time_float+1)
                ],limit=1)
                
                if hr_shift:
                   attendance.shift_id=hr_shift.id 
          
                