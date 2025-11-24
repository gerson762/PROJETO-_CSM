document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch('/login', {  // <-- CORRIGIDO: Caminho relativo
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('userRole', data.role);
            window.location.href = "templates/welcome.html";
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Erro:', error));
});