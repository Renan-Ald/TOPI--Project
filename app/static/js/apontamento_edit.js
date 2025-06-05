$(document).ready(function () {
        $(".select2").select2({
            width: '100%',
            placeholder: "Selecione uma opção",
            allowClear: true
        });

        const codProjetoInicial = $("#cod_projeto").val();
        const codApontamentoInicial = $("#CODTB1FAT").val();

        if (codApontamentoInicial) {
            console.log("Apontamento inicial carregado:", codApontamentoInicial);
            $("#selectApontamento").val(codApontamentoInicial).trigger('change');
        }

        // Carrega apontamentos ao abrir a página
        if (codProjetoInicial) {
            carregarApontamentos(codProjetoInicial, codApontamentoInicial);
        }

        $("#selectProjeto").change(function () {
            const codProjeto = $(this).val();
            console.log("Projeto selecionado:", codProjeto);

            $("#cod_projeto").val(codProjeto);
            $("#cod_apontamento").val(""); // Limpa valor ao trocar projeto

            if (codProjeto) {
                carregarApontamentos(codProjeto, null);
            } else {
                $("#selectApontamento").empty().append('<option value="">Escolha um apontamento...</option>');
                $("#selectApontamento").val('').trigger('change');
            }
        });

        $("#selectTarefa").change(function () {
            const codTarefa = $(this).val();
            console.log("Tarefa selecionada:", codTarefa);
            $("#cod_tarefa").val(codTarefa);
        });

        $("#selectApontamento").on('change', function () {
            const codApontamento = $(this).val();
            console.log("Apontamento selecionado pelo usuário:", codApontamento);
            $("#cod_apontamento").val(codApontamento);
});


        function carregarApontamentos(codProjeto, apontamentoSelecionado) {
            console.log("Carregando apontamentos para o projeto:", codProjeto);

            $.ajax({
                url: "/get_apontamentos",
                type: "GET",
                data: { cod_projeto: codProjeto },
                success: function (data) {
                    const apontamentoSelect = $("#selectApontamento");
                    apontamentoSelect.empty().append('<option value="">Escolha um apontamento...</option>');
                    console.log(data)
                    data.forEach(function (item) {
                        apontamentoSelect.append(
                            `<option value="${item.CODIGO}">${item.DESCRICAO}</option>`
                        );
                    });

                    if (apontamentoSelecionado) {
                        console.log("Setando apontamento selecionado após AJAX:", apontamentoSelecionado);
                        apontamentoSelect.val(apontamentoSelecionado).trigger('change');
                        $("#CODTB1FAT").val(apontamentoSelecionado);
                    } else {
                        apontamentoSelect.val('').trigger('change');
                    }
                },
                error: function () {
                    alert("Erro ao carregar os apontamentos.");
                }
            });
        }

        $("#formApontamento").submit(function (event) {
            event.preventDefault();

            var formData = $(this).serialize();
            console.log("Dados enviados no formulário:", formData);

            $.ajax({
                url: "/editar_apontamento",
                type: "PUT",
                data: formData,
                success: function (response) {
                    console.log("Resposta do servidor:", response);
                    alert(response.message);
                    window.location.href = "/dashboard";
                },
                error: function (error) {
                    console.error("Erro na submissão:", error);
                    alert(error.responseJSON?.error || "Erro ao salvar.");
                }
            });
        });
    });