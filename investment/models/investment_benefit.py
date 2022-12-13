from odoo import fields, models, api

class InvestmentBenefit(models.Model):
    _name = "investment.benefit"
    _description = "Investment Benefit"

    partner_id = fields.Many2one("res.partner")
    currency_id = fields.Many2one("res.currency")
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    benefit_value = fields.Float(compute="_benefit_amt")
    investment_ids = fields.One2many("investment.module", "benefit_id")


    @api.depends("investment_ids")
    def _benefit_amt(self):
        for rec in self:
            rec.benefit_value = 0.50 * rec.investment_ids.price



