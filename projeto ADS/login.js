document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Login realizado com sucesso!");
            window.location.href = "templates/welcome.html";
        } else {
            alert(data.message);
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
        alert("Ocorreu um erro na requisição. Verifique o servidor.");
    });
});