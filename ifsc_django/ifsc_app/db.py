from django.conf import settings
import pandas as pd
from ifsc_app.models import IFSC
import os


def _get_file_path(filename):
    return os.path.join(settings.BASE_DIR, filename)


def _load_xls_file():
    excel = pd.read_excel(_get_file_path(settings.XLS_FILE_NAME), sheet_name=settings.SHEETS)
    return excel


def _parse(records):
    records_dict = {}
    for record in records:
        records_dict[record["IFSC"]] = IFSC.instance(record)
    return records_dict


def _get_ifsc_dict():
    excel_file = _load_xls_file()
    ifsc_dict = {}
    for sheet in excel_file.keys():
        ifsc_dict = ifsc_dict | _parse(excel_file.get(sheet).to_dict("records"))
    return ifsc_dict


def load_in_memory():
    records = _get_ifsc_dict()
    try :
        IFSC.objects.bulk_create(records.values(),ignore_conflicts=True)
    except Exception:
        pass



