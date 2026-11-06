"""Pure scheduling policy for manual overrides and teaser mode."""
from datetime import timedelta
from logic import automatic_open, next_boundary


def planned_state(now,rows,tz,auto_enabled,manual_open_until=None,manual_closed_until=None):
    if manual_closed_until and now < manual_closed_until:
        return False
    if manual_open_until and now < manual_open_until:
        return True
    return bool(auto_enabled and automatic_open(now,rows,tz))


def teaser_boundary(now,rows,tz):
    """Return a just-started opening slot, once per actual boundary."""
    candidate=next_boundary(now-timedelta(seconds=90),rows,'open',tz)
    if candidate and 0 <= (now-candidate).total_seconds() < 90:
        return candidate
    return None
