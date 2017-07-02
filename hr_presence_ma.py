# -*- encoding: utf-8 -*-
import openerp.netsvc
from openerp.osv import fields, osv
import openerp.pooler as pooler
from openerp.tools.translate import _
import time
import datetime 
from openerp import api


class hr_pointage_ma(osv.osv):

    _name = "hr.pointage.ma"
    _description = 'presence du personnel'

    def est_present(self,cr, uid, ids, context=None):
	#now = time.localtime(time.time())
	#dt=strptime(now)
	#employee_ids = []
	#for emp in self.browse(cr, uid, ids, context=context):
		#dtp=strptime(emp.date_pointage)
		#if emp.type_entree:
			#if dt(0) == dtp(0) and dt(1) == dtp(1) and dt(2) == dtp(2):
				#employee_ids[emp.employee_id]=emp
	return self.browse(cr, uid, ids, context=context)[0].date_pointage
	#return employee_ids

    def check_attendance(self,cr, uid, ids,field_name,arg, context=None):
	 res = dict(map(lambda x: (x,0), ids))
	 for insc in self.browse(cr, uid, ids, context):
		now=time.strftime("%d/%m/%y %H:%M:%S",time.localtime())
		dtp2=time.strptime(now,"%d/%m/%y %H:%M:%S")
		dat=datetime.datetime(2016,05,31)
		dtp1=dat.strftime("%d/%m/%y")
		dtp=time.strptime(dtp1,"%d/%m/%y")
		#dat2=datetime.datetime(insc['date_pointage'])
		#dtp3=insc['date_pointage'].strftime("%d/%m/%y %H:%M:%S")
		dtp4=time.strptime(insc['date_pointage'],"%Y-%m-%d %H:%M:%S")
		#dtp2=time.strptime(self.date_pointage,"%d/%m/%y %H:%M:%S")
		
		
		if int(dtp4[0]) == int(dtp2[0]) and int(dtp4[1]) == int(dtp2[1]) and int(dtp4[2]) == int(dtp2[2]):
			set1 = set(insc['action_pointage'].split(' '))
			set2 = set('entree'.split(' '))
			if set1 == set2 :
#and self.est_sorti(cr,uid,ids,insc['date_pointage'],insc['employe_id'],arg,context) == False:
                        	res[insc.id]=u'présent'
			else:
		     		res[insc.id]='absent'
		else:
		     		res[insc.id]='absent'	 
	        return res

    def est_sorti(self,cr, uid, ids,dat,empl,arg, context=None):
	ids= self.search(cr, uid,
        [ '|', ('date_pointage', '!=', dat),
        '|', ('employee_id', 'like', empl),
	'|', ('action_pointage', 'like', 'Pointer Sortie'),],)
	if ids:
		return True
	else:
		return False
		
    def get_presence(self,cr, uid, ids,empl,arg, context=None):
	
	#emp_ids= self.search(cr, uid,['|', ('employee_id', 'like', empl)],)
	#employee=self.browse(cr, uid, emp_id, context)
	 result = {}
	 for insc in self.browse(cr, uid, ids, context):
		nm=insc['employee_id'].name_related
		s1=set(nm.split(' '))	
		s2=set(empl.split(' '))

	 	if  s1 == s2:
			result[insc.id]=insc
		
	 return result

    
    def get_heures_travail(self,cr, uid,ids,field_name,arg,context=None):
		
	if (self.action_pointage == "Pointer entree"):
			heures_travail= 0.0
	else:
		#point_ids= self.search(cr,uid,[('employee_id', '=', self.employee_id),('action_pointage','like','Pointer entree')],context)
		#for p in self.browse(cr, uid, point_ids, context):
			#dtp1=time.strftime("%d/%m/%y %H:%M:%S",self.date_pointage)
			#dtp2=time.strptime(p['date_pointage'],"%Y-%m-%d %H:%M:%S")
			#dtp3=time.strptime(dtp1,"%Y-%m-%d %H:%M:%S")
		 	#if int(dtp2[0]) == int(dtp3[0]) and int(dtp2[1]) == int(dtp3[1]) and int(dtp2[2]) == int(dtp3[2]):

				#heures_travail=self.heures_travail+(p.date_pointage-self.date_pointage)
				#heures_travail=p.date_pointage-self.date_pointage
				heures_travail= 2.1
	
	return heures_travail	
			
	
	

    @api.onchange('date_pointage')
    def _onchange_presence(self):
		#now = time.localtime(time.time())
		#now=time.strftime("%d/%m/%y %H:%M:%S",time.localtime())
		#dt=time.strptime(now,"%d/%m/%y %H:%M:%S")
		d = datetime.datetime.now()
		dat=datetime.datetime(2016,05,31)
		dtp1=dat.strftime("%d/%m/%y")
		dtp=time.strptime(dtp1,"%d/%m/%y")
	        if self.type_entree:
			   # print("*******************le jour:%d",self.date_pointage.day)
		 #if 10 < 9 :
			    if 10 > 8:
			    #if (self.date_pointage.day == d.day) and (self.date_pointage.month == d.month) and (self.date_pointage.year == d.year):
				self.presence='present'
			    else:
				self.presence='toto'
	        else:
				self.presence='present'


   

    _columns = {
        'name': fields.char('ordre de presence', size=32, readonly=False),
	'employee_id': fields.many2one('hr.employee', 'Employe', change_default=True, required=True, select=1),
        'date_pointage': fields.datetime('Date pointage', required=True,select=1),
        'period_id': fields.many2one('account.period', 'Periode', select=1),
	#'id_bulletin_ma': fields.many2one('hr.payroll_ma.bulletin', 'bulletin de paie', ondelete='cascade', select=True),
	'action_pointage': fields.selection([
            ('entree', 'Pointer entree'),('sortie', 'Pointer sortie'),
             ], 'action du pointage'),
	'type_entree': fields.selection([
            ('normal', 'Normal'),('retard', 'Entrée en retard'),
             ], 'etat entrée'),
	'type_sortie': fields.selection([
            ('normal', 'Normal'),('rdv', 'RDV'),('mission', 'Mission'),
             ], 'etat sortie'),
	'presence': fields.function(check_attendance,type='char',size=64),
	'heures_travail': fields.function(get_heures_travail,type='float'),
	'employe_present':fields.function(est_present,type='datetime'),

		}

    _defaults = {
        'presence': lambda *a: 'absent',
	'heures_travail': lambda *a: 0.0,
     
    }

    
	#ids = self.search(cr, uid,
       # [ '|', ('date_pointage', '<', ),],
        #order='employee_id' )
hr_pointage_ma()

class hr_presence_ma(osv.osv):

	_name = "hr.presence.ma"

	def is_today(date_pointage):
	
		 now=time.strftime("%d/%m/%y %H:%M:%S",time.localtime())
		 dtp2=time.strptime(now,"%d/%m/%y %H:%M:%S")
		 dtp4=time.strptime(date_pointage,"%Y-%m-%d %H:%M:%S")	
	 	 if int(dtp4[0]) == int(dtp2[0]) and int(dtp4[1]) == int(dtp2[1]) and int(dtp4[2]) == int(dtp2[2]):
			return True
		
	 	 else:
			return False

	
	def get_etat_presence(self,cr, uid,ids,field_name,arg,context=None):
		emp=self.pool.get('hr.employee')
		pointage_obj=self.pool.get('hr.pointage.ma')
		#for e in emp.browse(cr, uid, ids, context):
			
		point_ids= pointage_obj.search(cr,uid,[('employee_id', '=', 1)],context)
		for p in pointage_obj.browse(cr, uid, point_ids, context):

		 		if self.is_today(p.date_pointage):
		 	
					etat_pres='present'
		
				else:
					etat_pres='absent'
		return etat_pres

	def check_etat_presence(self,cr, uid,ids,field_name,arg,context=None):
		result = dict(map(lambda x: (x,1), ids))
		emp=self.pool.get('hr.employee')
		pointage_obj=self.pool.get('hr.pointage.ma')
		emp_ids=emp.search(cr,uid,[])
		for e in emp.read(cr, uid, emp_ids,['id']):
			point_ids= pointage_obj.search(cr,uid,[('employee_id','=',e['id']),],context)
			
			for p in pointage_obj.browse(cr, uid, point_ids, context):

		 		if self.is_today(p.date_pointage):
		 	
					result[e.id]='present'
		
				else:
					result[e.id]='absent'
		return result


	def get_employee(self,cr, uid,ids,field_name,arg,context=None):
		result = dict(map(lambda x: (x,1), ids))
		emp=self.pool.get('hr.employee')
		emp_ids=emp.search(cr,uid,[])
		for e in emp.browse(cr, uid, emp_ids, context):
			result[e.id]=e.name_related
		
		return result

	_columns = {
	'employee': fields.many2one('hr.employee','Employe', change_default=True),
	#'lst_presence': fields.one2many('hr.pointage.ma','employee_id','liste des presences'),
	#'etat_presence':fields.function(get_etat_presence,type='char'),
	#'lst_employe':fields.function(get_employee,string='employee',type='char'),
	'etat_presence':fields.selection([
            ('present', 'Présent'),('absent', 'Absent'),
             ], 'etat presence'),

	'retard': fields.float('Retard', readonly=False),
	'entree': fields.datetime('Entrée', required=False,select=1),
	'sortie': fields.datetime('Sortie', required=False,select=1),
	'heures_normal': fields.float('heures normales', readonly=False),
	'heures_supp': fields.float('heures supp', readonly=False),
	#'etat_presence':fields.function(check_etat_presence,type='char'),
        	   }

	@api.onchange('employee')
    	def _onchange_presence(self,cr,uid,ids,arg,context=None):
		obj=self.pool.get('hr.pointage.ma')
		self.lst_presence=obj.get_presence(cr, uid, ids,self.employee.name_related,arg, context)
	
hr_presence_ma()			
			
			
class hr_rtpresence_ma(osv.osv):

	_name = "hr.rtpresence.ma"

	_columns = {
	'employee': fields.many2one('hr.employee','Employe', change_default=True),
	
	'etat_presence':fields.selection([
            ('present', 'Présent'),('absent', 'Absent'),
             ], 'etat presence'),

	'entree': fields.datetime('Entrée', required=False,select=1),
	'sortie': fields.datetime('Sortie', required=False,select=1),
	
        	   }
hr_rtpresence_ma()

class hr_absence_ma(osv.osv):

	_name = "hr.absence.ma"

	_columns = {
	'employee': fields.many2one('hr.employee','Employe', change_default=True),
	
	'date_debut': fields.datetime('Debut de periode', required=False,select=1),
        'date_fin': fields.datetime('Fin de periode', required=False,select=1),
	'absence_hours': fields.float('Total des heures absentés',  readonly=False),
	
        	   }
hr_absence_ma()
       
