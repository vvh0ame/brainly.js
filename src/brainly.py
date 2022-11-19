import requests

class Brainly:
	def __init__(self, language: str = "ru") -> None:
		self.first_api = "https://znanija.com"
		self.second_api = "https://srv-user-moderation.z-dn.net"
		self.graphql_api = f"https://znanija.com/graphql/{language}"
		self.headers = {
			"content-type": "application/json",
			"user-agent": "Android-App 5.110.1"
		}
		self.user_id = None
		self.access_token = None

	def login(
			self,
			username: str,
			password: str) -> dict:
		data = {
			"autologin": True,
			"client_type": 1,
			"password": password,
			"username": username
		}
		response = requests.post(
			f"{self.first_api}/api/28/api_account/authorize",
			json=data,
			headers=self.headers)
		json = response.json()
		headers = response.headers
		if json["success"] == True:
			self.access_token = headers["x-b-token-long"]
			self.headers["x-b-token-long"] = self.access_token
			self.user_id = self.get_account_info()["data"]["user"]["id"]
		return json
		
	def register(
			self,
			username: str,
			email: str,
			password: str,
			country: str = "RU",
			account_type: str = "PARENT",
			date_of_birth: str = "2003-03-03") -> dict:
		data = {
			"operationName": "Registration",
			"variables": {
				"input": {
					"nick": username,
					"email": email,
					"password": password,
					"dateOfBirth": date_of_birth,
					"country": country,
					"acceptedTermsOfService": True,
					"accountType": account_type
				}
			},
			"query": "mutation Registration($input: RegisterInput!) { register(input: $input) { token pendingToken validationErrors { __typename ...ValidationErrorFragment } } }  fragment ValidationErrorFragment on ValidationError { path type error }"
		}
		return requests.post(
			f"{self.graphql_api}/?operationName=Registration",
			json=data,
			headers=self.headers).json()

	def get_account_info(self) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_users/me",
			headers=self.headers).json()

	def get_user_profile(self, user_id: int) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_user_profiles/get_by_id/{user_id}",
			headers=self.headers).json()

	def get_task_info(self, task_id: int) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_tasks/main_view/{task_id}",
			headers=self.headers).json()

	def answer_to_task(
			self,
			task_id: int,
			content: str,
			attachments: list = []) -> dict:
		data = {
			"attachments": attachments,
			"content": f"<p><strong>Ответ:</strong></p><p>{content}</p><p></p>",
			"task_id": task_id
		}
		return requests.post(
			f"{self.first_api}/api/28/api_responses/add",
			json=data,
			headers=self.headers).json()

	def get_ticket(self, task_id: int) -> dict:
		data = {
			"device_type": 301,
			"task_id": task_id
		}
		return requests.post(
			f"{self.first_api}/api/28/api_tickets/get",
			json=data,
			headers=self.headers).json()

	def remove_ticket(self, ticket_id: int) -> dict:
		data = {
			"ticket_id": ticket_id
		}
		return requests.post(
			f"{self.first_api}/api/28/api_tickets/remove",
			json=data,
			headers=self.headers).json()

	def get_similar_questions(self, task_id: int) -> dict:
		data = {
			"operationName": "SimilarQuestionQuery",
			"variables": {
				"id": task_id
			},
			"query": "query SimilarQuestionQuery($id: Int!) { questionById(id: $id) { similar { question { databaseId content author { nick avatar { thumbnailUrl } rank { name } } attachments { url } subject { name } } similarity } } }"
		}
		return requests.post(
			f"{self.graphql_api}/?operationName=SimilarQuestionQuery",
			json=data,
			headers=self.headers).json()

	def get_day_leaders(self) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_global_rankings/view/0/1",
			headers=self.headers).json()

	def get_week_leaders(self) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_global_rankings/view/0/3",
			headers=self.headers).json()

	def get_month_leaders(self) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_global_rankings/view/0/5",
			headers=self.headers).json()

	def get_3_months_leaders(self) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_global_rankings/view/0/0",
			headers=self.headers).json()

	def get_user_followings(self, user_id: int) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_users/followed_by/{user_id}",
			headers=self.headers).json()

	def get_user_followers(self, user_id: int) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_users/followers/{user_id}",
			headers=self.headers).json()

	def follow_user(self, user_id: int) -> dict:
		return requests.put(
			f"{self.first_api}/api/28/api_users/follow/{user_id}",
			headers=self.headers).json()
	
	def unfollow_user(self, user_id: int) -> dict:
		return requests.delete(
			f"{self.first_api}/api/28/api_users/unfollow/{user_id}",
			headers=self.headers).json()

	def get_user_tasks(
			self,
			user_id: int,
			limit: int = 10) -> dict:
		data = {
			"limit": limit,
			"user_id": user_id
		}
		return requests.post(
			f"{self.first_api}/api/28/api_tasks/view_list",
			json=data,
			headers=self.headers).json()

	def thank_answer(self, answer_id: int) -> dict:
		return requests.post(
			f"{self.first_api}/api/28/api_responses/thank/{answer_id}",
			headers=self.headers).json()

	def vote_answer(
			self,
			answer_id: int,
			value: int) -> dict:
		data = {
			"data": {
				"value": value
			}
		}
		return requests.post(
			f"{self.first_api}/api/28/api_responses/vote/{answer_id}",
			json=data,
			headers=self.headers).json()

	def get_answer_thanks(
			self,
			answer_id: int,
			limit: int = 20) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_thanks/get_for_answer/{answer_id}?limit={limit}",
			headers=self.headers).json()

	def comment_answer(
			self,
			model_id: int,
			content: str,
			model_type_id: int = 2) -> dict:
		data = {
			"content": content,
			"model_id": model_id,
			"model_type_id": model_type_id
		}
		return requests.post(
			f"{self.first_api}/api/28/api_comments/add",
			json=data,
			headers=self.headers).json()

	def get_user_report_reasons(self) -> dict:
		return requests.get(
			f"{self.second_api}/v1/ru/user_report_reasons",
			headers=self.headers).json()

	def report_user(
			self,
			user_id: int,
			reason_id: int,
			description: str = None) -> dict:
		data = {
			"userId": user_id,
			"reasonId": reason_id
		}
		if description:
			data["description"] = description
		return requests.post(
			f"{self.second_api}/v1/ru/user_reports",
			json=data,
			headers=self.headers).json()

	def get_questions(
			self,
			limit: int = 10,
			status: str = "ANSWER_NEEDED",
			feed_type: str = "PUBLIC",
			grade_ids: list = [],
			subject_ids: list = [],
			before: str = None) -> dict:
		data = {
			"operationName": "FeedQuestionsQuery",
			"variables": {
				"first": limit,
				"gradeIds": grade_ids,
				"subjectIds": subject_ids,
				"status": status,
				"feedType": feed_type
			},
			"query": "query FeedQuestionsQuery($first: Int, $before: ID, $gradeIds: [Int], $subjectIds: [Int], $status: FeedQuestionStatusFilter, $feedType: FeedType) { feed(first: $first, feedType: $feedType, before: $before, status: $status, gradeIds: $gradeIds, subjectIds: $subjectIds) { edges { node { __typename ...StreamQuestionFragment } cursor } pageInfo { endCursor hasNextPage hasPreviousPage } } }  fragment StreamQuestionFragment on Question { databaseId content isReported created author { nick avatar { thumbnailUrl } } created pointsForAnswer attachments { url } subject { name } }"
		}
		if before:
			data["before"] = before
		return requests.post(
			f"{self.graphql_api}?operationName=FeedQuestionsQuery",
			json=data,
			headers=self.headers).json()

	def get_user_progress(self, user_id: int) -> dict:
		data = {
			"operationName": "UserProgressById",
			"variables": {
				"id": user_id
			},
			"query": "query UserProgressById($id: Int!) { userById(id: $id) { __typename ...UserProgressFragment } }  fragment UserProgressFragment on User { answerCountBySubject { count subject { name icon } } receivedThanks progress { dailyAnswersBySubjectInLast14Days { count startOfDay subject { name icon } } dailyThanksInLast14Days { count startOfDay } } }"
		}
		return requests.post(
			f"{self.graphql_api}/?operationName=UserProgressById",
			json=data,
			headers=self.headers).json()

	def get_conversations(self, page: int = 0) -> dict:
		return requests.get(
			f"{self.first_api}/api/28/api_messages/get_conversations/{page}",
			headers=self.headers).json()

	def search_question(
			self,
			query: str,
			limit: int = 10) -> dict:
		data = {
			"operationName": "SearchQuestionQuery",
			"variables": {
				"query": query,
				"first": limit
			},
			"query": "query SearchQuestionQuery($query: String!, $first: Int, $after: ID) { questionSearch(query: $query, first: $first, after: $after) { edges { node { __typename ...SearchQuestionsFragment } highlight { contentFragments } } pageInfo { endCursor hasNextPage hasPreviousPage } } }  fragment SearchQuestionsFragment on Question { id databaseId subject { databaseId name } grade { databaseId name } answers { hasVerified nodes { verification { __typename } content thanksCount rating ratesCount attachments { url } } } content attachments { url } }"
		}
		return requests.post(
			f"{self.graphql_api}/?operationName=SearchQuestionQuery",
			json=data,
			headers=self.headers).json()

	def create_task(
			self,
			content: str,
			points: int,
			subject_id: int,
			attachments: list = []) -> dict:
		data = {
			"attachments": attachments,
			"content": content,
			"points": points,
			"subject_id": subject_id
		}
		return requests.post(
			f"{self.first_api}/api/28/api_tasks/add",
			json=data,
			headers=self.headers).json()

	def edit_task(
			self,
			task_id: int,
			content: str = None,
			attachments: list = []) -> dict:
		data = {
			"data": {
				"attachments": attachments,
				"content": content
			}
		}
		return requests.post(
			f"{self.first_api}/api/28/api_tasks/edit/{task_id}",
			json=data,
			headers=self.headers).json()
