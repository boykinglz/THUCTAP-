import base64
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class Relationship(models.Model):
    _name = 'hr.relationship'
    _description = 'Employee Relationship'

    employee_id = fields.Many2one('hr.employee', string='Employee', groups="hr.group_hr_user")
    name = fields.Char(string='Name', groups="hr.group_hr_user")
    relation_type = fields.Selection([
        ('family', 'Family'),
        ('friend', 'Friend'),
        ('colleague', 'Colleague')
    ], string='Relationship Type', groups="hr.group_hr_user")


class MedicalRecord(models.Model):
    _name = 'medical.record'
    _description = 'Medical Record'

    employee_id = fields.Many2one('hr.employee', string='Employee', groups="hr.group_hr_user")
    date = fields.Date(string='Date', groups="hr.group_hr_user")
    diagnosis = fields.Char(string='Diagnosis', groups="hr.group_hr_user")
    treatment = fields.Text(string='Treatment', groups="hr.group_hr_user")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    relationship_ids = fields.One2many('hr.relationship', 'employee_id', string='Relationships', groups="hr.group_hr_user")
    medical_record_ids = fields.One2many('medical.record', 'employee_id', string='Medical Records', groups="hr.group_hr_user")
    labor_contract = fields.Binary(string='Labor Contract', groups="hr.group_hr_user")
    labor_contract_filename = fields.Char(string='Labor Contract Filename', groups="hr.group_hr_user")
    appendix_contract = fields.Binary(string='Appendix Contract', groups="hr.group_hr_user")
    appendix_contract_filename = fields.Char(string='Appendix Contract Filename', groups="hr.group_hr_user")
    salary_adjustment = fields.Binary(string='Salary Adjustment', groups="hr.group_hr_user")
    salary_adjustment_filename = fields.Char(string='Salary Adjustment Filename', groups="hr.group_hr_user")

    # Override the existing view to add the relationship and medical record sections
    def _get_formview_id(self, access_uid=None):
        self.ensure_one()
        if self._context.get('family_information_view', False):
            return self.env.ref('your_module_name.view_employee_form_inherit').id
        return super(HrEmployee, self)._get_formview_id(access_uid)
class EmployeeReport(models.Model):
    _name = 'employee.report'
    _description = 'Báo cáo nhân viên'

    name = fields.Char('Họ tên')
    birthday = fields.Date('Ngày sinh')
    certificate = fields.Selection([
        ('bachelor', 'Cử nhân'),
        ('master', 'Thạc sĩ'),
        ('other', 'Khác'),
    ], 'Trình độ')
    study_field = fields.Char('Chuyên ngành')
    department_id = fields.Many2one('hr.department', 'Bộ phận')
    diagnosis = fields.Char('Số sổ BHXH')
    notes = fields.Text('Ghi chú')

    def get_employee_data(self):
        employees = self.env['hr.employee'].search([])
        employee_data = []
        for employee in employees:
            employee_data.append({
                'name': employee.name,
                'birthday': employee.birthday,
                'certificate': employee.certificate,
                'study_field': employee.study_field,
                'department_id': employee.department_id.name,
                'diagnosis': employee.diagnosis,
                'notes': employee.notes,
            })
        return employee_data