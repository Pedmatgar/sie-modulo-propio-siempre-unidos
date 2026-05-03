from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SubcontratoPendiente(models.Model):
    _name = 'subcontrato.pendiente'
    _description = 'Subcontratación pendiente'
    _order = 'comunidad, tipo_trabajo'

    tipo_trabajo = fields.Selection(
        selection=[
            ('limpiador', 'Limpiador/a'),
            ('portero', 'Portero/a'),
            ('socorrista', 'Socorrista'),
            ('jardinero', 'Jardinero/a'),
            ('mantenimiento', 'Mantenimiento'),
            ('obrero', 'Obrero/a'),
            ('vigilante', 'Vigilante de seguridad'),
            ('otro', 'Otro'),
        ],
        string='Tipo de trabajo',
        required=True,
    )
    otro_tipo_trabajo = fields.Char(
        string='Especificar otro trabajo',
    )
    comunidad = fields.Many2one(
        comodel_name='res.partner',
        string='Comunidad',
        required=True,
    )
    fecha_inicio = fields.Date(
        string='Fecha de inicio',
        required=False,
    )
    contacto = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto externo',
        domain="[('category_id.name', '=', 'Externo')]",
        required=True,
    )
    notas = fields.Text(
        string='Notas',
    )

    @api.constrains('tipo_trabajo', 'otro_tipo_trabajo')
    def _check_otro_tipo_trabajo(self):
        for record in self:
            if record.tipo_trabajo == 'otro' and not record.otro_tipo_trabajo:
                raise ValidationError("Si selecciona 'Otro', debe especificar el tipo de trabajo.")
