document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const loader = document.getElementById("loader");

    if (!loginForm || !loader) {
        console.error("Erro: Elementos do formulário ou loader não encontrados.");
        return;
    }

    document.getElementById("eye").addEventListener("click", function () {
        const senhaInput = document.getElementById("pwd");
        senhaInput.type = senhaInput.type === "password" ? "text" : "password";
    });

    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        const usuarioInput = document.querySelector("input[name='usuario']");
        const senhaInput = document.querySelector("input[name='senha']");
        const topiSelect = document.getElementById("topiSelect");

        if (!usuarioInput || !senhaInput || !topiSelect) {
            console.error("Erro: Campos de entrada não encontrados.");
            return;
        }

        const usuario = usuarioInput.value.trim();
        const senha = senhaInput.value.trim();
        const coligada = topiSelect.value;

        if (!coligada) {
            alert("Por favor, escolha uma opção (Topi ou CIS).");
            return;
        }

        // Exibir o loader
        loader.style.display = "flex";

        // Salvar coligada no localStorage
        localStorage.setItem("coligada", coligada);

        // Enviar a coligada para o backend
        fetch("/salvar-coligada", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ coligada: coligada })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Coligada salva:", data);
            return fetch(loginForm.action, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ usuario, senha })
            });
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url; // Redireciona ao sucesso
            } else {
                throw new Error("Usuário ou senha inválidos");
            }
        })
        .catch(error => {
            alert(error.message);
            console.error("Erro no login:", error);
        })
        .finally(() => {
            // Esconder o loader quando a requisição terminar
            loader.style.display = "none";
        });
    });
});
