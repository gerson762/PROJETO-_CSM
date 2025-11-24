function inicializarCookies() {
  const banner = document.getElementById("cookie-banner");
  const cookieAceito = localStorage.getItem("cookie-aceito");

  if (!cookieAceito && banner) {
    banner.style.display = "block";
    const botao = document.getElementById("aceitar-cookie");
    if (botao) {
      botao.addEventListener("click", function () {
        localStorage.setItem("cookie-aceito", "true");
        banner.style.display = "none";
      });
    }
  }
}

document.addEventListener("DOMContentLoaded", function () {
  inicializarCookies();
});
