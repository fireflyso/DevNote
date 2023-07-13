from locust import HttpUser, TaskSet, task


class Testlocust(TaskSet):
    @task(1)
    def test_queryMessage(self):
        post_url = ''
        r = self.client.get(post_url)
        assert 'I am' in str(r.content, encoding="utf-8")


class WebsiteUser(HttpUser):
    tasks = [Testlocust]
    min_wait = 500
    max_wait = 5000

