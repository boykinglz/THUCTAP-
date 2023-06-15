# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.mail.wizard.mail_compose_message import _reopen


class HrPayslipSend(models.TransientModel):
    _name = 'hr.payslip.send'
    _inherits = {'mail.compose.message': 'composer_id'}
    _description = 'Employee Payslip Send'

    is_email = fields.Boolean('Email', default=lambda self: self.env.user.company_id.invoice_is_email)
    payslip_without_email = fields.Text(compute='_compute_payslip_without_email',
                                        string='payslip(s) that will not be sent')
    is_print = fields.Boolean('Print', default=lambda self: self.env.user.company_id.invoice_is_print)
    printed = fields.Boolean('Is Printed', default=False)
    slip_ids = fields.Many2many('hr.payslip', 'hr_payslip_hr_payslip_send_rel', string='Payslips')
    composer_id = fields.Many2one('mail.compose.message', string='Composer', required=True, ondelete='cascade')
    template_id = fields.Many2one(
        'mail.template', 'Use template', index=True,
        domain="[('model', '=', 'hr.payslip')]"
    )
    employee_ids = fields.Many2many('hr.employee', string='Employees')

    @api.model
    def default_get(self, fields):
        res = super(HrPayslipSend, self).default_get(fields)
        res_ids = self._context.get('active_ids')
        composer = self.env['mail.compose.message'].create({
            'composition_mode': 'comment' if len(res_ids) == 1 else 'mass_mail',
        })
        res.update({
            'slip_ids': res_ids,
            'composer_id': composer.id,
        })
        return res

    @api.multi
    @api.onchange('slip_ids')
    def _compute_composition_mode(self):
        for wizard in self:
            wizard.composition_mode = 'comment' if len(wizard.slip_ids) == 1 else 'mass_mail'

    @api.onchange('template_id')
    def onchange_template_id(self):
        if self.composer_id:
            self.composer_id.template_id = self.template_id.id
            self.composer_id.onchange_template_id_wrapper()

    @api.onchange('is_email')
    def _compute_payslip_without_email(self):
        for wizard in self:
            if wizard.is_email and len(wizard.slip_ids) > 1:
                payslips = self.env['hr.payslip'].search([
                    ('id', 'in', self.env.context.get('active_ids')),
                    ('employee_id.email', '=', False)
                ])
                if payslips:
                    wizard.payslip_without_email = "%s\n%s" % (
                        _("The following payslip(s) will not be sent by email, because the customers don't have email address."),
                        "\n".join([i.reference or i.display_name for i in payslips])
                    )
                else:
                    wizard.payslip_without_email = False

    @api.multi
    def _send_email(self):
        if self.is_email:
            self.composer_id.send_mail()
            if self.env.context.get('mark_payslip_as_sent'):
                self.mapped('slip_ids').write({'sent': True})

    @api.multi
    def send_action(self):
        self.ensure_one()
        # Send the mails in the correct language by splitting the ids per lang.
        # This should ideally be fixed in mail_compose_message, so when a fix is made there this whole commit should be reverted.
        # basically self.body (which could be manually edited) extracts self.template_id,
        # which is then not translated for each customer.
        if self.composition_mode == 'mass_mail' and self.template_id:
            active_ids = self.env.context.get('active_ids', self.res_id)
            active_records = self.env[self.model].browse(active_ids)
            langs = active_records.mapped('employee_id.lang')
            default_lang = self.env.context.get('lang', 'en_US')
            for lang in (set(langs) or [default_lang]):
                active_ids_lang = active_records.filtered(lambda r: r.employee_id.lang == lang).ids
                self_lang = self.with_context(active_ids=active_ids_lang, lang=lang)
                self_lang.onchange_template_id()
                self_lang._send_email()
        else:
            self._send_email()
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def save_as_template(self):
        self.ensure_one()
        self.composer_id.save_as_template()
        self.template_id = self.composer_id.template_id.id
        action = _reopen(self, self.id, self.model, context=self._context)
        action.update({'name': _('Send Payslip')})
        return action
