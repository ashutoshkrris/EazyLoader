from core import app

@app.template_filter('humanize_duration')
def humanize_duration(seconds):
    """Converts seconds into HH:MM:SS"""
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if hour > 0:
        return "%d:%02d:%02d" % (hour, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)

@app.template_filter('humanize_views')
def humanize_views(views):
    str_views = len(str(views))
    if str_views <= 3:
        return views
    elif str_views <= 6:
        return f"{round(views/1000,1)}K"
    elif str_views <= 9:
        return f"{round(views/1000000, 1)}M"
    else:
        return f"{round(views/1000000000,1)}B"

@app.template_filter('humanize_date')
def humanize_date(date):
    return date.strftime("%b %d, %Y")
