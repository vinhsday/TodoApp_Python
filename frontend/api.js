export async function getTasks(accessToken) {
    const response = await fetch("http://127.0.0.1:8000/tasks", {
    headers: {
        "Authorization": `Bearer ${accessToken}`
    }
})
    if (!response.ok) {
        throw new Error("Failed to get tasks")
    }
    return response.json()
}

export async function createTask(title, deadline, accessToken) {
    const response = await fetch("http://127.0.0.1:8000/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            title: title,
            deadline: deadline
        })
    })

    if (!response.ok) {
        throw new Error("Failed to create task")
    }

    return response.json()
}

export async function updateTasks(task, completed, accessToken) {
    const response = await fetch(`http://127.0.0.1:8000/tasks/${task.id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            completed: completed
        })
    })
    if (!response.ok) {
        throw new Error("Failed to create task")
    }
    return response.json()
}

export async function deleteTasks(task, li, accessToken) {
    const response = await fetch(`http://127.0.0.1:8000/tasks/${task.id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken}`
        }
    })
    if (!response.ok) {
        throw new Error("Failed to create task")
    }
    li.remove()
    return response.json()
}

export async function editTasks(task, accessToken, title, deadline) {
    const response = await fetch(`http://127.0.0.1:8000/tasks/${task.id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            title: title,
            deadline: deadline
        })
    })
    if (!response.ok) {
        throw new Error("Failed to create task")
    }
    return response.json()
}
