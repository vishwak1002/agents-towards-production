"""
Copyright (c) 2025 Xpander, Inc. All rights reserved.
"""
import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import cm
import shutil

def export_meeting_schedule_pdf(meetings: list) -> str:
    """
    Generate a clean, well-formatted PDF agenda for weekly meetings and save it to the user's Downloads folder.
    Returns the full path to the saved PDF.
    """
    if not meetings:
        return "No meetings provided."

    # Sort meetings by start time
    meetings.sort(key=lambda m: m.get("start_time", ""))

    # Create temporary PDF file
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_pdf.name, pagesize=A4)
    elements = []

    # Add title (no emoji)
    styles = getSampleStyleSheet()
    title = Paragraph("<b>Weekly Meeting Agenda</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Define paragraph style for table cells
    cell_style = ParagraphStyle(name='Cell', fontSize=10, leading=12, alignment=TA_LEFT)

    # Table header
    data = [["Date", "Time", "Title", "Location", "Participants"]]

    for meeting in meetings:
        try:
            start_dt = datetime.fromisoformat(meeting["start_time"])
            end_dt = datetime.fromisoformat(meeting["end_time"])
            date = start_dt.strftime("%A, %b %d")
            time = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
        except Exception:
            date = time = "Invalid"

        title = Paragraph(meeting.get("title", "Untitled"), cell_style)
        location = Paragraph(meeting.get("location", "—"), cell_style)
        attendees = meeting.get("participants") or meeting.get("attendees") or []
        participants = Paragraph(", ".join(attendees) if isinstance(attendees, list) else str(attendees), cell_style)

        data.append([date, time, title, location, participants])

    # Create and style the table
    table = Table(data, colWidths=[3.5*cm, 3*cm, 5*cm, 4*cm, 5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#6741d9")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 1), (-1, -1), 6),
        ('RIGHTPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))

    elements.append(table)
    doc.build(elements)

    # Save final PDF to Downloads
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads_path, exist_ok=True)

    filename = f"weekly_meeting_agenda_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    final_path = os.path.join(downloads_path, filename)
    shutil.copy(temp_pdf.name, final_path)

    return final_path



# Set up local tools
local_tools = [{
    "declaration": {
        "type": "function",
        "function": {
            "name": "export_meeting_schedule_pdf",
            "description": "Generate a weekly meeting agenda as a PDF from a list of meetings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "meetings": {
                        "type": "array",
                        "description": "List of meetings to include in the agenda.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Title of the meeting"
                                },
                                "start_time": {
                                    "type": "string",
                                    "description": "Start time in ISO 8601 format"
                                },
                                "end_time": {
                                    "type": "string",
                                    "description": "End time in ISO 8601 format"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Meeting location (optional)"
                                },
                                "participants": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of participant names or emails"
                                }
                            },
                            "required": ["title", "start_time", "end_time"]
                        }
                    }
                },
                "required": ["meetings"]
            }
        }
    },
    "fn": export_meeting_schedule_pdf
}
]

## Helper functions to get the list of tools and the tool by name
local_tools_list = [tool['declaration'] for tool in local_tools]
local_tools_by_name = {tool['declaration']['function']['name']: tool['fn'] for tool in local_tools}