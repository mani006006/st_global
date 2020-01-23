# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Attendance Update',
    'version': '1.0',
    'summary': 'Customize the modules',
    'description': """Attendance Update""",
    'depends': ['hr_attendance','hr','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_shift.xml',
        'views/hr_attendance.xml',
        'views/hr_view.xml',
        'wizard/non_checkout.xml',
        'views/check_out_cron.xml',
        'views/email_template.xml',
    ],
}
