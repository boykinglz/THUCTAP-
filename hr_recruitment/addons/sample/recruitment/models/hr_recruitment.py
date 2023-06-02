from odoo import models, fields, api


class CustomRecruitmentSource(models.Model):
    _inherit = 'hr.recruitment.source'

    # Thêm trường tùy chỉnh vào model nguồn ứng viên
    custom_field = fields.Char()


class CustomRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    # Thêm trường tùy chỉnh vào model giai đoạn tuyển dụng
    custom_field = fields.Char()

class DegrreType(models.Model):
    _name = 'hr.recruitment.degrretype'

    name = fields.Char(string = 'Degree Type')



class CustomRecruitmentDegree(models.Model):
    _inherit = 'hr.recruitment.degree'

    # Thêm trường tùy chỉnh vào model bằng cấp
    Degree_type = fields.Many2many('hr.recruitment.degrretype',string='Degree Type')




class CustomApplicant(models.Model):
    _inherit = 'hr.applicant'

    # Thêm trường tùy chỉnh vào model ứng viên
    custom_field = fields.Char(string='Custom Field')

  
