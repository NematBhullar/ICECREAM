"""
provide functions to format the report to different formats.
"""
from json2html import json2html
from dict2xml import dict2xml
import json

def format_report(report: dict, format_type: str) -> str:
    """
    format the report accordingly. If the format is not html or xml, it returns
    in json format.

    Arguments:
        report (dict)               - the report dictionary to return to the 
                                     sender
        format (str)                - the format of the report.
                                     It can be 'html', 'xml' or 'json'. 
                                     Anything else will be treated as json.
    Return Value:
        str                         - the report in the specified format
    """
    if format_type == 'html':
        return json2html.convert(json=report)
    elif format_type == 'xml':
        return ('<?xml version="1.0" encoding="UTF-8"?>' 
            + dict2xml(report, wrap='send_invoice_report'))
    return json.dumps(report)
