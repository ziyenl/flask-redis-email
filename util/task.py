import jinja2

from util.mail import send_simple_message
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    """
    Render the html email template and filling in the variables
    :param template_filename: email html
    :param context: any variables
    :return: html
    """
    return template_env.get_template(template_filename).render(**context)

def send_registration_email(email, username):
    """
    Send registration email
    :param email: email.
    :param username: username
    :return: POST request
    """
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Shopify Store.",
        render_template("email/registration.html", username=username)
    )