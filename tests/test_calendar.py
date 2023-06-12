import unittest
from flask import render_template_string
from flask_testing import TestCase
from event_app import create_app


class CalendarTemplateTestCase(unittest.TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_calendar_template(self):
        # Test the rendering of the calendar template
        with self.app.app_context():
            # Render the template with dummy data
            rendered_template = render_template_string(
                """
                {% extends "base_layout.html" %}

                {% block title_block %}{% endblock %}

                {% block content_block %}
                  <div class="container my-5">
                    <!-- template content goes here -->
                  </div>
                {% endblock %}
                """,
                events=[],
                meetings=[],
                tasks=[]
            )

            # Add assertions to validate the rendered template
            # For example, assert that specific elements or classes are present in the rendered HTML
            self.assertIn('<div class="container my-5">', rendered_template)
            self.assertIn('container', rendered_template)
            self.assertIn('my-5', rendered_template)
            self.assertIn('<h1 align="center"><h1>Welcome {{current_user.first_name}}, this is your personal agenda</h1>', rendered_template)
            self.assertIn('Stay informed about the upcoming events and meetings!', rendered_template)
            self.assertIn('src="{{ url_for(\'static\', filename=\'images/calendar.png\') }}"', rendered_template)


if __name__ == '__main__':
    unittest.main()
