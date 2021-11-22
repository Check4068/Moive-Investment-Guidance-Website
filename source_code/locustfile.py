from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def get_success(self):
        self.client.get(
            "/similar/MedBudget%26NormalMovie%26Fantasy%26Clint%20Eastwood%26Other%20Company")

    @task
    def get_recommend(self):
        self.client.get(
            "/recommend/MedBudget%26NormalMovie%26Fantasy%26Clint%20Eastwood%26Other%20Company")
