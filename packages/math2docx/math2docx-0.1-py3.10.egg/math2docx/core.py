import mathml2omml
import latex2mathml.converter
from docx.oxml import parse_xml


def convert(latex_content: str):
  mathml_content = latex2mathml.converter.convert(latex_content)
  omml_content = mathml2omml.convert(mathml_content)
  results = (
    f'<p xmlns:m="http://schemas.openxmlformats.org/officeDocument'
    f'/2006/math">{omml_content}</p>'
  )
  return parse_xml(results)[0]
