import logging
logging.basicConfig(level=logging.INFO)
from sonarcloudx1.abstract import AbstractSonar
from sonarcloudx1	import factories

# Represents a software Project Branches
class MeasureHistory(AbstractSonar):

	def __init__(self,personal_access_token, sonar_url):
		super(MeasureHistory,self).__init__(personal_access_token=personal_access_token,sonar_url=sonar_url)
	
	def get_measurehistory(self, project_key, project_branche):
		return self.sonar.project_branches.search_project_branches(project=project_key, branche=project_branche)

	def get_all(self, today=False): 
		try:
			logging.info("Start function: get_measurehistory")
			
			project_service = factories.Project(personal_access_token=self.personal_access_token,sonar_url=self.sonar_url)
			project_service.set_organization_name(organization_name = self.organization_name)
			projects = project_service.get_all()
			projectbranches = []
			measurehistory = []
			
			for project in projects:
				projectbranches.append(self.get_projectbranches(project['key']))

			for project in projects:
				for branches in projectbranches:
					measurehistory.append(self.get_measurehistory(project['key'],branches['branches']['name']))

			return measurehistory

		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Branches")
		
		
