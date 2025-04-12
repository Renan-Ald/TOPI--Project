
$(document).ready(function () {
    $(".select2").select2({
        width: '100%',
        placeholder: "Selecione uma opção",
        allowClear: true
    });

    $("#selectProjeto").change(function () {
        var codProjeto = $(this).val();
        $("#cod_projeto").val(codProjeto);

        if (codProjeto) {
            console.log(codProjeto)
            $.ajax({
                url: "/get_apontamentos",
                type: "GET",
                data: { cod_projeto: codProjeto },
                success: function (data) {
                    $("#selectApontamento").empty().append('<option value="">Escolha um apontamento...</option>');
                    data.forEach(function (apontamento) {
                        $("#selectApontamento").append(`<option value="${apontamento.CODIGO}">${apontamento.DESCRICAO}</option>`);
                    });
                }
            });
        } else {
            $("#selectApontamento").empty().append('<option value="">Escolha um apontamento...</option>');
        }
    });
    $("#selectTarefa").change(function () {
        var codTarefa = $(this).val();
        $("#cod_tarefa").val(codTarefa);
    });

    // Quando o apontamento for selecionado
    $("#selectApontamento").change(function () {
        var codApontamento = $(this).val();
        $("#cod_apontamento").val(codApontamento);
    });

    $("#turno").change(function () {
        $("#cod_turno").val($(this).val());
    });
    $("#veiculo").change(function () {
        $("#cod_veiculo").val($(this).val());
    });

    $("#formApontamento").submit(function (event) {
event.preventDefault(); // Evita o recarregamento da página

// Serializa os dados do formulário principal
var formData = $(this).serializeArray();

// Capturar campos da aba "Informações Extras"
$("#extras input, #extras textarea, #extras select").each(function () {
var name = $(this).attr("name"); // Obtém o atributo "name"
var value = $(this).val(); // Obtém o valor selecionado/digitado

if (name) {
    // Se o valor estiver vazio, substitui por null
    value = value || null;
    formData.push({ name: name, value: value }); // Adiciona ao formData
}
});
formData.push({ name: "veiculo", value: $("#veiculo").val() || null });
formData.push({ name: "turno", value: $("#turno").val() || null });
formData.push({ name: "tipo_desp", value: $("#tipo_desp").val() || null });
console.log("Enviando apontamento:");
console.log(formData);

// Enviar os dados via AJAX para o backend
$.ajax({
type: "POST",
url: "/criar_apontamento",
data: $.param(formData), 
success: function (response) {
    alert("Apontamento criado com sucesso!");
},
error: function (error) {
    alert("Erro ao criar apontamento!");
}
});
});


});