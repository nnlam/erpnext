# ERPNext - web based ERP (http://erpnext.com)
# Copyright (C) 2012 Web Notes Technologies Pvt Ltd
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import webnotes

from webnotes.utils import cint, cstr, flt, nowdate
from webnotes.model.doc import Document
from webnotes.model.code import get_obj
from webnotes import msgprint

sql = webnotes.conn.sql
	


class DocType:
  def __init__(self, doc, doclist):
    self.doc = doc
    self.doclist = doclist   
  
  # Get Employees
  # ********************************************************************** 
  def get_employees(self):    
    lst1 = [[self.doc.employee_type,"employment_type"],[self.doc.branch,"branch"],[self.doc.designation,"designation"],[self.doc.department, "department"],[self.doc.grade,"grade"]]
    condition = "where "
    flag = 0
    for l in lst1:
      if(l[0]):
        if flag == 0:
          condition += l[1] + "= '" + l[0] +"'"
        else:
          condition += " and " + l[1]+ "= '" +l[0] +"'"
        flag = 1
    emp_query = "select name from `tabEmployee` "
    if flag == 1:
      emp_query += condition 
    e = sql(emp_query)
    return e

  # ----------------
  # validate values
  # ----------------
  def validate_values(self):
    val_dict = {self.doc.fiscal_year:'Fiscal Year', self.doc.leave_type:'Leave Type', self.doc.no_of_days:'New Leaves Allocated'}
    for d in val_dict:
      if not d:
        msgprint("Please enter : "+val_dict[d])
        raise Exception


  # Allocation
  # ********************************************************************** 
  def allocate_leave(self):
    self.validate_values()
    for d in self.get_employees():
      la = Document('Leave Allocation')
      la.employee = cstr(d[0])
      la.employee_name = webnotes.conn.get_value('Employee',cstr(d[0]),'employee_name')
      la.leave_type = self.doc.leave_type
      la.fiscal_year = self.doc.fiscal_year
      la.posting_date = nowdate()
      la.carry_forward = cint(self.doc.carry_forward)
      la.new_leaves_allocated = flt(self.doc.no_of_days)
      la_obj = get_obj(doc=la)
      la_obj.doc.docstatus = 1
      la_obj.validate()
      la_obj.on_update()
      la_obj.doc.save(1)
    msgprint("Leaves Allocated Successfully")
