# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions, _
import datetime
import pytz

class HrAttendance(models.Model):
    _inherit = "hr.attendance"
    
    shift_id=fields.Many2one("hr.attendance.shift", string="Shift", compute='_compute_shift_id', store=True)
    is_auto_checkout=fields.Boolean("Auto Checkout")
    
    def time_to_float(self, date_time):
        date_timezone=date_time.astimezone(pytz.timezone(self.env.user.partner_id.tz) )
        return float( "%.2f" %  float('%s.%s' % (date_timezone.time().hour, str(int(date_timezone.time().minute*100/60)))))
    
    @api.constrains('check_in', 'check_out')
    def _check_in_check_out(self):
        for attendance in self:
            hr_shift=False
            if attendance.check_in and attendance.check_out:
                if attendance.check_in.date() != attendance.check_out.date():
                    raise exceptions.ValidationError(_('In and Out should be in same date'))
                    
            if attendance.check_in:        
                time_float=self.time_to_float(attendance.check_in)    
#                 print(attendance.check_in,'checkin')   
                hr_shift = self.env['hr.attendance.shift'].search([
                    ('in_time', '<=', time_float),
                    ('in_time', '>=', time_float-1)
                ],limit=1)
                
                if not hr_shift:
                    raise exceptions.ValidationError(_('In time will be allowed only shift in time or an hour of delay'))
                
            if attendance.check_out:     
#                 print(attendance.check_out,'checkout')      
                time_float=self.time_to_float(attendance.check_out)                   
                if float( "%.2f" % hr_shift.out_time)>time_float or  float( "%.2f" % hr_shift.out_time)<float( "%.2f" %(time_float-(10/60))):
                    raise exceptions.ValidationError(_('Out time will be allowed only shift out time or 10 mins of delay'))

    @api.depends('check_in')
    def _compute_shift_id(self):
        for attendance in self:
            if attendance.check_in:                
                time_float=self.time_to_float(attendance.check_in)
                          
                hr_shift = self.env['hr.attendance.shift'].search([
                    ('in_time', '<=', time_float),
                    ('in_time', '>=', time_float-1)
                ],limit=1)
                
                if hr_shift:
                    attendance.shift_id=hr_shift.id

    @api.model
    def auto_checkout(self):
        attendance_ids = self.search([('check_out', '=', False),('shift_id', '!=', False)])
        
        ir_model_data = self.env['ir.model.data']
    
        for attendance in attendance_ids:
            time_float=self.time_to_float(datetime.datetime.today()) 
            if time_float>attendance.shift_id.out_time+0.16:
                n=datetime.datetime.today().date()
                attendance.is_auto_checkout=True
                attendance.check_out=datetime.datetime(n.year, n.month, n.day)+datetime.timedelta(hours=attendance.shift_id.out_time-5.5)
                mail_send=attendance.action_send_mail()
                print(mail_send)
             
    def action_send_mail(self):
        self.ensure_one()
        template_id = self.env.ref('hr_attendance_update.email_template_auto_checkout')
        if template_id:
            template_id.send_mail(self.id)
        
