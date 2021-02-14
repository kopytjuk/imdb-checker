import os
import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from celery_tasks import run_imdb_user_watchlist_check, run_imdb_top_250_check, get_state_by_id,\
    get_result_by_id
from logic.notifier import send_notification
from logic.datatypes import Results, UserRequest, TaskInfo, UserMessage


LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOG_LEVEL)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get('/alive', response_class=HTMLResponse)
async def alive():
    return 'I am alive!'


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/impressum", response_class=HTMLResponse)
async def impressum(request: Request):
    return templates.TemplateResponse("impressum.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.post("/check")
async def check_imdb_list(req: UserRequest):

    method = req.method
    location_code = req.location_code

    if method == "imdb_watchlist":
        url = req.url
        task = run_imdb_user_watchlist_check.delay(url, location_code)
    elif method == "imdb_top_250":
        task = run_imdb_top_250_check.delay(location_code)
        url = "https://www.imdb.com/chart/top/"  # only for print message

    task_id = task.id

    if LOG_LEVEL > logging.DEBUG:
        send_notification("Someone checks %s with task_id=%s" % (url, str(task_id)))

    return {"task_id": task_id}


@app.post('/get_state')
async def get_state(state: TaskInfo):

    task_id = state.task_id

    # app.logger.info("Checking state of '%s'" % task_id)
    logging.debug("Checking state of '%s'" % task_id)

    state, message = get_state_by_id(task_id)
    return {"state": state, "message": message}


@app.post('/get_result', response_model=Results)
async def get_result(state: TaskInfo):

    task_id = state.task_id

    res = get_result_by_id(task_id)
    if LOG_LEVEL > logging.DEBUG:
        send_notification(
            "Successfully provided result of task_id='%s'" % task_id)

    return {"result": res["result"]}


@app.post('/send_message')
async def message(message: UserMessage):

    message_str = "Name: {name:s}\nE-Mail: {email:s}\nReason: {reason:s}\n" \
        "Message:\n\n{message:s}".format(**{
            "name": message.name,
            "email": message.email,
            "reason": message.reason.name,
            "message": message.message
        })

    send_notification(message_str)

    logging.info(message_str)
    return {"message": True}
