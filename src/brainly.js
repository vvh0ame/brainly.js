class Brainly {
	constructor(language = "en") {
		this.language = language
		this.firstApi = "https://znanija.com/api/28"
		this.secondApi = "https://srv-user-moderation.z-dn.net"
		this.graphqlApi = `https://znanija.com/graphql/${this.language}`
		this.headers = {
			"content-type": "application/json",
			"user-agent": "Android-App 5.110.1"
		}
	}

	async login(username, password) {
		const response = await fetch(
			`${this.firstApi}/api_account/authorize`, {
				method: "POST",
				body: JSON.stringify({
					autologin: true,
					client_type: 1,
					password: password,
					username: username
				}),
				headers: this.headers
			})
		const headers = response.headers
		const data = await response.json()
		if (data.success) {
			this.accessToken = headers.get("x-b-token-long")
			this.headers["x-b-token-long"] = this.accessToken
			this.userId = await this.getAccountInfo().data.user.id
		}
		return data
	}

	async getAccountInfo() {
		const response = await fetch(
			`${this.firstApi}/api_users/me`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async register(
			username,
			email,
			password,
			country = "US",
			accountType = "PARENT",
			dateOfBirth = "2001-01-01") {
		const response = await fetch(
			`${this.graphqlApi}/?operationName=Registration`, {
				method: "POST",
				body: JSON.stringify({
					operationName: "Registration",
					variables: {
						input: {
							nick: username,
							email: email,
							password: password,
							dateOfBirth: dateOfBirth,
							country: country,
							acceptedTermsOfService: true,
							accountType: accountType
						}
					},
					query: "mutation Registration($input: RegisterInput!) { register(input: $input) { token pendingToken validationErrors { __typename ...ValidationErrorFragment } } }  fragment ValidationErrorFragment on ValidationError { path type error }"
				}),
				headers: this.headers
			})
		return response.json()
	}

	async getUserProfile(userId) {
		const response = await fetch(
			`${this.firstApi}/api_user_profiles/get_by_id/${userId}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getTaskInfo(taskId) {
		const response = await fetch(
			`${this.firstApi}/api_tasks/main_view/${taskId}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async answerToTask(taskId, content, attachments = []) {
		const response = await fetch(
			`${this.firstApi}/api_responses/add`, {
				method: "POST",
				body: JSON.stringify({
					attachments: attachments,
					content: `<p><strong>Ответ:</strong></p><p>${content}</p><p></p>`,
					task_id: taskId
				}),
				headers: this.headers
			})
		return response.json()
	}

	async getTicket(taskId) {
		const response = await fetch(
			`${this.firstApi}/api_tickets/get`, {
				method: "POST",
				body: JSON.stringify({
					device_tyoe: 301,
					task_id: taskId
				}),
				headers: this.headers
			})
		return response.json()
	}

	async removeTicket(ticketId) {
		const response = await fetch(
			`${this.firstApi}/api_tickets/remove`, {
				method: "POST",
				body: JSON.stringify({
					ticket_id: ticketId
				}),
				headers: this.headers
			})
		return response.json()
	}

	async getSimilarQuestions(taskId) {
		const response = await fetch(
			`${this.graphqlApi}/?operationName=SimilarQuestionQuery`, {
				method: "POST",
				body: JSON.stringify({
					operationName: "SimilarQuestionQuery",
					variables: {
						id: taskId
					},
					query: "query SimilarQuestionQuery($id: Int!) { questionById(id: $id) { similar { question { databaseId content author { nick avatar { thumbnailUrl } rank { name } } attachments { url } subject { name } } similarity } } }"
				}),
				headers: this.headers
			})
		return response.json()
	}

	async getDayLeaders() {
		const response = await fetch(
			`${this.firstApi}/api_global_rankings/view/0/1`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getWeekLeaders() {
		const response = await fetch(
			`${this.firstApi}/api_global_rankings/view/0/3`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getMonthLeaders() {
		const response = await fetch(
			`${this.firstApi}/api_global_rankings/view/0/5`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getUserFollowers(userId) {
		const response = await fetch(
			`${this.firstApi}/api_users/followers/${userId}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getUserFollowings(userId) {
		const response = await fetch(
			`${this.firstApi}/api_users/followed_by/${userId}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async followUser(userId) {
		const response = await fetch(
			`${this.firstApi}/api_users/follow/${userId}`, {
				method: "PUT",
				headers: this.headers
			})
		return response.json()
	}

	async unfollowUser(userId) {
		const response = await fetch(
			`${this.firstApi}/api_users/unfollow/${userId}`, {
				method: "DELETE",
				headers: this.headers
			})
		return response.json()
	}

	async thankAnswer(answerId) {
		const response = await fetch(
			`${this.firstApi}/api_responses/thank/${answerId}`, {
				method: "POST",
				headers: this.headers
			})
		return response.json()
	}

	async reportUser(userId, reasonId, description = null) {
		let body = {
			userId: userId,
			reasonId: reasonId
		}
		if (description) {
			body.description = description
		}
		const response = await fetch(
			`${this.secondApi}/v1/ru/user_reports`, {
				method: "POST",
				body: JSON.stringify(body),
				headers: this.headers
			})
		return response.json()
	}

	async getQuestions(
			limit = 10,
			status = "ANSWER_NEEDED",
			feedType = "PUBLIC",
			gradeIds = [],
			subjectIds = [],
			before = null) {
		let body = {
			operationName: "FeedQuestionsQuery",
			variables: {
				first: limit,
				gradeIds: gradeIds,
				subjectIds: subjectIds,
				status: status,
				feedType: feedType
			},
			query: "query FeedQuestionsQuery($first: Int, $before: ID, $gradeIds: [Int], $subjectIds: [Int], $status: FeedQuestionStatusFilter, $feedType: FeedType) { feed(first: $first, feedType: $feedType, before: $before, status: $status, gradeIds: $gradeIds, subjectIds: $subjectIds) { edges { node { __typename ...StreamQuestionFragment } cursor } pageInfo { endCursor hasNextPage hasPreviousPage } } }  fragment StreamQuestionFragment on Question { databaseId content isReported created author { nick avatar { thumbnailUrl } } created pointsForAnswer attachments { url } subject { name } }"
		}
		console.log(JSON.stringify(body))
		const response = await fetch(
			`${this.graphqlApi}/?operationName=FeedQuestionsQuery`, {
				method: "POST",
				body: JSON.stringify(body),
				headers: this.headers
			})
		return response.json()
	}

	async getConversations(page = 0) {
		const response = await fetch(
			`${this.firstApi}/api_messages/get_conversations/${page}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}
}

module.exports = {Brainly}
