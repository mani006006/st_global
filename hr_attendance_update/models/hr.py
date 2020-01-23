# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions, _

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    attendance_ids=fields.One2many("hr.attendance","employee_id", "Attendance List")
    