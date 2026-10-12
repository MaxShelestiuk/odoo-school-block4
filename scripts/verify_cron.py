"""Run via odoo-bin shell on a disposable verification database only."""
from datetime import timedelta

from odoo import fields

Visit = env['hr.hospital.patient.visit']  # noqa: F821
visits = Visit.create([
    {'name': 'B4 cron overdue',
     'visit_datetime': fields.Datetime.now() - timedelta(days=1)},
    {'name': 'B4 cron future',
     'visit_datetime': fields.Datetime.now() + timedelta(days=1)},
])
env.cr.commit()  # noqa: F821
cron = env.ref('hr_hospital.hospital_visit_cancel_overdue_cron')  # noqa: F821
result = cron.method_direct_trigger()
env.cr.commit()  # noqa: F821
env.invalidate_all()  # noqa: F821
assert visits[0].state == 'cancelled', result
assert visits[1].state == 'planned', result
print('PASS: actual Run Manually trigger, overdue cancelled, future unchanged')
visits.unlink()
env.cr.commit()  # noqa: F821
