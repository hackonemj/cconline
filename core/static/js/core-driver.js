$(document).ready(function () {
    $('.modal').modal();
    $('.tooltipped').tooltip();
    $('.fixed-action-btn').floatingActionButton();
    $('#id_obs').addClass('materialize-textarea');

    $(".disabled-btn-sd").click(function () {
        alert("Não pode adicionar novo serviço, termine o anterior.");
    });

    $("#id_codigo_do_servico").keyup(function () {
        var codigo_do_servico = $(this).val();

        $.ajax({
            url: 'ajax/validate-codigo-servico/',
            data: {
                'codigo_do_servico': codigo_do_servico
            },
            dataType: 'json',
            success: function (data) {
                if (data.encontrou) {
                    $('#id_descricao_servico').val(data.cliente + " / " + data.nome);
                    $('#id_descricao_servico').css("color", "#333");
                }
                else {
                    $('#id_descricao_servico').val('*serviço não encontrado');
                    $('#id_descricao_servico').css("color", "#F44336");
                }
            }
        });

    });

    $("#id_automovel_matricula").keyup(function () {
        var automovel_matricula = $(this).val();

        $.ajax({
            url: 'ajax/validate-automovel-matricula/',
            data: {
                'automovel_matricula': automovel_matricula
            },
            dataType: 'json',
            success: function (data) {
                if (data.encontrou) {
                    $('#id_automovel_modelo').val(data.automovel_modelo);
                    $('#id_automovel_modelo').css("color", "#333");
                    $('#id_km_inicial').val(data.automovel_km_actual);
                }
                else {
                    $('#id_automovel_modelo').val('*matricula não encontrada');
                    $('#id_automovel_modelo').css("color", "#F44336");
                }
            }
        });

    });


});

function finalizarServico(id, url) {
    // Submit post on submit
    $('.finalizar-servico-form').on('click', function (event) {
        var km_final = $('#id_km_final').val();
        //event.preventDefault();
        $.ajax({
            type: "Get",
            url: url,
            data: {
                'id': id,
                'km_final': km_final
            },
            dataType: 'json',
            success: function (data) {

            },
        });
        //$('#finalizar-servico-modal').modal('close');
    });
}


