import frappe

from frappe import _


def validate(doc, method):
    pass
    # if not _is_pet_related_to(doc.patient, doc.customer):
    #     frappe.throw(_('Pet is not related to the customer'))


def _is_pet_related_to(pet, customer):
    filters = {'parent': pet, 'customer': customer}
    pet_relations = frappe.get_all('Pet Relation', filters=filters)
    return len(pet_relations) > 0


def on_submit(doc, method):
    settings = frappe.get_doc("Vetcare Settings")
    pricing_rule_name = settings.full_grooming_service_pricing_rule
    pricing_rule_items = frappe.db.get_all("Pricing Rule Item Code", filters={"parent": pricing_rule_name}, pluck="item_code")
    if doc.pricing_rules:
        for pr in doc.pricing_rules:
            if pr.pricing_rule == pricing_rule_name and pr.item_code in pricing_rule_items:
                    customer = frappe.get_doc("Customer", doc.customer)
                    customer.custom_full_service_loyalty_count = 0
                    customer.save()
                    frappe.db.commit()
    elif doc.items:
        for item in doc.items:
            if item.item_code in pricing_rule_items:
                customer = frappe.get_doc("Customer", doc.customer)
                customer.custom_full_service_loyalty_count += item.qty
                if customer.custom_full_service_loyalty_count > 5:
                    customer.custom_full_service_loyalty_count = 5
                customer.save()
                frappe.db.commit()

              
