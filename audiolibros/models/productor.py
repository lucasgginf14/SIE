from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Productor(models.Model):
    _name = 'audiolibro.productor'
    _description = 'Productor de audiolibro'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre', required=True)
    descripcion = fields.Text('Descripción')
    nacionalidad = fields.Char('Nacionalidad')
    email = fields.Char('Correo electrónico')
    telefono = fields.Char('Teléfono')

    audiolibros_ids = fields.One2many('audiolibro.audiolibro', 'productor_id', string='Audiolibros')

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe un productor con este nombre.'),
        ('email_unique', 'UNIQUE(email)', 'Ya existe un productor con este correo electrónico.'),
    ]

    @api.constrains('email')
    def _check_email(self):
        pattern = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
        for rec in self:
            if rec.email and not pattern.match(rec.email):
                raise ValidationError('Correo electrónico inválido.')

    @api.constrains('telefono')
    def _check_telefono(self):
        # Permitir dígitos, espacios, +, -, paréntesis
        pattern = re.compile(r'^[0-9\+\-\s\(\)]+$')
        for rec in self:
            if rec.telefono and not pattern.match(rec.telefono):
                raise ValidationError('Teléfono inválido. Solo se permiten dígitos, espacios, "+", "-", y paréntesis.')