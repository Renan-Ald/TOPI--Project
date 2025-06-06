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

// Função de pesquisa na tabela
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const table = document.querySelector('.table');
    const tbody = table.querySelector('tbody');

    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const rows = tbody.getElementsByTagName('tr');

        for (let row of rows) {
            const cells = row.getElementsByTagName('td');
            let found = false;

            for (let cell of cells) {
                if (cell.textContent.toLowerCase().indexOf(searchText) > -1) {
                    found = true;
                    break;
                }
            }

            row.style.display = found ? '' : 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('mainTable');
    const contextMenu = document.getElementById('contextMenu');
    const searchContainer = document.getElementById('searchContainer');
    const searchColumnName = document.getElementById('searchColumnName');
    const columnSearchInput = document.getElementById('columnSearchInput');
    const clearSearch = document.getElementById('clearSearch');
    
    let currentColumnIndex = -1;

    // Função para mostrar o menu de contexto
    function showContextMenu(e, columnIndex) {
        e.preventDefault();
        currentColumnIndex = columnIndex;
        
        contextMenu.style.display = 'block';
        contextMenu.style.left = e.pageX + 'px';
        contextMenu.style.top = e.pageY + 'px';
    }

    // Função para esconder o menu de contexto
    function hideContextMenu() {
        contextMenu.style.display = 'none';
    }

    // Função para realizar a pesquisa na coluna específica
    function searchInColumn(searchText) {
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        
        for (let row of rows) {
            const cells = row.getElementsByTagName('td');
            const cell = cells[currentColumnIndex];
            
            if (cell) {
                const cellText = cell.textContent.toLowerCase();
                row.style.display = cellText.includes(searchText.toLowerCase()) ? '' : 'none';
            }
        }
    }

    // Event Listeners
    table.addEventListener('contextmenu', function(e) {
        const target = e.target;
        if (target.tagName === 'TH') {
            const columnIndex = Array.from(target.parentNode.children).indexOf(target);
            showContextMenu(e, columnIndex);
        }
    });

    document.addEventListener('click', function(e) {
        if (!contextMenu.contains(e.target)) {
            hideContextMenu();
        }
    });

    contextMenu.addEventListener('click', function(e) {
        if (e.target.dataset.action === 'search') {
            hideContextMenu();
            const columnName = table.getElementsByTagName('th')[currentColumnIndex].textContent;
            searchColumnName.textContent = `Pesquisar em ${columnName}:`;
            searchContainer.style.display = 'block';
            columnSearchInput.focus();
        }
    });

    columnSearchInput.addEventListener('input', function() {
        searchInColumn(this.value);
    });

    clearSearch.addEventListener('click', function() {
        columnSearchInput.value = '';
        searchContainer.style.display = 'none';
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        for (let row of rows) {
            row.style.display = '';
        }
    });
});
