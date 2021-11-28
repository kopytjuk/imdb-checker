import time
from multiprocessing import Value
from typing import Tuple, List

from celery import Celery

from logic.main import check_imdb_user_watchlist, check_imdb_top_250_movies
from logic.config import default_config
from logic.datatypes import ResultElement

broker_url = default_config.CELERY_BROKER_URL
result_url = default_config.CELERY_RESULT_URL
broker_pool_limit = default_config.CELERY_BROKER_POOL_LIMIT

print("Using %s for broker." % broker_url[:20])

app = Celery('celery_tasks', broker_url=broker_url, backend=result_url)
app.conf.update(broker_pool_limit=int(broker_pool_limit))


class ProgressTracker:

    def __init__(self, task):
        self._task = task
        self._progress = None
        self._total = None
        self._message = ""

    def start_work(self, message: str, total: int):
        self._progress = Value('i', 0)
        self._message = message
        self._total = total
        self.update()

    def info(self, message: str):
        self._message = message
        self._total = None
        self.update()

    def progress(self, i: int):
        self._progress.value += i
        self.update()

    def update(self):
        message = self._message
        if self._total:
            message = "%s %d/%d" % (self._message, self._progress.value, self._total)
        self._task.update_state(state="PROGRESS", meta={"message": message})


@app.task(bind=True)
def run_imdb_user_watchlist_check(self, url: str, location_code: str) -> dict:

    pt = ProgressTracker(self)

    pt.info("Starting ...")

    url = url.strip()

    response_dict = {"result": None}

    response_dict["result"] = check_imdb_user_watchlist(url, location_code, pt)

    pt.info("Finalizing ...")

    return response_dict


@app.task(bind=True)
def run_imdb_top_250_check(self, location_code: str) -> dict:

    pt = ProgressTracker(self)

    pt.info("Starting ...")

    response_dict = {"result": []}

    response_dict["result"] = check_imdb_top_250_movies(location_code, pt)

    pt.info("Finalizing ...")

    return response_dict


@app.task(bind=True)
def check_medialist(self, name: str, location_code: str) -> dict:

    # medialist = get_list

    pt = ProgressTracker(self)

    pt.info("Starting ...")

    response_dict = {"result": []}

    pt.info("Finalizing ...")

    return response_dict


def get_state_by_id(id: str) -> Tuple[str, str]:
    """Return current task state by id.

    Args:
        id (str): task id

    Returns:
        Tuple[str, str]: state and message
    """

    job = app.AsyncResult(id)
    state = job.state

    message = ""
    if state == "PROGRESS":
        info = job.info
        message = info["message"]
    elif state == "FAILURE":
        error = job.info
        message = str(error)
    return state, message


def get_result_by_id(id: str) -> List[ResultElement]:
    result = app.AsyncResult(id)
    print("Trying to get results from '%s'" % id)
    return result.get(timeout=10)


# small example for Celery
@app.task
def wait(seconds: int):
    time.sleep(seconds)
    return "Waited for %d seconds!" % int(seconds)
