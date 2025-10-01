document.getElementById("reset-password-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get('email');
    const token = document.getElementById("token").value;
    const newPassword = document.getElementById("new_password").value;

    fetch('http://127.0.0.1:5000/reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, token: token, new_password: newPassword }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            window.location.href = "login.html";
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
        alert("Ocorreu um erro na requisição.");
    });
});