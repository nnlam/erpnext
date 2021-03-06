wn.query_reports["Bank Reconciliation Statement"] = {
	"filters": [
		{
			"fieldname":"account",
			"label": "Bank Account",
			"fieldtype": "Link",
			"options": "Account",
			"get_query": function() {
				return {
					"query": "accounts.utils.get_account_list", 
					"filters": {
						"is_pl_account": "No",
						"account_type": "Bank or Cash"
					}
				}
			}
		},
		{
			"fieldname":"report_date",
			"label": "Date",
			"fieldtype": "Date",
			"default": get_today()
		},
	]
}