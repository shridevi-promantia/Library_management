frappe.ui.form.on("Purchase Order", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button("Create Sales Order", function() {
                frappe.call({
                    method: "library_management.library_management.purchase_order_api.create_sales_order_from_po",
                    args: {
                        po_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint("Sales Order Created: " + r.message);
                        }
                    }
                });
            });
        }
    }
});
