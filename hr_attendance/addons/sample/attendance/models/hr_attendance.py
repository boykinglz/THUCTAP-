from odoo import models, fields, api

class CustomAttendance(models.Model):
    _inherit = 'hr.attendance'

    # Thêm trường tùy chỉnh vào model ứng viên
    # age = fields.Char(string='age')
    
    total_worked_hours = fields.Float(string='Total Worked Hours', compute='_compute_total_worked_hours')

    @api.depends('check_in', 'check_out')
    def _compute_total_worked_hours(self):
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                attendance.total_worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.total_worked_hours = 0.0

  
