from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Subcontrato(models.Model):
    _name = 'subcontrato.subcontrato'
    _description = 'Subcontrato'
    _rec_name = 'name'
    _order = 'fecha_inicio desc, name'

    name = fields.Char(
        string='Referencia del contrato',
        required=True,
        copy=False,
        default='Nuevo',
    )
    empleado_externo = fields.Many2one(
        comodel_name='res.partner',
        string='Empleado externo',
        required=True,
    )
    tipo_trabajo = fields.Selection(
        selection=[
            ('limpiador', 'Limpiador/a'),
            ('portero', 'Portero/a'),
            ('socorrista', 'Socorrista'),
            ('jardinero', 'Jardinero/a'),
            ('vigilante', 'Vigilante de seguridad'),
            ('otro', 'Otro'),
        ],
        string='Tipo de trabajo',
        required=True,
    )
    comunidad = fields.Many2one(
        comodel_name='res.partner',
        string='Comunidad asignada',
        required=True,
    )
    fecha_inicio = fields.Date(
        string='Fecha de inicio',
        required=True,
    )
    fecha_fin = fields.Date(
        string='Fecha de finalización',
        required=True,
    )
    importe = fields.Float(
        string='Importe mensual (€)',
        digits=(10, 2),
    )
    notas = fields.Text(
        string='Notas',
    )
    state = fields.Selection(
        selection=[
            ('activo', 'Activo'),
            ('expirado', 'Expirado'),
        ],
        string='Estado',
        default='activo',
        required=True,
        tracking=True,
    )
    vencimiento_anticipado = fields.Boolean(
        string='Vencimiento anticipado',
        default=False,
        readonly=True,
        help='Indica que el contrato fue expirado manualmente antes de alcanzar su fecha de finalización.',
    )

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for record in self:
            if record.fecha_fin < record.fecha_inicio:
                raise ValidationError(
                    'La fecha de finalización debe ser posterior a la fecha de inicio.'
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._auto_expirar_si_vencido()
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'fecha_fin' in vals or 'state' in vals:
            self._auto_expirar_si_vencido()
        return res

    def _auto_expirar_si_vencido(self):
        """Expire any active contracts whose end date has passed."""
        today = fields.Date.today()
        to_expire = self.filtered(
            lambda r: r.state == 'activo' and r.fecha_fin < today
        )
        if to_expire:
            super(Subcontrato, to_expire).write({'state': 'expirado', 'vencimiento_anticipado': False})

    def action_expirar(self):
        """Manually expire the contract. Marks vencimiento_anticipado if the end date has not yet passed."""
        today = fields.Date.today()
        for record in self:
            if record.state != 'activo':
                continue
            record.vencimiento_anticipado = record.fecha_fin >= today
            record.state = 'expirado'

    @api.model
    def _cron_eliminar_contratos_expirados(self):
        """Scheduled action: expire contracts whose end date has passed."""
        today = fields.Date.today()
        expirados = self.search([('fecha_fin', '<', today), ('state', '=', 'activo')])
        expirados.write({'state': 'expirado', 'vencimiento_anticipado': False})
