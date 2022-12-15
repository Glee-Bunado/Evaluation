from odoo import fields, models, api
from datetime import date
from datetime import datetime



class InvestmentBenefit(models.Model):
    _name = "investment.benefit"
    _description = "Investment Benefit"

    partner_id = fields.Many2one("res.partner")
    currency_id = fields.Many2one("res.currency")
    date_start = fields.Date(string="Start Date", default=datetime.strptime("2022-12-15", '%Y-%m-%d').date())
    date_end = fields.Date(string="End Date",  default=datetime.strptime("2022-12-15", '%Y-%m-%d').date())
    investment_start = fields.Date(string="Start of Investment",
                                   default=datetime.strptime("2022-12-15", '%Y-%m-%d').date())
    registered_benefits = fields.Float("Registered Benefit Amount")
    benefit_value = fields.Float(compute="_benefit_amt")
    investment_id = fields.Many2one("investment.module")
    following_benefit_rate = fields.Float(compute="_following_benefit_rate")
    total_benefit = fields.Float(compute="_total_benefit")

    @api.depends("investment_id")
    def _following_benefit_rate(self):
        for rec in self:
            # benefit rate for the following investments
            inv_search = self.env["investment.benefit"].search([('partner_id', '=', rec.partner_id.id)])
            x = []
            for inv in inv_search:
                x.append(inv.investment_id.total_invested)

            rec.following_benefit_rate = x[0]/rec.investment_id.total_investments

    @api.depends("investment_id")
    def _benefit_amt(self):
        for rec in self:
            first_benefit_rate = 0.50

            d_start = date(rec.date_start.year, rec.date_start.month, rec.date_start.day)
            d_end = date(rec.date_end.year, rec.date_end.month, rec.date_end.day)

            if d_start == rec.investment_start and (0 < (d_end - d_start).days <= 15):
                rec.benefit_value = rec.registered_benefits * first_benefit_rate

            elif (d_end - rec.investment_start).days > 15:
                rec.benefit_value = rec.registered_benefits * rec.following_benefit_rate

            else:
                rec.benefit_value = 0

    @api.depends("benefit_value")
    def _total_benefit(self):
        for rec in self:
            benefits = self.env["investment.benefit"].search([('partner_id', '=', rec.partner_id.id)])
            rec.total_benefit = sum([benefit.benefit_value for benefit in benefits])




