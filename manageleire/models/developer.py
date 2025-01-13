# -*- coding: utf-8 -*-

from odoo import models, fields, api # type: ignore

#TEMA 9 --> HERENCIA EN ODOO
class developer(models.Model):

    '''
    Con esto, estamos modificando la tabla de res.partner y añadiendo los campos que indiquemos (si 
    añadimos un campo ya existente, se va a sobreescribir).
    '''
    _name = 'res.partner'
    _inherit = 'res.partner' #herencia

    is_dev = fields.Boolean()
    '''
    Vamos a añadir campos a la tabla res.partner: technologies (Many2many). Este campo se va a 
    añadir al modelo res.partner y no se va a crear un modelo nuevo developer:
    '''
    technologies = fields.Many2many('manageleire.technology',
                                    relation='developer_technologies',
                                    column1='developer_id',
                                    column2='technologies_id')
