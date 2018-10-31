
import json
import sys


import sendgrid
import os
from sendgrid.helpers.mail import *
RATING = 2.5

SENDGRID_API_KEY = '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'



def run_checker(scraped_movies):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("test@example.com")
    to_email = Email("14bce070@nirmauni.ac.in")
    subject = "Highly rated movies of the day"
    body = "High rated movies for today:<br><br>"
    for scraped_movie in scraped_movies:
        if  float(scraped_movie['rating']) > RATING:
            body= body+scraped_movie['name']+" Rating: " +scraped_movie['rating']+"<br>"

    content = Content("text/html", body)
 
 
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("Sent email with {} movie(s).".format(len(movies)))


if __name__ == '__main__':
    movies_json_file = "movies.json"
   with open(movies_json_file) as scraped_movies_file:
        movies = json.loads(scraped_movies_file.read())
    run_checker(movies)
