from odoo import models, fields

class CustomContract(models.Model):
    _inherit = 'hr.contract'

    custom_field = fields.Char('Custom Field')
    

# class ContractBenefit(models.Model):
#     _name = 'hr.contract_benefit'

#     name = fields.char(string='Contract Name')
#     employee_id = fields.Many2one('hr.employee', string='Employee')
#     amount = fields.Float(string='Amount')


