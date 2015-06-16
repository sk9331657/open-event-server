"""Copyright 2015 Rafal Kowalski"""
import datetime
import unittest
import logging
from setup_database import Setup

from open_event import app
from open_event.models import db
from open_event.models.track import Track
from open_event.models.event import Event


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def tearDown(self):
        Setup.drop_db()

    def test_api_tracks(self):
        ev = Event(name="event1", start_time=datetime.datetime(2003, 8, 4, 12, 30, 45), end_time=datetime.datetime(2003, 8, 4, 12, 30, 45))
        tr = Track(name="name", event_id=1, description="description")
        with app.app_context():
            db.session.add(ev)
            db.session.add(tr)
            try:
                db.session.commit()
            except Exception as error:
                logging.error(error)
        self.assertEqual(self.app.get('/admin/event/1').status_code, 200)
        self.assertEqual(self.app.get('/admin/event/1/track').status_code, 200)

if __name__ == '__main__':
    unittest.main()