
from unisos.wsf import wsf_config

def log(s):
    """Log with the scraping context."""
    print(f"{wsf_config.params.scrapingName}: {s}")


def tagHasClassname(
        tag, # bs4.element.Tag
        classname: str,
) -> bool:
    """True if `tag` has a class `classname`, False otherwise."""

    if not tag.attrs:
        return False

    elif 'class' not in tag.attrs:
        return False

    else:
        return classname in tag.attrs['class']

