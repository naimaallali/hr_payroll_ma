# -*- encoding: utf-8 -*-
import openerp.netsvc
from openerp.osv import fields, osv
import openerp.pooler as pooler
from openerp.tools.translate import _
import time
import datetime 
from datetime import date
from openerp import api


class hr_total_work_wiz(osv.osv):
  
    _name = "hr.total.work.wizard"
    _description = 'total des heures de travail'

    _columns = {
        
        'date_debut': fields.datetime('Debut de periode', required=True,select=1),
        'date_fin': fields.datetime('Fin de periode', required=True,select=1),
	#'period': fields.char('periode',size=32,readonly=True),
		}

    #@api.onchange('date_debut','date_fin')
    def _onchange_period(self,cr, uid,ids,context=None):
	period_obj = self.pool.get('account.period')
        pids = period_obj.search(cr, uid, ['&',('date_start','<=',self.date_debut),('date_stop','>=',self.date_fin)], context=context)
	self.period=period_obj.browse(cr, uid, pids, context)['name']
	

    @api.multi
    def total_work_hours(self):
	    return {
		'type'     : 'ir.actions.act_window',
		'res_model': 'hr.total.work',
		'view_mode': 'tree',
			 }

hr_total_work_wiz()

class hr_total_work(osv.osv):
  
    _name = "hr.total.work"
    _description = 'total des heures de travail'

    _columns = {
        
        'date_debut': fields.datetime('Debut de periode', required=False,select=1),
        'date_fin': fields.datetime('Fin de periode', required=False,select=1),
	'employee_name': fields.many2one('hr.employee', 'Employe', change_default=True),
	'period_id': fields.many2one('account.period', 'Periode', select=1),
	'working_days': fields.float('Total des jours travaillés',  readonly=False),
	'normal_working_hours': fields.float('Total des heures normales travaillées',  readonly=False),
	'hs_working_hours': fields.float('Total des heures supplémentaires travaillées',  readonly=False),
		}
hr_total_work()

class hr_absence(osv.osv):
  
    _name = "hr.absence"
    _description = 'total des absences'

    _columns = {
        
        'date_debut': fields.datetime('Debut de periode', required=False,select=1),
        'date_fin': fields.datetime('Fin de presence', required=False,select=1),
	'employee_name': fields.many2one('hr.employee', 'Employe', change_default=True),
	'absence_hours': fields.float('Total des heures absentées', readonly=False),
		}
hr_absence()
