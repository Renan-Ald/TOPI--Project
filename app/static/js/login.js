// Show/hide password onClick of button using Javascript only

// https://stackoverflow.com/questions/31224651/show-hide-password-onclick-of-button-using-javascript-only

function show() {
    var p = document.getElementById('pwd');
    p.setAttribute('type', 'text');
}

function hide() {
    var p = document.getElementById('pwd');
    p.setAttribute('type', 'password');
}

var pwShown = 0;

document.getElementById("eye").addEventListener("click", function () {
    if (pwShown == 0) {
        pwShown = 1;
        show();
    } else {
        pwShown = 0;
        hide();
    }
}, false);

document.getElementById('loginForm').addEventListener('submit', function(event) {
    const topiSelect = document.getElementById('topiSelect');
    const coligada = document.getElementById("topiSelect").value;
    
    // Verifica se o campo "topi" está selecionado
    if (!topiSelect.value) {
        event.preventDefault(); // Impede o envio do formulário
        alert('Por favor, escolha uma opção (Topi ou CIS).');
    }
    localStorage.setItem("coligada", coligada);
    fetch('/salvar-coligada', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ coligada: coligada })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Coligada salva com sucesso:", data);
    })
    .catch(error => {
        console.error("Erro ao salvar a coligada:", error);
    });
    
});
