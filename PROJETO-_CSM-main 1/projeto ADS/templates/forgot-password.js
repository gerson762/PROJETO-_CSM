document.getElementById("forgot-password-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;

    fetch('http://127.0.0.1:5000/forgot_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Redireciona para a página de redefinição
            window.location.href = `reset-password.html?email=${email}`;
        } else {
            alert(data.message);
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
        alert("Ocorreu um erro na requisição.");
    });
});