import frappe

@frappe.whitelist()
def hello():
    return "Hello Shridevi!"
@frappe.whitelist()
def get_book(name):
    doc = frappe.get_doc("Library Book", name)
    return doc
@frappe.whitelist()
def update_book(name=None, book_name=None, author=None, **kwargs):
    if not name:
        return "Name is required"

    doc = frappe.get_doc("Library Book", name)

    if book_name:
        doc.book_name = book_name

    if author:
        doc.author = author

    doc.save()
    return doc


@frappe.whitelist()
def create_book():
    doc = frappe.new_doc("Library Book")
    doc.book_name = "marathi book"
    doc.author = "abc"
    doc.save()
    return doc

@frappe.whitelist()
def delete_book(name):
    frappe.delete_doc("Library Book", name, force=1)
    return {"message": f"Book {name} deleted successfully"}
