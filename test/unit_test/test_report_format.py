"""
test different report formats of the report
"""
import json
from src.format_report import format_report
import re

def is_valid_html(html_string):
    """
    check if the string is a valid html/xml string
    """
 
    # Regex to check valid
    # HTML tag using regex.
    regex = "<(\"[^\"]*\"|'[^']*'|[^'\">])*>"
     
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if html_string is None:
        return False
 
    # Return if the string
    # matched the ReGex
    if re.search(p, html_string) is not None:
        return True
    return False

def test_invalid_format():
    json_report = format_report({
        "status": "fail",
        "reason": "Please provide a valid API key in the header."
    }, "abc")
    assert json_report == json.dumps({
        "status": "fail",
        "reason": "Please provide a valid API key in the header."
    })

def test_html_report():
    html_report = format_report({
        "status": "fail",
        "reason": "Please provide a valid API key in the header."
    }, "html")
    assert is_valid_html(html_report)

def test_xml_report():
    xml_report = format_report({
        "status": "fail",
        "reason": "Please provide a valid API key in the header."
    }, "xml")
    assert is_valid_html(xml_report)

def test_html_list_of_dicts():
    html_reports = format_report([
        {
            "status": "fail",
            "reason": "Please provide a valid API key in the header."
        },
        {
            "status": "fail",
            "reason": "bad request"
        }
    ], "html")
    assert is_valid_html(html_reports)

def test_xml_list_of_dicts():
    xml_reports = format_report([
        {
            "status": "fail",
            "reason": "Please provide a valid API key in the header."
        },
        {
            "status": "fail",
            "reason": "bad request"
        }
    ], "xml")
    assert is_valid_html(xml_reports)