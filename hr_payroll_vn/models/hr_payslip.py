# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools.misc import format_date


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    basic_wage = fields.Monetary(compute='_compute_basic_net')
    net_wage = fields.Monetary(compute='_compute_basic_net')
    currency_id = fields.Many2one(related='contract_id.currency_id')
    dates = fields.Char(compute='_compute_dates')
    sent = fields.Boolean(readonly=True, default=False, copy=False,
                          help="It indicates that the payslip has been sent.")
    user_id = fields.Many2one('res.users', string='Human Resources Manager', track_visibility='onchange',
                              readonly=True, states={'draft': [('readonly', False)]},
                              default=lambda self: self.env.user, copy=False)

    def _compute_basic_net(self):
        for payslip in self:
            payslip.basic_wage = payslip._get_salary_line_total('BASIC')
            payslip.net_wage = payslip._get_salary_line_total('NET')

    def _get_salary_line_total(self, code):
        lines = self.line_ids.filtered(lambda line: line.code == code)
        return sum([line.total for line in lines])

    @api.depends('date_from')
    def _compute_dates(self):
        for slip in self.filtered(lambda p: p.date_from):
            lang = slip.employee_id.sudo().address_home_id.lang or self.env.user.lang
            context = {'lang': lang}
            del context

            slip.dates = '%(dates)s' % {
                'dates': format_date(self.env, slip.date_from, date_format="MMMM y", lang_code=lang)
            }

    @api.multi
    def action_payslip_sent(self):
        self.ensure_one()
        template = self.env.ref('hr_payroll_vn.email_template_edi_payslip', False)
        compose_form = self.env.ref('hr_payroll_vn.hr_payslip_send_wizard_form', False)
        lang = self.env.context.get('lang')
        if template and template.lang:
            lang = template._render_template(template.lang, 'hr.payslip', self.id)
        self = self.with_context(lang=lang)
        STATE = {
            'draft': _('Draft Payslip'),
            'verify': _('Draft Payslip'),
            'done': _('Payslip'),
            'cancel': _('Payslip'),
        }
        ctx = dict(
            default_model='hr.payslip',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            model_description=STATE[self.state],
            custom_layout="mail.mail_notification_paynow",
            force_email=True
        )
        return {
            'name': _('Send Payslip'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payslip.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
