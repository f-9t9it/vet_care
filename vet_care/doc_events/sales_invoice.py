import frappe

from frappe import _


def validate(doc, method):
    if doc.pos_profile:
        doc.pb_set_cost_center = frappe.db.get_value("POS Profile", doc.pos_profile, "cost_center")
    # if not _is_pet_related_to(doc.patient, doc.customer):
    #     frappe.throw(_('Pet is not related to the customer'))


def _is_pet_related_to(pet, customer):
    filters = {'parent': pet, 'customer': customer}
    pet_relations = frappe.get_all('Pet Relation', filters=filters)
    return len(pet_relations) > 0
