class EmailTemplates:
    def __init__(self):
        file = open("templates/index.html", "r")
        self.basic_template = file.read()

        file = open("templates/error.html", "r")
        self.error_template = file.read()

    def generate_basic_template(self, entries: dict) -> str:
        return self.basic_template.format(to_name=entries["to_name"], certs=entries["certs"])

    def generate_error_template(self, entries: dict) -> str:
        return self.error_template.format(to_name=entries["to_name"], error_message=entries["error_message"])

    def generate_cert_list(self, results: list) -> str:
        html = "<h4>Expiring Certs:</h4>"
        html = html + "<ul>"

        for result in results:
            html = html + "<li>" + result[0] + "</li>"

        html = html + "</ul>"

        return html
