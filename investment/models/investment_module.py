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
    benefit_id = fields.Many2one("investment.benefit")
