from odoo import fields, models, api
from datetime import date
import datetime


class InvestmentBenefit(models.Model):
    _name = "investment.benefit"
    _description = "Investment Benefit"

    partner_id = fields.Many2one("res.partner")
    currency_id = fields.Many2one("res.currency")
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    benefit_value = fields.Float(compute="_benefit_amt")
    investment_id = fields.Many2one("investment.module")

    @api.depends("investment_id")
    def _benefit_amt(self):
        for rec in self:
            # benefit rate for the following investments
            invest_search = self.env["investment.benefit"].search([('partner_id', '=', rec.partner_id.id)])
            x = []
            for inv in invest_search:
                x.append(inv.investment_id.investment_amount)

            first_benefit_value = 0.50 * x[0]
            following_benefit_rate = sum(x)/rec.investment_id.total_investments

            d_start = date(rec.date_start.year, rec.date_start.month, rec.date_start.day)
            d_end = date(rec.date_end.year, rec.date_end.month, rec.date_end.day)
            d_deposit = date(rec.investment_id.date.year, rec.investment_id.date.month, rec.investment_id.date.day)

            if 0 < (d_end - d_start).days <= 15:
                rec.benefit_value = first_benefit_value

            if (d_end - d_start).days > 15:
                rec.benefit_value = rec.investment_id.next_investments * following_benefit_rate




