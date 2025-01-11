from services.BaseService import BaseService

class ReportGenService(BaseService):
    def __init__(self):
        print(f"Initialized report generation service")

    def generate_report(self, conversation, enable_report=False):
        if enable_report:
            return "Generated report for conversation: {}".format(conversation)
        else:
            return ""