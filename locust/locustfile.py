from locust import HttpUser, task, between


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
