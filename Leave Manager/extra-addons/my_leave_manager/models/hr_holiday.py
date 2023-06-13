from odoo import fields, models


class CustomHrHolidays(models.Model):
    _inherit = 'hr.leave'

    @api.multi
    def get_state_display(self):
        return dict(self._fields['state'].selection).get(self.state)
