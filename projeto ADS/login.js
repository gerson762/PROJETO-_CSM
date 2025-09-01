document.getElementById("login-form").addEventListener("submit", function(event) {
  event.preventDefault(); // Evita o envio padrão do formulário

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username === "" || password === "") {
    alert("Por favor, preencha todos os campos.");
  } else {

    alert("Login simulado. Para um login real, é necessário um backend para autenticação.");
  }
});