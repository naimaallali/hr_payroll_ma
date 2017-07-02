# -*- encoding: utf-8 -*-
import openerp.netsvc
from openerp.osv import fields, osv
import openerp.pooler as pooler
from openerp.tools.translate import _
import time
from datetime import date, datetime

class hr_payroll_ma_bulletin_auto(osv.osv):

    _name = "hr.payroll_ma.bulletin_auto"
    _inherit="hr.payroll_ma.bulletin"

    def get_normal_hours(self,cr, uid,ids,context=None):

	total_work=self.pool.get('hr.total.work')
	nh_ids = total_work.search(cr, uid, [('employee_name','=',self.employee_id),('period_id','=',self.period_id)], context=context)
	nh=total_work.browse(cr, uid, nh_ids, context).normal_working_hours
	return nh

    def get_hs_hours(self,cr, uid,ids,context=None):

	total_work=self.pool.get('hr.total.work')
	hs_ids = total_work.search(cr, uid, [('employee_name','=',self.employee_id),('period_id','=',self.period_id)], context=context)
	hs=total_work.browse(cr, uid, hs_ids, context).hs_working_hours
	return hs

    def get_working_days(self,cr, uid,ids,context=None):

	total_work=self.pool.get('hr.total.work')
	hs_ids = total_work.search(cr, uid, [('employee_name','=',self.employee_id),('period_id','=',self.period_id)], context=context)
	hs=total_work.browse(cr, uid, hs_ids, context).working_days
	return hs

    _columns = {
        
        'employee_id': fields.many2one('hr.employee', 'Employe', change_default=True, readonly=False, required=True, select=1),
     
        #'normal_hours' : fields.function(get_normal_hours,type="float"),
	#'hs_hours' : fields.function(get_hs_hours,type="float"),
	#'working_days' : fields.function(get_working_days,type="float"),
	#'normal_hours' : fields.float('heures normales',readonly=True),
	'hs_hours' : fields.float('heures supplémentaires',readonly=True),
	#'working_days' : fields.float('jours travaillés',readonly=True),
	}

    _defaults = {
        #'normal_hours': '160',
        'hs_hours': '18',
        'working_days': '20',
		}

hr_payroll_ma_bulletin_auto()
    



