import datetime
import uuid

ICS_FILE = "Erindale_Shifts2.ics"

def add_event(date_str, time_str):
    """
    date_str format: "DD MM" (e.g. "24 08" -> 24th August)
    time_str format: "HHMM-HHMM" (e.g. "1600-1900")
    """

    # Parse date
    day, month = map(int, date_str.split())
    year = datetime.datetime.now().year  # use current year
    start_time, end_time = time_str.split("-")
    
    # Parse times
    start_hour, start_minute = int(start_time[:2]), int(start_time[2:])
    end_hour, end_minute = int(end_time[:2]), int(end_time[2:])
    
    # Build datetime objects
    start_dt = datetime.datetime(year, month, day, start_hour, start_minute)
    end_dt = datetime.datetime(year, month, day, end_hour, end_minute)

    # Format for ICS (local Australia/Adelaide time)
    dtstart_str = start_dt.strftime("%Y%m%dT%H%M%S")
    dtend_str = end_dt.strftime("%Y%m%dT%H%M%S")
    dtstamp_str = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    uid_str = f"{uuid.uuid4().int}@ical.marudot.com"

    # Event template
    event = f"""
BEGIN:VEVENT
DTSTAMP:{dtstamp_str}
UID:{uid_str}
DTSTART;TZID=Australia/Adelaide:{dtstart_str}
DTEND;TZID=Australia/Adelaide:{dtend_str}
SUMMARY:Work - Erindale
LOCATION:Erindale Chicken & Seafood 365 Kensington Rd\\, Kensington Gardens SA 5068\\, Australia
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Work - Erindale
TRIGGER:-PT30M
END:VALARM
END:VEVENT
"""

    # Insert before END:VCALENDAR
    with open(ICS_FILE, "r", encoding="utf-8") as f:
        ics_content = f.read()

    new_content = ics_content.replace("END:VCALENDAR", event + "END:VCALENDAR")

    with open(ICS_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ Event added successfully!")


# Example usage:
add_event("27 09", "1600-1900")
