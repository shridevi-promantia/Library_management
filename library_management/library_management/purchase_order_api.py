import frappe
import requests
from frappe.utils import nowdate, add_days

@frappe.whitelist()
def create_sales_order_from_po(po_name):

    po = frappe.get_doc("Purchase Order", po_name)

    url = "http://localhost:8000/api/resource/Sales Order"
    api_key = "2f3b4a70ee109cc"
    api_secret = "f1f7cea75f0e1e0"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"token {api_key}:{api_secret}"
    }

    # Delivery date in string format
    delivery = add_days(nowdate(), 7)

    payload = {
        "naming_series": "SAL-ORD-.YYYY.-",
        "customer": po.supplier,      # you can change this
        "order_type": "Sales",
        "transaction_date": nowdate(),
        "delivery_date": str(delivery),
        "currency": "INR",
        "selling_price_list": "Standard Selling",
        "items": [],
        "taxes": []
    }

    # Add first item
    if po.items:
        item = po.items[0]
        payload["items"].append({
            "item_code": item.item_code,
            "qty": item.qty,
            "rate": item.rate,
            "uom": item.uom,
            "delivery_date": str(item.schedule_date)
        })

    # Add first tax
    if po.taxes:
        tax = po.taxes[0]
        payload["taxes"].append({
            "charge_type": tax.charge_type,
            "account_head": tax.account_head,
            "rate": tax.rate,
            "description": tax.description
        })

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    if response.status_code != 200 or "data" not in data:
        frappe.throw(f"Sales Order creation failed: {data}")
    return data["data"]["name"]
