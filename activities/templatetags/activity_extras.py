from django import template

register = template.Library()

@register.filter(name='format_effort')
def format_effort(value):
    #Formats distance or duration
    try:
        val = float(value)
        return f"{val:.1f} km"
    except (ValueError, TypeError):
        return "0.0 km"


@register.filter(name='workout_intensity')
def workout_intensity(distance):

    #Returns an intensity label based on workout distance.
    try:
        dist = float(distance)
        if dist >= 20.0:
            return "Ultra Endurance"
        elif dist >= 10.0:
            return "High Intensity"
        elif dist >= 5.0:
            return "Moderate"
        return "Light Session"
    except (ValueError, TypeError):
        return "Standard"