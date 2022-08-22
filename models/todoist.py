from typing import Optional

from pydantic import BaseModel

COLORS = [
    "#b8256f", "#db4035", "#ff9933", "#fad000", "#afb83b", "#7ecc49", "#299438", "#6accbc",
    "#158fad", "#14aaf5", "#96c3eb", "#4073ff", "#884dff", "#af38eb", "#eb96eb", "#e05194",
    "#ff8d85", "#808080", "#b8b8b8", "#ccac93"
]


class DueDate(BaseModel):
    """Todoist DueDate of a task."""
    date: str
    timezone: Optional[str]
    string: str
    lang: str
    is_recurring: bool


class TodoistItem(BaseModel):
    """Todoist Item (Task) model."""
    id: int
    content: str
    checked: bool
    project_id: int
    description: Optional[str] = None
    user_id: int
    in_history: int
    priority: int
    collapsed: int
    date_added: str
    date_completed: Optional[str]
    assigned_by_uid: Optional[int]
    responsble_by_uid: Optional[int]
    added_by_uid: Optional[int]
    is_deleted: bool
    sync_id: Optional[int]
    parent_id: Optional[int]
    child_order: Optional[int]
    section_id: Optional[int]
    labels: list
    notes: Optional[list]
    due: Optional[DueDate]


class TodoistProject(BaseModel):
    """Todoist Project model."""
    child_order: int
    collapsed: bool
    color: int
    has_more_notes: bool
    id: int
    inbox_project: bool = False
    is_archived: bool
    is_deleted: bool
    is_favorite: bool
    name: str
    parent_id: Optional[int]
    shared: bool
    sync_id: Optional[int]

    def color_hex(self) -> str:
        """Returns the color of the self todoist project."""
        return COLORS[self.color - 30]


class TodoistLabel(BaseModel):
    """Todoist Label model."""
    color: int
    id: int
    is_deleted: bool
    is_favorite: bool
    item_order: int
    name: str

    def color_hex(self) -> str:
        """Returns the color of the self todoist label."""
        return COLORS[self.color - 30]


class TodoistWebhookInitiator(BaseModel):
    """Todoist User model inside webhook body."""
    email: str
    full_name: str
    id: str
    image_id: Optional[str]
    is_premium: bool


class TodoistWebhook(BaseModel):
    """Todoist incoming webhook model."""
    event_name: str
    user_id: int
    event_data: TodoistItem
    initiator: TodoistWebhookInitiator
    version: str
