import { editTasks, getTasks } from "./api.js";
import { createTask } from "./api.js";
import { updateTasks } from "./api.js";
import { deleteTasks } from "./api.js";
let accessToken;
const input = document.querySelector("input");
const button = document.querySelector("button");
const list = document.querySelector("ul");
const deadline = document.querySelector("#deadline");
function renderTask(task) {
  const li = document.createElement("li");
  const title = document.createElement("span");
  const checkbox = document.createElement("input");
  const deadline = document.createElement("span");
  const status = document.createElement("span");
  const editButton = document.createElement("button");
  editButton.textContent = "Edit";
  editButton.addEventListener("click", () => {
    editTaskUI(task, li);
  });
  status.textContent = getDeadlineStatus(task.deadline);
  if (task.deadline) {
    deadline.textContent = `Deadline: ${new Date(task.deadline).toLocaleString()}`;
  } else {
    deadline.textContent = "No deadline";
  }
  status.classList.add("deadline-status");
  status.classList.add(status.textContent.toLowerCase());
  checkbox.type = "checkbox";
  checkbox.checked = task.completed;
  checkbox.addEventListener("change", () =>
    updateTasks(task, checkbox.checked, accessToken)
  );
  title.textContent = task.title;
  const deleteButton = document.createElement("button");
  deleteButton.textContent = "Delete";
  deleteButton.addEventListener("click", async () => {
    try {
      await deleteTasks(task, li, accessToken);
    } catch (error) {
      console.error(error);
    }
  });

  li.appendChild(checkbox);
  li.appendChild(title);
  li.appendChild(deadline);
  li.appendChild(status);
  li.appendChild(editButton);
  li.appendChild(deleteButton);
  list.appendChild(li);
}

function updateTaskUI(task, li) {
  li.innerHTML = "";
  const title = document.createElement("span");
  const checkbox = document.createElement("input");
  const deadline = document.createElement("span");
  const status = document.createElement("span");
  const editButton = document.createElement("button");
  editButton.textContent = "Edit";
  editButton.addEventListener("click", () => {
    editTaskUI(task, li);
  });
  status.textContent = getDeadlineStatus(task.deadline);
  if (task.deadline) {
    deadline.textContent = `Deadline: ${new Date(task.deadline).toLocaleString()}`;
  } else {
    deadline.textContent = "No deadline";
  }
  status.classList.add("deadline-status");
  status.classList.add(status.textContent.toLowerCase());
  checkbox.type = "checkbox";
  checkbox.checked = task.completed;
  checkbox.addEventListener("change", () =>
    updateTasks(task, checkbox.checked, accessToken)
  );
  title.textContent = task.title;
  const deleteButton = document.createElement("button");
  deleteButton.textContent = "Delete";
  deleteButton.addEventListener("click", async () => {
    try {
      await deleteTasks(task, li, accessToken);
    } catch (error) {
      console.error(error);
    }
  });

  li.appendChild(checkbox);
  li.appendChild(title);
  li.appendChild(deadline);
  li.appendChild(status);
  li.appendChild(editButton);
  li.appendChild(deleteButton);
}

function editTaskUI(task, li) {
  const titleInput = document.createElement("input");
  titleInput.type = "text";
  titleInput.value = task.title;

  const deadlineInput = document.createElement("input");
  deadlineInput.type = "datetime-local";

  if (task.deadline) {
    deadlineInput.value = task.deadline.slice(0, 16);
  }

  const saveButton = document.createElement("button");
  saveButton.textContent = "Save";
  saveButton.addEventListener("click", async () => {
    try {
      const edited_task = await editTasks(
        task,
        accessToken,
        titleInput.value,
        deadlineInput.value || null
      );

      updateTaskUI(edited_task, li);
    } catch (error) {
      console.error(error);
    }
  });

  const cancelButton = document.createElement("button");
  cancelButton.textContent = "Cancel";
  cancelButton.addEventListener("click", () => {
    try {
      updateTaskUI(task, li);
    } catch (error) {
      console.error(error);
    }
  });

  li.innerHTML = "";

  li.appendChild(titleInput);
  li.appendChild(deadlineInput);
  li.appendChild(saveButton);
  li.appendChild(cancelButton);
}

button.addEventListener("click", async () => {
  const title = input.value.trim();
  const deadlineElement = deadline.value;
  if (title === "") {
    return;
  }

  button.disabled = true;
  try {
    const task = await createTask(title, deadlineElement || null, accessToken);
    renderTask(task);
    input.value = "";
  } catch (error) {
    console.error(error);
  } finally {
    button.disabled = false;
    deadline.value = null;
  }
});

const formData = new URLSearchParams();

formData.append("username", "1");
formData.append("password", "1");

fetch("http://127.0.0.1:8000/users/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: formData
})
  .then((response) => response.json())
  .then((data) => {
    accessToken = data.access_token;
  })
  .then((data) => getTasks(accessToken))
  .then((tasks) => tasks.forEach((task) => renderTask(task)))
  .catch((error) => {
    console.error(error);
  });

function getDeadlineStatus(deadline) {
  if (!deadline) {
    return "none";
  }
  const now = new Date();
  const deadlineDate = new Date(deadline);
  if (deadlineDate < now) {
    return "overdue";
  } else if (deadlineDate.getDate === now.getDate()) {
    return "today";
  }
  return "upcoming";
}
