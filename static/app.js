const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");
const count = document.getElementById("count");
const message = document.getElementById("message");

async function request(url, options = {}) {
  const response = await fetch(url, options);

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Something went wrong");
  }

  if (response.status === 204) return null;
  return response.json();
}

async function loadTasks() {
  try {
    const tasks = await request("/api/tasks");
    renderTasks(tasks);
    message.textContent = "";
  } catch (error) {
    message.textContent = error.message;
  }
}

function renderTasks(tasks) {
  list.replaceChildren();
  empty.hidden = tasks.length > 0;

  const completed = tasks.filter(task => task.completed).length;
  count.textContent = `${completed}/${tasks.length} completed`;

  for (const task of tasks) {
    const item = document.createElement("li");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.setAttribute("aria-label", "Mark task completed");

    const title = document.createElement("span");
    title.className = "task-title";
    title.textContent = task.title;

    if (task.completed) title.classList.add("completed");

    checkbox.addEventListener("change", async () => {
      try {
        await request(`/api/tasks/${task.id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ completed: checkbox.checked })
        });
        await loadTasks();
      } catch (error) {
        message.textContent = error.message;
      }
    });

    const remove = document.createElement("button");
    remove.className = "delete";
    remove.textContent = "Delete";

    remove.addEventListener("click", async () => {
      try {
        await request(`/api/tasks/${task.id}`, { method: "DELETE" });
        await loadTasks();
      } catch (error) {
        message.textContent = error.message;
      }
    });

    item.append(checkbox, title, remove);
    list.appendChild(item);
  }
}

form.addEventListener("submit", async event => {
  event.preventDefault();

  const title = input.value.trim();
  if (!title) return;

  try {
    await request("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    input.value = "";
    message.textContent = "";
    await loadTasks();
    input.focus();
  } catch (error) {
    message.textContent = error.message;
  }
});

loadTasks();
