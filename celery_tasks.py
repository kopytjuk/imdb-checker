import time
from multiprocessing import Value

from celery import Celery
from celery.states import FAILURE

from logic.watchlist_checker import check

from logic.config import CELERY_BROKER_URL as broker_url
from logic.config import CELERY_RESULT_URL as result_url
from logic.config import CELERY_BROKER_POOL_LIMIT as broker_pool_limit


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
def run_check(self, url: str, location_code: str) -> dict:

    pt = ProgressTracker(self)

    pt.info("Starting ...")

    url_to_check: str = url

    user_location: str = location_code

    url_to_check = url_to_check.strip()

    response_dict = {"result": None}

    if not url_to_check.startswith("https://www.imdb.com/"):
        self.update_state(state=FAILURE)
    else:
        response_dict["result"] = check(url_to_check, user_location, pt)
    
    pt.info("Finalizing ...")

    return response_dict


@app.task
def wait(seconds: int):
    time.sleep(seconds)

    return "Waited for %d seconds!" % int(seconds)


def get_state_by_id(id: str) -> bool:
    job = app.AsyncResult(id)
    state = job.state

    message = ""
    if state == "PROGRESS":
        info = job.info
        message = info["message"]
    return state, message


def get_result_by_id(id: str) -> dict:
    result = app.AsyncResult(id)
    print("Trying to get results from '%s'" % id)
    return result.get(timeout=10)