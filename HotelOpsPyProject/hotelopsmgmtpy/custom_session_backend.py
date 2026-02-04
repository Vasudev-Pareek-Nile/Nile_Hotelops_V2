from django.contrib.sessions.backends.db import SessionBase


class CustomSessionBackend(SessionBase):
    def create(self):
        """
        Create a new session ID and store it in the database.
        """
        self._session_key = 'my_custom_session_id'
        self.save(must_create=True)
