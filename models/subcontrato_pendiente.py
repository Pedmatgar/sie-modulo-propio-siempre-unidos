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
    presupuesto = fields.Float(
        string='Presupuesto (€)',
        digits=(10, 2),
    )
    notas = fields.Text(
        string='Notas',
    )

    def action_crear_subcontrato(self):
        self.ensure_one()
        notas_partes = []
        if self.presupuesto:
            notas_partes.append(f'Presupuesto: {self.presupuesto:.2f} €')
        if self.notas:
            notas_partes.append(self.notas)
        notas_combinadas = '\n'.join(notas_partes) if notas_partes else False

        return {
            'type': 'ir.actions.act_window',
            'name': 'Nuevo subcontrato',
            'res_model': 'subcontrato.subcontrato',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_tipo_trabajo': self.tipo_trabajo,
                'default_otro_tipo_trabajo': self.otro_tipo_trabajo,
                'default_comunidad': self.comunidad.id,
                'default_empresa_o_empleado_externa_o_externo': self.contacto.id,
                'default_fecha_inicio': self.fecha_inicio,
                'default_notas': notas_combinadas,
            },
        }

    @api.constrains('tipo_trabajo', 'otro_tipo_trabajo')
    def _check_otro_tipo_trabajo(self):
        for record in self:
            if record.tipo_trabajo == 'otro' and not record.otro_tipo_trabajo:
                raise ValidationError("Si selecciona 'Otro', debe especificar el tipo de trabajo.")
