{
    'name': 'Vietnam HR Payroll',
    'depends': ['hr_payroll'],
    'data': [
        'views/hr_payslip_views.xml',
        'views/report_payslip_run_templates.xml',
        'views/hr_payroll_run_report.xml',
        'wizard/hr_payslip_send_views.xml',
        'data/mail_template_data.xml'
    ]
}