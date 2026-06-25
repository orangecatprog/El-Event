import markdown
import bleach
from django import template

register = template.Library()

@register.filter
def markdown_extras(text, title=None):
    if not text:
        return ""

    first_line = text.strip().split("\n")[0].strip()
    if not first_line.startswith("#"):
        text = f"# {title}\n\n{text}" if title else text

    html = markdown.markdown(text)
    
    clean_html = bleach.clean(
        html,
        tags=["p", "b", "i", "strong", "em", "ul", "li", "a", "h1", "h2", "h3", "code", "pre"],
        attributes={"a": ["href", "title"]},
        strip=True
    )


    return clean_html
