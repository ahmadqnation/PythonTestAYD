from locust import HttpUser, task, between, LoadTestShape


class TodoUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post("/auth/login", json={
            "email": "locust@test.dk",
            "password": "Locust1234!",
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


class SpikeLoadShape(LoadTestShape):
    # (stage_end_seconds, user_count, spawn_rate)
    stages = [
        ( 30,  10,   5),  # Opvarmning: 10 brugere i 30 sek
        ( 40, 200, 200),  # Spike: 200 brugere på 10 sek (spawn_rate=200 for hurtig stigning)
        ( 70, 200,   1),  # Hold spike i 30 sek
        ( 80,  10, 200),  # Fald tilbage til 10 brugere på 10 sek
        (110,  10,   1),  # Stabilisering: 10 brugere i 30 sek
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage_end, users, spawn_rate in self.stages:
            if run_time < stage_end:
                return (users, spawn_rate)
        return None
