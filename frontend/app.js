import { editTasks, getTasks, searchTasks } from "./api.js";
import { createTask } from "./api.js";
import { updateTasks } from "./api.js";
import { deleteTasks } from "./api.js";

const accessToken = localStorage.getItem("accessToken")
if (!accessToken) {
  window.location.href = "login.html"
}
const input = document.querySelector("input");
const add_button = document.getElementById("add");
const list = document.querySelector("ul");
const deadline = document.querySelector("#deadline");
const search_input = document.getElementById("search")
const logout_button = document.getElementById("logout")
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

add_button.addEventListener("click", async () => {
  const title = input.value.trim();
  const deadlineElement = deadline.value;
  if (title === "") {
    return;
  }
  add_button.disabled = true;
  try {
    const task = await createTask(title, deadlineElement || null, accessToken);
    renderTask(task);
    input.value = "";
  } catch (error) {
    console.error(error);
  } finally {
    add_button.disabled = false;
    deadline.value = null;
  }
});


function getDeadlineStatus(deadline) {
  if (!deadline) {
    return "none";
  }
  const now = new Date();
  const deadlineDate = new Date(deadline);
  if (deadlineDate < now) {
    return "overdue";
  } else if (deadlineDate.getFullYear === now.getFullYear
    && deadlineDate.getMonth === now.getMonth
    && deadlineDate.getDate === now.getDate
  ) {
    return "today";
  }
  return "upcoming";
}


search_input.addEventListener("input", async()=>{
  const keyword = search_input.value.trim()
  list.innerHTML = ""
  if (keyword === "") {
    const tasks = await getTasks(accessToken)
    tasks.forEach(task => renderTask(task))
    return
  }

  const sortedTasks = await searchTasks(accessToken, keyword)
  if (sortedTasks.length > 0) {
    sortedTasks.forEach(task => renderTask(task))
  } else {
    list.innerHTML = `<li class="error-message">There is no task you find !!</li>`
  
  }
})


const tasks = await getTasks(accessToken)
tasks.forEach(task=>renderTask(task))
logout_button.addEventListener("click", ()=>{
  localStorage.removeItem("accessToken")
  window.location.href = "login.html"
})
