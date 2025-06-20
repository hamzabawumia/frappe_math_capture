# Copyright (c) 2025, hamza bawumia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import random_string

from .math_captcha_mixin import MathCaptchaMixin

class registration(MathCaptchaMixin):

    def after_insert(self):
        self.ensure_roles_exist()
        self.create_user()

    def ensure_roles_exist(self):
        """Make sure Doctor, Nurse, and Patient roles exist."""
        roles = ["Doctor", "Nurse", "Patient"]
        for r in roles:
            if not frappe.db.exists("Role", r):
                frappe.get_doc({"doctype": "Role", "role_name": r}).insert(ignore_permissions=True)

    def create_user(self):
        # Check if user already exists
        if frappe.db.exists("User", self.email):
            frappe.throw("A user with this email already exists.")

        # Assign role based on i_am_a_ value
        role_map = {
            "Doctor": "Doctor",
            "Nurse": "Nurse",
            "Patient": "Patient"
        }

        selected_role = role_map.get(self.i_am_a_)

        if not selected_role:
            frappe.throw("Invalid role selection.")


# since we are using a Password field in the repherod_registration doctype,
# Frappe automatically hashes the value stored in a Password field before saving to the database.
#
# So when you do:
#
# "new_password": self.password
# You are actually assigning a hashed password to new_password,
# and Frappe hashes it again, which breaks the login.
#
# To prevent the above issue, you need to decrypt the password first.

        # 🔐 Get decrypted password from the field
        plain_password = self.get_password("password")


        # Create the user
        user = frappe.get_doc({
            "doctype": "User",
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone_number,
            "send_welcome_email": 1,
            "enabled": 1,
            "new_password": plain_password,  # Optional: only if you want to set it directly
            "roles": [{"role": selected_role}]  # ✅ Assign role during creation
        })

        user.flags.ignore_password_policy = True  # <-- Bypass password strength validation

        user.insert(ignore_permissions=True)


        frappe.db.commit()  # Commit to make sure user is created

