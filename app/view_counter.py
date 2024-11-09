import threading
import time

from functools import wraps

DURATION_IN_SECONDS_BEFORE_VIEW_EXPIRES = 3

class ViewCounter():
    def __init__(self):
        self.views = 0

    def get_views(self):
        return self.views

    def add_view(self):
        self.views += 1

    def delete_view(self):
        self.views -= 1

    def expire_view(self):
        time.sleep(DURATION_IN_SECONDS_BEFORE_VIEW_EXPIRES)
        self.delete_view()

    def add_expiring_view(self):
        self.add_view()
        threading.Thread(target=self.expire_view).start()

def add_view_count(view_function):
    view_counter = ViewCounter()

    @wraps(view_function)
    def wrapper(*args, **kwargs):
        view_counter.add_expiring_view()
        return view_function(view_count=view_counter.get_views(), *args, **kwargs)

    return wrapper
