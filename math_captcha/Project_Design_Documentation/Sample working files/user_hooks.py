# IF NEEDED: This file is used to create the user profile it is inserted into the hooks.py file
# like so:
#
#
# doc_events = {
#
#     "User": {
#         "after_insert": "repherod.user_hooks.create_user_profile"
#             # located in the repherod base directory alongside hooks.py
#     }


import frappe

def create_user_profile(doc, method):
    # Check if profile already exists (shouldn't happen on insert, but safe check)
    if not frappe.db.exists("Repherod User Profile", {"user_id": doc.name}):
        # here doc.name is the doc that was passed to this function

        frappe.get_doc({
            "doctype": "Repherod User Profile",

            "user_id": doc.name,
            "first_name": doc.first_name,
            "last_name": doc.last_name,
            "phone_number": doc.phone,
            # the core User doctype in frappe has the attribute "phone" not phone_number
            
        }).insert(ignore_permissions=True)
