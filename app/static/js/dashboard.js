// Função para salvar o apontamento
function salvarCodApontamento(codapontamento) {
  fetch("/salvar-codapontamento", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ codapontamento: codapontamento }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("CodApontamento salvo:", data);
    })
    .catch((error) =>
      console.error("Erro ao salvar CodApontamento:", error)
    );
}

// Adicionar evento de clique aos botões de editar
document.querySelectorAll(".editar-link").forEach((button) => {
  button.addEventListener("click", function () {
    let codapontamento = this.getAttribute("data-codapontamento");
    salvarCodApontamento(codapontamento);
  });
});

// Confirmação de exclusãoACCAA
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.delete-link').forEach(link => {
    link.addEventListener('click', function(e) {
      // ⚠️ Impede a ação se estiver desabilitado visualmente
      if (this.classList.contains('disabled')) {
        e.preventDefault();
        return;
      }

      e.preventDefault();

      const codApontamento = this.getAttribute('data-codapontamento');
      const projeto = this.getAttribute('data-projeto');
      const data = this.getAttribute('data-data');
      const horaInicio = this.getAttribute('data-hora-inicio');
      const horaFim = this.getAttribute('data-hora-fim');

      const mensagem = `Tem certeza que deseja excluir este apontamento?\n\n` +
                      `Detalhes do apontamento:\n` +
                      `Código: ${codApontamento}\n` +
                      `Projeto: ${projeto}\n` +
                      `Data: ${data}\n` +
                      `Horário: ${horaInicio} - ${horaFim}\n\n` +
                      `Esta ação não pode ser desfeita.`;

      if (confirm(mensagem)) {
        window.location.href = this.href;
      }
    });
  });
});
