# -*- coding: utf-8 -*-

from odoo import models, fields, api # type: ignore
import datetime

#se va a traducir en una tabla en la base de datos
class sprint(models.Model):

    #ATRIBUTOS
    _name = 'manageleire.sprint' #nombreModulo.nombreModelo --> así le llamo desde Odoo
    _description = 'manageleire.sprint'


    #CAMPOS
    #entre paréntesis es el nombre de la tabla que se va a mostrar en la vista
    name = fields.Char(string = "Nombre del sprint", readonly = False, required = True, help = "Introduzca el nombre del sprint")
                                            #readonly (solo lectura): false --> se puede editar. Si fuese true no se podría editar
                                            #required: True --> obligatorio
                                            #cuando estoy sobre Nombre en la vista, se ve el mensaje de help
    description = fields.Char(string = "Descripción")
    start_date = fields.Datetime(string = "Fecha inicio")
    #el compute y store es debido al uso de la función abajo definida (_get_end_date)
    end_date = fields.Datetime(string = "Fecha fin", compute="_get_end_date", store=True) 

    #PRACTICA 17 - TEMA 8 -->  con la fecha de inicio y la duración, calcularemos la fecha de fin. Además, la fecha de fin se almacene en base de datos y sólo se recalcule si el usuario cambia la fecha de inicio o la duración:
    duration = fields.Integer(string="Duración (días)", default=15)


    #RELACIONES
    #Cada sprint tiene múltiples tareas asignadas; cada tarea se asigna a un sprint específico
    tasks_id = fields.One2many(string ="Tasks", 
                               comodel_name="manageleire.task", 
                               inverse_name="sprint_id")
    #Muchas sprint tienen un proyecto
    project_id = fields.Many2one(comodel_name="manageleire.project", 
                                 string="Project", 
                                 required=True, 
                                 ondelete="cascade")

    #FUNCIONES
    #función para calcular la fecha de fin (para duration)
    #@api.depends define dependencias entre campos. Los métodos que usan este decorador se ejecutan automáticamente cuando cambian los valores de los campos indicados como argumentos.
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for sprint in self:
            '''isinstance() se utiliza para verificar si un objeto pertenece a una clase. 
            Devuelve True si el objeto pertenece a la clase y False en caso contrario'''
            if isinstance(sprint.start_date, datetime.datetime) and sprint.duration > 0:
                '''timedelta pertenece al módulo datetime y se utiliza para representar una 
                    diferencia o duración en tiempo (un intervalo de tiempo). Se usa para realizar operaciones con 
                    fechas: sumar o restar tiempo a una fecha, diferencia entre 2 fechas…
                    Sintaxis: timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
                    Todos los argumentos son opcionales, se pueden marcar varios a la vez, y por defecto tienen el valor 0
                    '''
                sprint.end_date = sprint.start_date + datetime.timedelta(days=sprint.duration)
            else:
                sprint.end_date = sprint.start_date