from locust import HttpUser, task

class FirstLocust(HttpUser) :
    @task
    def hello(self):
        self.client.get('/')