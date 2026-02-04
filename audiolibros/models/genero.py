from odoo import models, fields

class Genero(models.Model):
    _name = 'audiolibro.genero'
    _description = 'Género de audiolibro'
    _rec_name = 'nombre'

    nombre = fields.Char('Género', required=True)
    descripcion = fields.Text('Descripción')

    audiolibros_ids = fields.One2many(
        'audiolibro.audiolibro',
        'genero_id',
        string='Audiolibros'
    )

    _sql_constraints = [
        ('nombre_unique', 'UNIQUE(nombre)', 'Ya existe un género con este nombre.'),
    ]