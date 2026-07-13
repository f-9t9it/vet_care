frappe.ui.form.on('Sales Invoice', {
    onload: function(frm) {
        _get_show_zip_code().then((show_zip_code) => {
            // read only fields can't be set through set_df_property
            if (!show_zip_code) {
                $('div[title="vc_zip_code"]').hide();
            }
        });
    },
    refresh: function(frm) {
        _set_zip_code(frm);
    },
    patient: function(frm) {

    },
    validate:function(frm)
    {
        calculate_full_service_loyalty(frm);
    }
});


async function _set_zip_code(frm) {
    const { message: customer } = await frappe.db.get_value('Customer', frm.doc.customer, 'vc_zip_code');
    setTimeout(() => frm.fields_dict.vc_zip_code.set_input(customer.vc_zip_code), 150);
}


async function _get_show_zip_code() {
    const show_zip_code = await frappe.db.get_single_value('Vetcare Settings', 'show_zip_code');
    return show_zip_code;
}


frappe.ui.form.on("Sales Invoice Item", {
    item_code: function(frm, cdt, cdn) {
        calculate_full_service_loyalty(frm);
    },

    qty: function(frm, cdt, cdn) {
        calculate_full_service_loyalty(frm);
    }
});

function calculate_full_service_loyalty(frm) {
    if (!frm.doc.customer) return;

    frappe.call({
        method: "vet_care.doc_events.sales_invoice.return_items_full_service_loyalty",
        args: {
            doc: frm.doc
        },
        callback: function(r) {
            if (!r.message) return;

            let loyalty_items = r.message.items || [];
            let customer_count = r.message.full_service_loyalty_count || 0;

            console.log(r.message);
            let item_set = new Set(loyalty_items);

            let total_qty = 0;

            (frm.doc.items || []).forEach(row => {
                if ((item_set.has(row.item_code) && row.discount_amount == 0) && row.is_free_item != 1) {
                    total_qty += flt(row.qty);
                }
            });

            let total_loyalty = customer_count + total_qty;

            frm.set_value(
                "custom_full_service_loyalty_count",
                total_loyalty
            );
        }
    });
}