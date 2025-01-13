# -*- coding: utf-8 -*-

from odoo import models, fields, api # type: ignore

#se va a traducir en una tabla en la base de datos
class project(models.Model):

    #ATRIBUTOS
    _name = 'manageleire.project' #nombreModulo.nombreModelo --> así le llamo desde Odoo
    _description = 'manageleire.project'


    #CAMPOS
    #entre paréntesis es el nombre de la tabla que se va a mostrar en la vista
    name = fields.Char(string = "Nombre del proyecto", readonly = False, required = True, help = "Introduzca el nombre del proyecto")
                                            #readonly (solo lectura): false --> se puede editar. Si fuese true no se podría editar
                                            #required: True --> obligatorio
                                            #cuando estoy sobre Nombre en la vista, se ve el mensaje de help
    description = fields.Char(string = "Descripción")


    #RELACIONES
    #Un proyecto tiene varias historias
    history_id = fields.One2many(string="Historias", 
                                 comodel_name="manageleire.history", 
                                 inverse_name="project_id")

    #Un proyecto tiene muchos sprints
    sprint_id = fields.One2many(string="Carreras",
                                comodel_name="manageleire.sprint", 
                                inverse_name= "project_id")