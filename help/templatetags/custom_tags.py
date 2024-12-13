from django import template

register = template.Library()

@register.filter
def render_stars(rating):
    """
    Converts a numeric rating into a string of stars (HTML).
    """
    try:
        full_stars = int(rating)  # Number of full stars
        half_star = 1 if rating - full_stars >= 0.5 else 0  # Half star if applicable
        empty_stars = 5 - full_stars - half_star  # Remaining stars to make it 5

        # Generate star icons
        stars_html = ('<i class="fas fa-star text-warning"></i>' * full_stars +
                      '<i class="fas fa-star-half-alt text-warning"></i>' * half_star +
                      '<i class="far fa-star text-warning"></i>' * empty_stars)
        return stars_html
    except (ValueError, TypeError):
        return '<i class="far fa-star text-warning"></i>' * 5  # Default 5 empty stars for invalid input