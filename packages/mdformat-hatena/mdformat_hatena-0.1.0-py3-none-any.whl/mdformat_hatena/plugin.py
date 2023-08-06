from mdformat.renderer import _context


HARD_BR = '<br data-shodo="1">'


def update_mdit(mdit):
    pass


def softbreak(node, context):
    if context.options.get("mdformat", {}).get("breaks", False):
        return f"{HARD_BR}\n"
    else:
        return "\n"


def hardbreak(node, context):
    # はてなでは \ での改行挿入ができない
    return f"{HARD_BR}\n"


def paragraph(node, content):
    body = _context.paragraph(node, content)
    return body.replace(HARD_BR, "  ")


def text(node, context):
    # [asign:...] などを保護するためエスケープをしない
    return node.content


RENDERERS = {
    "softbreak": softbreak,
    "hardbreak": hardbreak,
    "text": text,
    "paragraph": paragraph,
}
