import frappe
from frappe.model.document import Document
from resume_parser.utils.parser_utils import parse_resume


class Resume(Document):

    def after_insert(self):
        if self.resume_file:
            self.process_resume()

    def process_resume(self):
        try:
            self.status = "Processing"
            self.save(ignore_permissions=True)

            file_doc = frappe.get_doc("File", {"file_url": self.resume_file})
            file_path = file_doc.get_full_path()

            result = parse_resume(file_path)

            self.skills = result.get("skills")
            self.score = result.get("score")
            self.status = "Processed"

        except Exception:
            frappe.log_error(frappe.get_traceback(), "Resume Parsing Failed")
            self.status = "Failed"

        self.save(ignore_permissions=True)
