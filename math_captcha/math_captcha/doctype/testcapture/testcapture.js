// <yourapp>/<yourapp>/doctype/tescapture.py

// Copyright (c) 2025, hamzabawumia@yahoo.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("TestCapture", {
// 	refresh(frm) {
//
// 	},
// });



frappe.ui.form.on('TestCapture', {
    onload: function(frm) {
        // Only generate question if it's not already set
        if (!frm.doc.math_question) {
            const a = Math.floor(Math.random() * 10) + 1;
            const b = Math.floor(Math.random() * 10) + 1;

            frm.set_value('math_question', `What is ${a} + ${b}?`);
        }
    },

    validate: function(frm) {
        const user_answer = parseInt(frm.doc.math_answer);
        const question = frm.doc.math_question;

        try {
            // Expected format: "What is A + B?"
            const parts = question.split(" ");
            const a = parseInt(parts[2]);
            const b = parseInt(parts[4]);

            if ((a + b) !== user_answer) {
                frappe.throw("Incorrect math answer. Please try again.");
            }
        } catch (e) {
            frappe.throw("You need to answer the math question to show you are Human.");
        }
    }
});

