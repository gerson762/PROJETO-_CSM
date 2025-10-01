document.getElementById("register-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const fullName = document.getElementById("full_name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("As senhas não coincidem. Por favor, tente novamente.");
        return;
    }

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            full_name: fullName,
            email: email,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cadastro realizado com sucesso! Você já pode fazer login.");
            window.location.href = "login.html";
        } else {
            alert(data.message);
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
        alert("Ocorreu um erro no cadastro. Por favor, tente novamente.");
    });
});