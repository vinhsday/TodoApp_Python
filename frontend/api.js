import { API_BASE_URL } from "./config.js";

export async function getTasks(accessToken) {
  const response = await fetch(`${API_BASE_URL}/tasks`, {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  });
  if (!response.ok) {
    throw new Error("Failed to get tasks");
  }
  return response.json();
}

export async function createTask(title, deadline, accessToken) {
  const response = await fetch(`${API_BASE_URL}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      title: title,
      deadline: deadline
    })
  });

  if (!response.ok) {
    throw new Error("Failed to create task");
  }

  return response.json();
}

export async function updateTasks(task, completed, accessToken) {
  const response = await fetch(`${API_BASE_URL}/tasks/${task.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      completed: completed
    })
  });
  if (!response.ok) {
    throw new Error("Failed to create task");
  }
  return response.json();
}

export async function deleteTasks(task, li, accessToken) {
  const response = await fetch(`${API_BASE_URL}/tasks/${task.id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`
    }
  });
  if (!response.ok) {
    throw new Error("Failed to create task");
  }
  li.remove();
  return response.json();
}

export async function editTasks(task, accessToken, title, deadline) {
  const response = await fetch(`${API_BASE_URL}/tasks/${task.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      title: title,
      deadline: deadline
    })
  });
  if (!response.ok) {
    throw new Error("Failed to create task");
  }
  return response.json();
}

export async function searchTasks(accessToken, name) {
  const response = await fetch(`${API_BASE_URL}/tasks?search=${name}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  });
  if (!response.ok) {
    throw new Error("Failed to get tasks");
  }
  return response.json();
}

export async function login(username, password) {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: formData
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  localStorage.setItem("accessToken", data.access_token);

  window.location.href = "index.html";
}


export async function register(username, password, confirm_password) {
  if (password != confirm_password) {
    throw new Error("There's something wrong. Maybe your confirm one ?")
  }
  const response = await fetch(`${API_BASE_URL}/users/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body:JSON.stringify({
      "username": username,
      "password": password
    })
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Register failed");
  }

  window.location.href = "login.html";
}