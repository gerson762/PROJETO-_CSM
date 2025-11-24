document.getElementById("register-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const fullName = document.getElementById("full_name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("Senhas não conferem");
        return;
    }

    fetch('/register', { // <-- CORRIGIDO
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, email: email, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cadastro OK!");
            window.location.href = "login.html";
        } else {
            alert(data.message);
        }
    });
});