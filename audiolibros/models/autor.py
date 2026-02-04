from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Autor(models.Model):
    _name = 'audiolibro.autor'
    _description = 'Autor del audiolibro'
    _rec_name = 'nombre_completo'

    nombre = fields.Char('Nombre', required=True)
    apellidos = fields.Char('Apellidos', required=True)
    fecha_nacimiento = fields.Date('Fecha de Nacimiento')
    nacionalidad = fields.Char('Nacionalidad')
    biografia = fields.Text('Biografía')

    nombre_completo = fields.Char(compute='_compute_nombre_completo', store=True)

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_completo(self):
        for r in self:
            nombre = r.nombre or ''
            apellidos = r.apellidos or ''
            r.nombre_completo = (nombre + ' ' + apellidos).strip()

    audiolibros_ids = fields.Many2many(
        'audiolibro.audiolibro',
        'autores_ids',
        string='Audiolibros'
    )

    _sql_constraints = [
        ('autor_unique', 'UNIQUE(nombre, apellidos)', 'Ya existe un autor con este nombre.'),
    ]

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for rec in self:
            if rec.fecha_nacimiento and rec.fecha_nacimiento > fields.Date.context_today(rec):
                raise ValidationError('La fecha de nacimiento no puede ser futura.')