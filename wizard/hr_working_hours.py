# -*- encoding: utf-8 -*-
import openerp.netsvc
from openerp.osv import fields, osv
import openerp.pooler as pooler
from openerp.tools.translate import _
import time
import datetime 
from openerp import api


class hr_working_hours(osv.osv):
  
    _name = "hr.working.hours"
    _description = 'calcul heures de travail'

    _columns = {
        
        'date_debut_pres': fields.datetime('Date debut de presence', required=True,select=1),
        'date_fin_pres': fields.datetime('Date fin de presence', required=True,select=1),
	'date_debut_abs': fields.datetime('Date debut absence', required=True,select=1),
	'date_fin_abs': fields.datetime('Date fin absence', required=True,select=1),
	'creat_timesheet': fields.boolean('voulez vous créer les feuilles des temps pour les employés présents en cette période?'),
	'creat_abssheet':fields.boolean('voulez vous créer les listes des absences des employés absents en cette période?'),
	

		}

    def import_data(self,cr, uid,ids,context=None):
	result=[]
	pointage_obj=self.pool.get('hr.pointage.ma')
	emp_obj=self.pool.get('hr.employee')
	work_obj=self.pool.get('hr.total.work')
	emp_ids=emp.search(cr,uid,[])
	for e in emp_obj.browse(cr, uid, emp_ids, context):
		point_ids=pointage_obj.search(cr,uid,[('date_pointage','>',self.date_debut_pres),'|',('date_pointage','<',self.date_fin_pres),('employee_id','=',e['id'])])
		for p in pointage_obj.browse(cr, uid, point_ids, context):
			res=res+p.heures_travail
	work_obj.create(cr, uid,{ 'date_debut':self.date_debut_pres,'date_fin':self.date_fin_pres,'employee_id':e['id'] ,'working_hours' : res})
	
    @api.multi
    def total_absence_hours(self):
	    return {
		'type'     : 'ir.actions.act_window',
		'res_model': 'hr.absence.ma',
		'view_mode': 'form,tree',
			 }

	
