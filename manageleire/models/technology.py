# -*- coding: utf-8 -*-

from odoo import models, fields, api # type: ignore

#se va a traducir en una tabla en la base de datos
class technology(models.Model):

    #ATRIBUTOS
    _name = 'manageleire.technology' #nombreModulo.nombreModelo --> así le llamo desde Odoo
    _description = 'manageleire.technology'


    #CAMPOS
    #entre paréntesis es el nombre de la tabla que se va a mostrar en la vista
    name = fields.Char(string = "Nombre de la tecnología", readonly = False, required = True, help = "Introduzca el nombre de la tecnología")
                                            #readonly (solo lectura): false --> se puede editar. Si fuese true no se podría editar
                                            #required: True --> obligatorio
                                            #cuando estoy sobre Nombre en la vista, se ve el mensaje de help
    description = fields.Char(string = "Descripción")
    photo = fields.Image(string = "Imagen")


    #RELACIONES
    #Cada tarea usa múltiples tecnologías y cada tecnología está asociada a múltiples tareas
    tareas_id = fields.Many2many(string="Tareas",
                                 comodel_name = "manageleire.task", #modelo con el que se crea la relación
                                 relation = "tasks_technologys", #nombre de la tabla que crea --> SE CONSULTA EN ODOO-AJUSTES-TECNICO-RELACIONES MANY2MANY (buscar por el nombre la tabla, lo que alberga relation)
                                 column1 = "technologys_ids", #hace referencia al registro de la tabla actual (columna izquierda)
                                 column2 = "tasks_ids") #hace referencia al registro de comodel_name (columna derecha)