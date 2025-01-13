# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api # type: ignore

#se va a traducir en una tabla en la base de datos
class task(models.Model):

    #ATRIBUTOS
    _name = 'manageleire.task' #nombreModulo.nombreModelo --> así le llamo desde Odoo
    _description = 'manageleire.task'


    #CAMPOS
    #entre paréntesis es el nombre de la tabla que se va a mostrar en la vista
    name = fields.Char(string = "Nombre de la tarea", readonly = False, required = True, help = "Introduzca el nombre de la tarea")
                                            #readonly (solo lectura): false --> se puede editar. Si fuese true no se podría editar
                                            #required: True --> obligatorio
                                            #cuando estoy sobre Nombre en la vista, se ve el mensaje de help
    description = fields.Char(string = "Descripción")
    start_date = fields.Datetime(string = "Fecha inicio")
    end_date = fields.Datetime(string = "Fecha fin") 
    is_paused = fields.Boolean(string = "¿Está parado?")
    #PRACTICA 17 - TEMA 8 --> Añadir al modelo tarea un nuevo campo computado llamado code, que no se almacene 
                            #en la base de datos y que tome el siguiente valor: una cadena (TSK_, seguido del campo id del modelo)
    code = fields.Char(string="Código", compute="_compute_code")
    #TEMA 9 --> campo creado para almacenar la fecha y hora de creación de la tarea con una función lambda
    definition_date = fields.Datetime(string = "Fecha de creación", default=lambda p: datetime.datetime.now())


    #RELACIONES
    #Cada sprint tiene múltiples tareas asignadas; cada tarea se asigna a un sprint específico
    sprint_id = fields.Many2one(comodel_name="manageleire.sprint", 
                                string = "Sprint",
                                ondelete = "cascade",
                                #TEMA 9 --> vamos a tener un solo sprint abierto por proyecto en cada momento (fecha de inicio y de fin) y cada una de las tareas que vamos creando asociadas a la historia de usuario, 
                                            #se van a asociar al sprint que esté abierto, de forma automática; el usuario no va a decidir el sprint que se va a asociar a la tarea.
                                compute="_get_sprint",
                                store= True)
    #Cada tarea usa múltiples tecnologías y cada tecnología está asociada a múltiples tareas
    tecnologias_id = fields.Many2many(string="Tecnologías",
                                      comodel_name="manageleire.technology", #es el obligatorio por defecto, es el nombre del modelo con el que se establece la relación
                                      relation="tecnologias_tareas", #nombre de la tabla que crea --> SE CONSULTA EN ODOO-AJUSTES-TECNICO-RELACIONES MANY2MANY (buscar por el nombre la tabla, lo que alberga relation)
                                      column1="tecnologias_ids", #hace referencia al registro de la tabla actual (columna izquierda)
                                      column2="tareas_ids") #hace referencia al registro de comodel_name (columna derecha)
    #Muchas tareas están asociadas a una historia
    history_id = fields.Many2one(comodel_name="manageleire.history", 
                                 string="Historia", 
                                 required=True, 
                                 ondelete="cascade")
    
    
    #FUNCIONES
    #PRACTICA 17 - TEMA 8 --> método del campo code
    def _compute_code(self):
        for task in self:
            task.code = "TSK_"+ str(task.id) #id es un campo propio dEL programa de cada modelo


    #TEMA 9 --> El campo sprint se va a calcular cuando se genere el valor del campo “code” (la función _get_sprint
                #se va a ejecutar cuando el campo code cambie) por eso se crea la función _get_sprint, con el decorador @api.depends (“code”).
    @api.depends('code')
    def _get_sprint(self):
        for task in self: #recibe la colección de tareas
            #obtener todos los sprints que tenemos en el sistema
                #self.env --> se introduce el modelo a buscar y sobre este modelo, queremos buscar los sprints asociados al proyecto en concreto; puede haber varios. 
                #Para obtener los registros del modelo sprint: usamos search. Cada sprint tiene un campo project_id
                #(relación Many2one); buscamos los sprints cuyo project_id.id sea igual al project_id.id de la historia de la 
                #tarea. El resultado de esta búsqueda será un conjunto de registros (recordset) que cumplan con la condición.
            sprints = self.env['manageleire.sprint'].search([('project_id', '=', task.history_id.project_id.id)])
            found = False
            #recorre la lista de sprints asociados al proyecto al que pertenece la tarea 
            for sprint in sprints:
                #verificar que el campo end_date contiene una fecha válida (comprobar que es un objeto de tipo datetime: isinstance(sprint.end_date, datetime.datetime). 
                #También comprobar si la fecha de finalización del sprint es posterior a la fecha actual
                if isinstance(sprint.end_date, datetime.datetime) and sprint.end_date > datetime.datetime.now():
                    #si se encuentra un sprint válido, se asigna su ID al campo task.sprint_id y found pasa a valer True
                    task.sprint_id = sprint
                    found = True
            if not found:
                task.sprint_id = False

    #AMPLIACIÓN: botón de eliminar que elimina el registro que se quiera. Se mostrará en el tree
    def f_delete(self):
        #Eliminar el registro actual --> cuando se define un botón con type="object", el botón pasa automáticamente el registro actual (o los registros seleccionados) al método
        if not self:
            raise ValueError("No se seleccionó ningún registro para eliminar.")

        #Eliminar la tarea
        self.unlink()
