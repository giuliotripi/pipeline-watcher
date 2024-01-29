import os
import time

import requests
import datetime
import pytz

'''

'''

ultimoStato = {}

BASE_URL = os.getenv("PIPELINE_MONITOR_URL")

PROJECT_IDS = []

USER: str | None = None


def main():
	dataStr = datetime.datetime.now().strftime("%Y-%m-%dT00:00:00")

	reqUrl = BASE_URL + "/jobs?since=" + dataStr

	for projectId in PROJECT_IDS:
		reqUrl += "&projectId=" + projectId

	if USER is not None:
		reqUrl += "&user=" + USER

	print(reqUrl)

	r = requests.get(reqUrl)

	for job in r.json():

		dtStart = datetime.datetime.strptime(job['dtStart'], "%Y-%m-%dT%H:%M:%S.%f%z")

		pipelineId = job['pipelineId']
		jobId = job['id']
		jobName = job['name']

		finished = "dtEnd" in job

		failed = "failed" in job and job["failed"] is True

		build = jobName == "build"
		deploy = jobName == "deploy-on-commit"

		rome_timezone = pytz.timezone("Europe/Rome")
		currentDateTime = datetime.datetime.now(rome_timezone)

		diffTime = currentDateTime - dtStart

		if diffTime.total_seconds() < 900:
			alreadyPrinted = False
			if pipelineId in ultimoStato:
				if jobId in ultimoStato[pipelineId]:
					if ultimoStato[pipelineId][jobId] == "FINISHED":
						continue
					elif ultimoStato[pipelineId][jobId] == "RUNNING":
						alreadyPrinted = True
				else:
					ultimoStato[pipelineId][jobId] = None
			else:
				ultimoStato[pipelineId] = {}
				ultimoStato[pipelineId][jobId] = None

			ultimoStato[pipelineId][jobId] = "FINISHED" if finished else "RUNNING"

			if failed:
				print("ROSSO")
			elif not finished:
				if build:
					print("GIALLO")
				if deploy:
					print("BLU")
			else:
				if deploy:
					print("VERDE")


if __name__ == "__main__":
	while True:
		main()
		time.sleep(10)
