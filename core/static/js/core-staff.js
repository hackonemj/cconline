$(document).ready(function () {
    var is_auto, is_cod_servico, is_funcionario, is_km_final;

    $("#id_funcionario").keyup(function () {
        var id_funcionario = $(this).val();

        $.ajax({
            url: 'ajax/validate-funcionario/',
            data: {
                'id_funcionario': id_funcionario
            },
            dataType: 'json',
            success: function (data) {
                if (data.encontrou) {
                    $('#func_nome').val(data.nome);
                    $('#func_nome').css("color", "#333");
                    is_funcionario = true
                }
                else {
                    $('#func_nome').val('*funcionário não encontrado');
                    $('#func_nome').css("color", "#F44336");
                    is_funcionario = false
                }
            }
        });

    });

    $("#sd_codigo_servico").keyup(function () {
        var codigo_do_servico = $(this).val();

        $.ajax({
            url: 'ajax/validate-codigo-servico/',
            data: {
                'codigo_do_servico': codigo_do_servico
            },
            dataType: 'json',
            success: function (data) {
                if (data.encontrou) {
                    $('#sd_descricao_servico').val(data.cliente + " / " + data.nome);
                    $('#sd_descricao_servico').css("color", "#333");
                    is_cod_servico = true
                }
                else {
                    $('#sd_descricao_servico').val('*serviço não encontrado');
                    $('#sd_descricao_servico').css("color", "#F44336");
                    is_cod_servico = false
                }
            }
        });

    });

    $("#auto_matricula").keyup(function () {
        var automovel_matricula = $(this).val();

        $.ajax({
            url: 'ajax/validate-automovel-matricula/',
            data: {
                'automovel_matricula': automovel_matricula
            },
            dataType: 'json',
            success: function (data) {
                if (data.encontrou) {
                    $('#auto_modelo').val(data.automovel_modelo);
                    $('#auto_modelo').css("color", "#333");
                    if (data.automovel_km_actual > 0) {
                        $('#sd_km_inicial').val(data.automovel_km_actual);
                        $('#sd_km_inicial').attr('disabled')
                        $('#sd_km_inicial').addClass('valid');
                    }
                    $('#sd_km_inicial').addClass('valid');
                    $('#sd_km_inicial').removeClass('invalid');
                    is_auto = true
                }
                else {
                    $('#sd_km_inicial').val(0);
                    $('#auto_modelo').val('*matricula não encontrada');
                    $('#auto_modelo').css("color", "#F44336");
                    $('#sd_km_inicial').addClass('invalid');
                    $('#sd_km_inicial').removeClass('valid');
                    is_auto = false
                }
            }
        });

    });
    $("#sd_km_final").keyup(function () {
        var km_inicial = $("#sd_km_inicial").val();
        var km_final = $("#sd_km_final").val();
        if (km_final <= km_inicial) {
            $("#sd_km_final").removeClass('valid');
            $("#sd_km_final").addClass('invalid');
            is_km_final = false
        }
        else if (km_final > km_inicial) {
            $("#sd_km_final").removeClass('invalid');
            $("#sd_km_final").addClass('valid');
            is_km_final = true
        }
    });

    $('#SD-form').submit(function (event) {
        var id_funcionario = $("#id_funcionario").val();
        var codigo_servico = $("#sd_codigo_servico").val();
        var auto_matricula = $("#auto_matricula").val();
        var km_inicial = $("#sd_km_inicial").val();
        var km_final = $("#sd_km_final").val();
        var obs = $("#sd_obs").val();

        event.preventDefault();
        if (is_auto && is_cod_servico && is_funcionario && is_km_final) {
            $.ajax({
                type: "POST",
                url: 'ajax/criar-sd/',
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                data: {
                    'id_funcionario': id_funcionario,
                    'codigo_servico': codigo_servico,
                    'auto_matricula': auto_matricula,
                    'km_inicial': km_inicial,
                    'km_final': km_final,
                    'obs': obs,
                },
                success: function (data) {
                    var elem = document.querySelector('#criar-sd');
                    var instance = M.Modal.getInstance(elem);
                    instance.destroy();
                    document.getElementById("SD-form").reset();
                    M.toast({
                        html: 'Serviço Diário criado com sucesso   <i class="material-icons">done</i>',
                        classes: 'rounded toast-element'
                    });
                    setTimeout(function () {
                        location.reload();
                    }, 1000);
                },
                error: function (data) {
                }
            });
        }
        else {
            if (is_funcionario == false) {
                $("#id_funcionario").addClass('invalid');
                if (is_auto == false) {
                    $("#auto_matricula").addClass('invalid');
                    if (is_cod_servico == false) {
                        $("#sd_codigo_servico").addClass('invalid');
                    }
                }
            }
            else if (is_auto == false) {
                $("#auto_matricula").addClass('invalid');
            }
            else if (is_cod_servico == false) {
                $("#sd_codigo_servico").addClass('invalid');
            }
            else if (is_km_final == false) {
                $("#sd_km_final").removeClass('valid');
                $("#sd_km_final").addClass('invalid');
            }
        }

    });

});
