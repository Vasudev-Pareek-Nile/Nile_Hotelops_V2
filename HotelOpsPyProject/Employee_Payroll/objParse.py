from datetime import datetime

def parse_dateF(date_str):
        formats = ['%d/%m/%Y', '%Y%m%d']  # List of possible formats
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt).date()
                return date_obj
            except ValueError:
                continue
        return None