$(document).ready(function(){
    var res = false;
    $('body').on('click', '.sav_th', function(){
        var elem = $(this);
        elem.attr('disabled',true);
        $('#error_th').html('');
        cont = elem.parents('#bodyin').find('#cont_th')[0].value;
        cont = cont.replace(/&nbsp;/g,' ');
        cont = cont.replace(/<br>/g,' ');
        cont = cont.replace(/<[^>]*>?/g, '');
        cont = cont.trim();
        if (res==false){
            res = true;
            elem.removeClass('btn-success').addClass('btn-danger');
			if (cont.length != 0){
                $('#error_th').attr('style','color: #787272;');
                $('#error_th').html('Guardando, por favor espere.');
                $.post('/save_thing/',{cont:cont}, function(json){
                    if(json.success != false){
                        setTimeout(function (){
                            $('#error_th').attr('style','color: #1fea21;');
                            $('#error_th').html('Guardado con exito.');
                            elem.parents('#bodyin').find('#cont_th')[0].value = '';
                            setTimeout(function (){
                                $('#error_th').attr('style','');
                                $('#error_th').html('');
                                $('#misthi').prepend(json);
                                elem.attr('disabled',false);
                                res = false;
                                elem.removeClass('btn-danger').addClass('btn-success');
                            },1000);
                        },1000);
                    }else{
                        $('#error_th').attr('style','');
                        $('#error_th').html(json.msj);
                        setTimeout(function (){
                            $('#error_th').html('');
                            elem.attr('disabled',false);
                            res = false;
                            elem.removeClass('btn-danger').addClass('btn-success');
                        },3000);
                    }
                });
            }else{
                $('#error_th').html('No puede estar vacio. Debe ingresar un contenido.');
                setTimeout(function (){
                    $('#error_th').html('');
                    elem.attr('disabled',false);
                    res = false;
                    elem.removeClass('btn-danger').addClass('btn-success');
                },3000);
            }
		}
        
    });
});