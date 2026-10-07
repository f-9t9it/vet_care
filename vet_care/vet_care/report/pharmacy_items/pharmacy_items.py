# Copyright (c) 2026, 9T9IT and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	data = []
	columns = [
		{
			"fieldname": "name",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname": "item_name",
			"label": "Item Name",
			"fieldtype": "Data",
			
		},
		{
			"fieldname": "image",
			"label": "Image",
			"fieldtype": "HTML",
			
		},
		{
			"fieldname": "medicine_name",
			"label": "Medicine Name",
			"fieldtype": "Data",
			
		},
		{
			"fieldname": "medicine_group",
			"label": "Medicine Group",
			"fieldtype": "Link",
			"options": "Medicine Group"
		},
		{
			"fieldname": "active_ingredient",
			"label": "Active Ingredient",
			"fieldtype": "Small Text",
			
		},
		{
			"fieldname": "concentration",
			"label": "Concentration",
			"fieldtype": "Data",
			
		},
		{
			"fieldname": "packaging",
			"label": "Packaging",
			"fieldtype": "Data",
		},
		{
			"fieldname": "wholesale_price",
			"label": "Wholesale Price",
			"fieldtype": "Currency",
		},
		{
			"fieldname": "retail_price",
			"label": "Retail Price",
			"fieldtype": "Currency",
		}

	]
	if filters.get("warehouse"):
		columns.append({
			"fieldname": "stock",
			"label": "Stock",
			"fieldtype": "Float",
		})
	group_by = ''
	item_filters = {"custom_pharmacy_item":1}
	if filters.get("medicine_group"):
		item_filters["custom_medicine_group"] = filters.get("medicine_group")
	if filters.get("item_group"):
		item_filters["item_group"] = filters.get("item_group")
	if filters.get("item_code"):
		item_filters["name"] = filters.get("item_code")
	if filters.get('group_by_medicine_group'):
		group_by = 'medicine_group'
	items = frappe.db.get_all("Item", filters=item_filters, fields=["name", "stock_uom", "item_name", "image", "custom_medicine_name as medicine_name", "custom_medicine_group as medicine_group", "custom_active_ingredient as active_ingredient", "custom_concentration as concentration", "custom_package as packaging"], group_by=group_by)	
	data = []
	for item in items:
		item["image"] = f'<img src="{frappe.utils.get_url()}{item["image"]}" width="50" height="100">' if item["image"] else ""
		item['wholesale_price'] = frappe.db.get_value("Item Price", {"item_code": item['name'], "buying":1, "uom": item['stock_uom'],"price_list":"Wholesale Price"}, "price_list_rate") or 0
		item['retail_price'] = frappe.db.get_value("Item Price", {"item_code": item['name'], "selling":1, "uom": item['stock_uom'],"price_list":"Pharmacy Prices"}, "price_list_rate") or 0
		if filters.get("warehouse"):
			item['stock'] = frappe.db.get_value("Bin", {"item_code": item['name'], "warehouse": filters.get("warehouse")}, "actual_qty") or 0
		data.append(item)
	return columns, data
