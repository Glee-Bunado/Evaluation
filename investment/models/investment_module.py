# -*- coding: utf-8 -*-
from odoo import fields, models, api


class InvestmentModule(models.Model):
    _name = "investment.module"
    _description = "investment model"

    name = fields.Char(string="Reference")
    date = fields.Date(string="Date")
    investment_amount = fields.Float(string="Investment Amount")
    currency_id = fields.Many2one("res.currency", string="Currency")
    partner_id = fields.Many2one("res.partner")
    total_invested = fields.Float(string="Total Invested Amount", compute="_total_invested")
    total_investments = fields.Float(string="Total Investments", compute="_total_investments")
    first_investment = fields.Float(compute="_first_investment")
    next_investments = fields.Float(compute="_next_investments")

    @api.depends("investment_amount")
    def _total_invested(self):
        for rec in self:
            invest_search = self.env["investment.module"].search([('partner_id', '=', rec.partner_id.id)])
            rec.total_invested = sum([inv.investment_amount for inv in invest_search])

    @api.depends("investment_amount")
    def _total_investments(self):
        total = sum(self.env["investment.module"].search([]).mapped('investment_amount'))
        for rec in self:
            rec.total_investments = total

    @api.depends("investment_amount")
    def _first_investment(self):
        for rec in self:
            invest_search = self.env["investment.module"].search([('partner_id', '=', rec.partner_id.id)])
            x = []
            for inv in invest_search:
                x.append(inv.investment_amount)
            rec.first_investment = x[0]
    @api.depends("investment_amount")
    def _next_investments(self):
        for rec in self:
            invest_search = self.env["investment.module"].search([('partner_id', '=', rec.partner_id.id)])
            x = []
            for inv in invest_search:
                x.append(inv.investment_amount)
            rec.next_investments = sum(x[1:])
