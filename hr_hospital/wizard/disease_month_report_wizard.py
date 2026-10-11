from datetime import datetime, time, timedelta

import pytz

from odoo import fields, models
from odoo.exceptions import UserError


class DiseaseMonthReportWizard(models.TransientModel):
    _name = 'hospital.disease.month.report.wizard'
    _description = 'Monthly Disease Visit Report'

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Лікарі')
    disease_ids = fields.Many2many('hr.hospital.disease', string='Хвороби')
    date_from = fields.Date(string='З')
    date_to = fields.Date(string='По', help='Останній день включається повністю.')

    def action_show_visits(self):
        self.ensure_one()
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise UserError(self.env._('Дата «з» має бути не пізніше дати «по».'))
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'child_of', self.disease_ids.ids))
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        for date, operator in ((self.date_from, '>='), (self.date_to, '<')):
            if not date:
                continue
            # Exclusive next-local-day boundary includes the entire final day,
            # including DST transitions, without comparing Datetime with Date.
            if operator == '<':
                date += timedelta(days=1)
            boundary = user_tz.localize(datetime.combine(date, time.min))
            utc_boundary = boundary.astimezone(pytz.UTC).replace(tzinfo=None)
            domain.append(('visit_datetime', operator, utc_boundary))
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Звіт по хворобах за місяць'),
            'res_model': 'hr.hospital.patient.visit',
            'view_mode': 'list,form,pivot,graph', 'target': 'current',
            'domain': domain,
            'context': {'group_by': 'disease_id', 'active_test': False},
        }
