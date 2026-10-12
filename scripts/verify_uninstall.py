"""Run via odoo-bin shell on a disposable verification database only."""
module = env['ir.module.module'].search([('name', '=', 'hr_hospital')])  # noqa: F821
cron_id = env.ref('hr_hospital.hospital_visit_cancel_overdue_cron').id  # noqa: F821
module.button_immediate_uninstall()
env.cr.commit()  # noqa: F821
assert module.state == 'uninstalled'
assert not env['ir.cron'].browse(cron_id).exists()  # noqa: F821
assert not env['ir.model.data'].search_count([('module', '=', 'hr_hospital')])  # noqa: F821
print('PASS: uninstall removes module records and cron')
