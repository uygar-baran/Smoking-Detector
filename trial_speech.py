import os
import time
import speech_recognition as sr
import argparse
import smtplib

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print(
            "The sentence above has a sentiment score of {}".format(sentence_sentiment)
        )

    return score


def analyze(content):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    document = types.Document(content=content, type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    return print_result(annotations)

def sendemail(to_whom):
	# variables
	user_name = "Brian"
	sponsor_name = "Jake"
	gender = "him"
	sender_email = "hack2020send@gmail.com"
	rec_email = "hack2020recieve2@gmail.com"
	password = "hack2020"

	if to_whom == 'user':
		message = "Subject: Smoke Detector\n\nHey {},\n\nIt's normal to not succeed the first few times you try to quit. Most people understand this, and know that they have to try to quit again. Know that we believe in you.".format(user_name)
		rec_email = "hack2020recieve@gmail.com"
	else:
	 	message = "Subject: Smoke Detector\n\nDear {},\n\nThis email is to notify you that {} has been having the urges to relapse recently. Please reach out to {} as soon as possible to support {}.".format(sponsor_name, user_name, user_name, gender)

	# establishes connection to simple mail transfer protocol
	server = smtplib.SMTP('smtp.gmail.com', 587)

	server.starttls()
	server.login(sender_email, password)
	server.sendmail(sender_email, rec_email, message)
	print("Email sent!!!!!!!!")
	server.quit()

def get_audio():
	sum = 0 # overall sentiment
	score = 0 # single line score
	flag = 0 # for e-mails

	r = sr.Recognizer()

	with sr.Microphone() as source:
		while True:
			audio = r.listen(source)
			said = ""

			try:
				said = r.recognize_google(audio)
				print(said)
				said.lower()
				score = analyze(said)

				# keywords that trigger the system immediately
				bad_words = ['smoke', 'cigarette', 'smoking', 'cigar']
				if any(x in said for x in bad_words):
					print("\nKeyword Found!\n")
					sum = -3
					score = 0

				# sum calculations
				if score < 0:
					sum += score
				else:
					sum += score / 2
				print("Overall Sentiment: overall score is {}. ".format(sum))

			# if microphone does not pick up any sound
			except Exception as e:
				print("Exception: " + str(e))

			# if threshold has been passed (email user)
			if sum <= -2 and flag == 0:
				print("emailing the user...")
				sendemail('user')
				flag = 1

			# if threshold has been passed (email family)
			if sum <= -3:
				print("emailing the family...")
				sendemail('family')
				sum = sum / 8
				flag = 0
		return said


if __name__ == "__main__":
    get_audio()
