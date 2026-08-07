import { register } from "./api.js";
const errorMessage = document.getElementById("error");

document.getElementById('loginForm').addEventListener('submit',async function(e) {
    // Ngăn chặn form gửi đi theo mặc định (làm tải lại trang)
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('confirm').value

    try {
        const data = await register(username,password, confirm)
    } catch (error) {
        errorMessage.textContent = error.message
    }
});
