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
