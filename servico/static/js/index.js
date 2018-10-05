let table = $('#datatables').DataTable({
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/api/servico/",
        "type": "GET"
    },
    "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese.json"
    },
    "columns": [
        {"data": "activo"},
        {"data": "codigo"},
        {"data": "zona"},
        {"data": "cliente"},
        {"data": "nome"},
        {"data": "valor_dia"},
        {"data": "portagens"},
        {"data": "banca"},
        {"data": "fatura"},
        {
            "data": null,
            "defaultContent": '<a class="btn-floating btn-small waves-effect waves-teal btn-flat modal-trigger" href="#edit-or-create-servico" id="edit-modal-btn"><i class="material-icons">edit</i></a>'

        }
    ]
});

let id = 0;

$('#datatables tbody').on('click', 'a', function () {
    let data = table.row($(this).parents('tr')).data();
    let servico_id = $(this).attr('id');
    if (servico_id == 'edit-modal-btn') {
        // EDIT button
        $('#activo').val(data['activo']);
        $('#zona').val(data['zona']);
        $('#codigo').val(data['codigo']);
        $('#cliente').val(data['cliente']);
        $('#nome').val(data['nome']);
        $('#valor_dia').val(data['valor_dia']);
        $('#portagens').val(data['portagens']);
        $('#banca').val(data['banca']);
        $('#fatura').val(data['fatura']);
        $('#type').val('edit');
        $('#modal_title').text('EDITAR SERVIÇO');
    }

    id = data['id'];

});

$('form').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let type = $('#type').val();
    let method = 'PUT';
    let url = '/api/servico/';

    // edit
    url = url + id + '/';

    $.ajax({
        url: url,
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        method: method,
        data: $this.serialize(),
        success: function (data) {
            M.toast({html: 'Dados alterados   <i class="material-icons">done</i>', classes: 'rounded toast-element'});
            setTimeout(function () {
                location.reload();
            }, 1500);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR)
        },
    })
});


