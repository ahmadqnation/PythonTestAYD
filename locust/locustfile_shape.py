from locust import HttpUser, task, between, LoadTestShape


class TodoUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post("/auth/login", json={
            "email": "testuser@test.dk",
            "password": "Test1234!",
        })
        token = response.json().get("access_token")
        self.headers = {"Authorization": f"Bearer {token}"}

    @task(3)
    def get_todos(self):
        self.client.get("/todos", headers=self.headers)

    @task(2)
    def create_and_delete_todo(self):
        response = self.client.post("/todos", json={
            "title": "Test todo opgave",
            "completed": False,
        }, headers=self.headers)

        if response.status_code == 201:
            todo_id = response.json().get("id")
            self.client.delete(f"/todos/{todo_id}", headers=self.headers, name="/todos/[id]")


class StepLoadShape(LoadTestShape):
    # (stage_end_seconds, user_count, spawn_rate)
    stages = [
        (120,  10,  5),
        (240,  25, 10),
        (360,  50, 15),
        (480, 100, 20),
        (600, 150, 25),
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage_end, users, spawn_rate in self.stages:
            if run_time < stage_end:
                return (users, spawn_rate)
        return None
