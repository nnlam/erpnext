import webnotes

def execute():
	webnotes.reload_doc("core", "doctype", "patch_log")
	if webnotes.conn.table_exists("__PatchLog"):
		for d in webnotes.conn.sql("""select patch from __PatchLog"""):
			webnotes.doc({
				"doctype": "Patch Log",
				"patch": d[0]
			}).insert()
	
		webnotes.conn.commit()
		webnotes.conn.sql("drop table __PatchLog")