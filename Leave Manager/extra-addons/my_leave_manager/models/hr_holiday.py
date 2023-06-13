from odoo import fields, models


class CustomHrHolidays(models.Model):
    _inherit = 'hr.leave'

    def check_inheritance(self):
        for test in self._inherit:
            print("Test something:" +test)
