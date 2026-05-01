# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SieMember(models.Model):
    _name = 'sie.member'
    _description = 'Miembro SIE'
    _order = 'name asc'

    name = fields.Char(
        string='Nombre',
        required=True,
        index=True,
    )
    code = fields.Char(
        string='Código',
        copy=False,
        readonly=True,
        default='Nuevo',
    )
    email = fields.Char(string='Correo Electrónico')
    phone = fields.Char(string='Teléfono')
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('active', 'Activo'),
            ('inactive', 'Inactivo'),
        ],
        string='Estado',
        default='draft',
        required=True,
        tracking=True,
    )
    notes = fields.Text(string='Notas')
    date_join = fields.Date(
        string='Fecha de Ingreso',
        default=fields.Date.today,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'Nuevo') == 'Nuevo':
                vals['code'] = self.env['ir.sequence'].next_by_code('sie.member') or 'Nuevo'
        return super().create(vals_list)

    def action_activate(self):
        for record in self.filtered(lambda r: r.state == 'draft'):
            record.write({'state': 'active'})

    def action_deactivate(self):
        for record in self.filtered(lambda r: r.state == 'active'):
            record.write({'state': 'inactive'})

    def action_reset_draft(self):
        for record in self.filtered(lambda r: r.state != 'draft'):
            record.write({'state': 'draft'})
