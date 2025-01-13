# -*- coding: utf-8 -*-

from odoo import models, fields, api # type: ignore

#se va a traducir en una tabla en la base de datos
class history(models.Model):

    #ATRIBUTOS
    _name = 'manageleire.history' #nombreModulo.nombreModelo --> así le llamo desde Odoo
    _description = 'manageleire.history'


    #CAMPOS
    #entre paréntesis es el nombre de la tabla que se va a mostrar en la vista
    name = fields.Char(string = "Nombre de la historia", readonly = False, required = True, help = "Introduzca el nombre de la historia")
                                            #readonly (solo lectura): false --> se puede editar. Si fuese true no se podría editar
                                            #required: True --> obligatorio
                                            #cuando estoy sobre Nombre en la vista, se ve el mensaje de help
    description = fields.Char(string = "Descripción")


    #RELACIONES
    #Muchas historias pertenece a un proyecto
    project_id = fields.Many2one(comodel_name="manageleire.project", 
                                 string="Proyecto", 
                                 required=True, 
                                 ondelete="cascade")
    
    #Cada historia tiene muchas tareas
    task_id = fields.One2many(string="Tareas", 
                              comodel_name="manageleire.task", 
                              inverse_name="history_id")
    
    #TEMA 9
    #Conjunto de tecnologías usadas en una historia
    used_technologies = fields.Many2many(string="Tecnologías usadas",
                                         comodel_name="manageleire.technolog",
                                         compute="_get_used_technologies")


    #FUNCIONES
    #Comprobar todas las tecnologías utilizadas en las tareas de una historia y asignarlas al campo used_technologies de esa historia
    def _get_used_technologies(self):
        for history in self:
            technologies = None #array para almacenar todas las tecnologías
            for task in history.task_id: #recorrer todas las tareas de una historia
                if not technologies:
                    technologies = task.tecnologias_id
                else:
                    technologies = technologies + task.tecnologias_id
            history.used_technologies = technologies #asignar las tecnologías a la historia