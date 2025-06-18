
USE CASE:
"""
Self Registration by Users
SEE GOOD WORKING EXAMPLES in africahomecare app and repherod app.
"""

AIM:
"""
To setup a math_capture for frappe just like django-math-capture so that outside users can self register on a website or app.
"""

ARCHITECTURAL PLAN:
"""
STEP 1 : 
Create a doctype/model called "registration"
This doctype has fields for  [
 "i_am_a_",
  "email",
  "first_name",
  "last_name",
  "phone_number",
  "password",
  "confirm_password",
  "math_question",
  "math_answer",
  "math_captcha",
]

The doctype.py will import the mixin
and contain the ff code: - which will provide server side validation
for the from and if valid will create a user account 
for the new user in the frappe core User doctype.

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

        # Create the user
        user = frappe.get_doc({
            "doctype": "User",
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone_number,
            "send_welcome_email": 1,
            "enabled": 1,
            "new_password": self.password,  # Optional: only if you want to set it directly
            "roles": [{"role": selected_role}]  # ✅ Assign role during creation
        })

        user.flags.ignore_password_policy = True  # <-- Bypass password strength validation

        user.insert(ignore_permissions=True)


        frappe.db.commit()  # Commit to make sure user is created

STEP 2: Create a webform to allow the user to Register.

The webform will have the fields from the "registration" doctype.
The webform.js file (register.js) will have the following code to provide client side validation:

frappe.ready(function () {
	console.log("✅ Web Form JS loaded successfully!");

	if (!frappe.web_form) {
		console.error("❌ frappe.web_form not available.");
		return;
	}

	const interval = setInterval(() => {
		if (frappe.web_form.doc) {
			console.log("📌 Web Form is fully loaded");

			// frappe.msgprint('Please fill all values carefully');

			// Set math question if not already present
			if (!frappe.web_form.doc.math_question) {
				const a = Math.floor(Math.random() * 10) + 1;
				const b = Math.floor(Math.random() * 10) + 1;
				const question = `What is ${a} + ${b}?`;
				frappe.web_form.set_value('math_question', question);
			}

			// Safe validation without throwing error
			frappe.web_form.validate = () => {
				const question = frappe.web_form.doc.math_question;
				const user_answer = parseInt(frappe.web_form.doc.math_answer);

				if (!question || isNaN(user_answer)) {
					frappe.msgprint("You need to answer the math question to prove you are human.");
					frappe.validated = false;
					return;
				}

				const parts = question.split(" ");
				if (parts.length < 5) {
					frappe.msgprint("Invalid math question format.");
					frappe.validated = false;
					return;
				}

				const a = parseInt(parts[2]);
				const b = parseInt(parts[4]);

				if ((a + b) !== user_answer) {
					frappe.msgprint("Incorrect math answer. Please try again.");
					frappe.validated = false;
					return;
				}
			};

			clearInterval(interval);
		}
	}, 100);
});

"""

User Navigation / nav_links:
"""
When a user navigates to the login page, they also get a link to register.
Where is the code located ?
So it is located @ /home/hamza/frappe-bench/apps/frappe/frappe/www/login.html
i.e. we edit the login.html and add the code to navigate to the register page.

"""

URL:
"""
href="/register" (since this the name we gave our webform)
"""

View:
"""

"""

Template:
"""

"""

Models Involved:
"""
registration model / doctype - it has no foreignkey link to any other model 
It is a flat model.
"""

# Start implementing the use case logic here
