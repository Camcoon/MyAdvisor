from fastapi import APIRouter, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import get_settings
from app.dependencies.auth import get_current_user
from app.utilities.flash import get_flashed_messages

template_env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
template_env.globals['get_flashed_messages'] = get_flashed_messages
templates = Jinja2Templates(env=template_env)
static_files = StaticFiles(directory="app/static")

router = APIRouter(tags=["Jinja Based Endpoints"], include_in_schema=get_settings().env.lower() in ["dev","development"])
api_router = APIRouter(
    tags=["API Endpoints"], prefix="/api", dependencies=[Depends(get_current_user)]
)

from . import (
    admin_home as admin_home,
)
from . import (
    index as index,
)
from . import (
    login as login,
)
from . import (
    logout as logout,
)
from . import (
    register as register,
)
from . import (
    server_config as server_config,
)
from . import (
    user_home as user_home,
)
from . import (
    users as users,
)
from . import (
    advising_api as advising_api,
)
