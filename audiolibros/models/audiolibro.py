from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Audiolibro(models.Model):
    _name = 'audiolibro.audiolibro'
    _description = 'Audiolibro del catálogo'
    _rec_name = 'titulo'

    titulo = fields.Char('Título', required=True)
    duracion = fields.Float('Duración (horas)', digits=(6, 2))
    portada = fields.Binary('Portada')
    formato = fields.Selection([
        ('mp3', 'MP3'),
        ('aac', 'AAC'),
        ('wav', 'WAV'),
        ('flac', 'FLAC'),
        ('ogg', 'OGG'),
        ('m4a', 'M4A'),
    ], string='Formato', required=True)
    isbn = fields.Char('ISBN', required=True)
    precio = fields.Float('Precio', required=True)

    autores_ids = fields.Many2many('audiolibro.autor', string="Autores", required=True)
    genero_id = fields.Many2one('audiolibro.genero', string="Género", required=True)
    productor_id = fields.Many2one('audiolibro.productor', string='Productor', required=True)

    _sql_constraints = [
        ('precio_positivo', 'CHECK(precio >= 0)', 'El precio no puede ser negativo.'),
        ('duracion_positiva', 'CHECK(duracion > 0)', 'La duración no puede ser negativa.'),
        ('isbn_unique', 'UNIQUE(isbn)', 'Ya existe un audiolibro con este ISBN.'),
    ]

    @api.constrains('isbn')
    def _check_isbn(self):
        for record in self:
            if record.isbn:
                isbn_limpio = re.sub(r'[\s-]', '', record.isbn)
                if not re.match(r'^\d{13}$', isbn_limpio):
                    raise ValidationError('El ISBN debe contener exactamente 13 dígitos numéricos.')

    @api.constrains('precio')
    def _check_precio(self):
        for record in self:
            if record.precio < 0:
                raise ValidationError('El precio debe ser un valor positivo.')

    @api.constrains('duracion')
    def _check_duracion(self):
        for record in self:
            if record.duracion <= 0:
                raise ValidationError('La duración debe ser un valor positivo.')