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
document.querySelectorAll(".btn-editar").forEach((button) => {
  button.addEventListener("click", function () {
    let codapontamento = this.getAttribute("data-codapontamento"); // Pega o código do atributo
    salvarCodApontamento(codapontamento);
  });
});

//Modal de confirmação de exclusão

document.addEventListener('DOMContentLoaded', function() {
  const deleteModal = document.getElementById('deleteModal');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

  if (deleteModal) {
    deleteModal.addEventListener('show.bs.modal', function(event) {
      const button = event.relatedTarget;

      const codColigada = button.getAttribute('data-codcoligada');
      const codApontamento = button.getAttribute('data-codapontamento');

      //Pega a linha da tabela que contém o botão
      const row = button.closest('tr');

      document.getElementById('deleteCodApontamento').textContent = row.cells[1].textContent; 

      document.getElementById('deleteProjeto').textContent = row.cells[3].textContent;

      document.getElementById('deleteData').textContent = row.cells[4].textContent;

      //Formatar horário

      const horaInicio = row.cells[5].textContent;
      const horaFim = row.cells[6].textContent;

      document.getElementById('deleteHorario').textContent = `${horaInicio} - ${horaFim}`;

      //Atualizar o link de confirmação com os parâmetros corretos
      // confirmDeleteBtn.href = `/apontamento_delete?codcoligada=${codColigada}&codapontamento=${codApontamento}`;
      
    });

    //Evento para quando o modal for fechado
    deleteModal.addEventListener('hidden.bs.modal', function() {
      //Resetar o botão de confirmação
      if (confirmDeleteBtn) {
        confirmDeleteBtn.innerHTML = '<i class="fas fa-trash-alt"></i> Excluir';
        confirmDeleteBtn.classList.remove('disabled');
      }
    });
  }

  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', function(e) {
      // Desabilitar o botão e mostrar animação de carregamento
      this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Excluindo...';
      this.classList.add('disabled');
      
      // Permitir que o navegador processe a animação antes de redirecionar
      setTimeout(() => {
        // O redirecionamento acontecerá automaticamente pelo href
      }, 10000);
    });
  }
})
