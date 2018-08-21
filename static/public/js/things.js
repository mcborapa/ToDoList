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

    $('body').on('click', '.del_th', function(){
        var elem = $(this);
        var agree = confirm('Desea eliminar el To Do List?');
        if (agree){
            typo = elem.parents('.princ').data('type');
            thing = elem.parents('.princ').data('pk');
            $.post('/delete_thing/',{thing:thing}, function(json){
                if(json.success){
                    elem.parents('.princ').remove();
                }else{
                    if(typo == 'index'){
                        elem.parents('.princ').find('.errorus').html('');
                        elem.parents('.princ').find('.errorus').html(json.msj);
                    }
                }
            }, 'json');
        }
    });

    $('body').on('click', '.chang_stat', function(){
        var elem = $(this);
        elem.parents('.princ').find('.errorus').html('');
        stat = elem[0].title;
        thing = elem.parents('.princ').data('pk');
        $.post('/chang_stat/',{thing:thing, stat:stat}, function(json){
            if(json.success){
                elem.attr('title',json.new_st);
                if(json.stat){
                    elem.parents('.princ').find('#card_pr').removeClass().addClass('card border-success mb-3');
                    elem.parents('.princ').find('#card_bd').removeClass('text-danger').addClass('text-success');
                    elem.parents('.princ').find('#fech_th').html('<strong>Terminada el: '+ json.fecha +'</strong>');
                }else{
                    elem.parents('.princ').find('#card_pr').removeClass().addClass('card border-danger mb-3');
                    elem.parents('.princ').find('#card_bd').removeClass('text-success').addClass('text-danger');
                    elem.parents('.princ').find('#fech_th').html('<strong>Creada el: '+ json.fecha +'</strong>');
                }
            }else{
                elem.parents('.princ').find('.errorus').html(json.msj);
            }
        }, 'json');
    });

    $('body').on('click', '.view_th', function(){
        var elem = $(this);
        fecha = elem.parents('.princ').find('#fech_th').html();
        cont = elem.parents('.princ').data('cont');
        thing = elem.parents('.princ').data('pk');
        stat = elem.parents('.princ').find('.chang_stat');
        stat = stat[0].title;
        if(stat == 'Pendiente'){
            stat = '<span class="badge badge-danger badge-pill">Pendiente</span>';
        }else if(stat == 'Terminada'){
            stat = '<span class="badge badge-success badge-pill">Completada</span>';
        }
        modal = $('#view_thsp');
        modal.find('#cond_th').html(fecha);
        modal.attr('data-pk',thing);
        modal.find('.modal-body').html(cont);
        modal.find('#ststth').html(stat);
        $('#ver_thg').click();
    });

    $('body').on('click', '.edit_thi', function(){
        var elem = $(this);
        elem.removeClass('btn-primary').addClass('btn-danger');
        elem.attr('disabled',true);
        elem.parents('#editthmo').find('.errorus').html('');
        thing = document.getElementById("editthmo").dataset.pk;
        cont = elem.parents('#editthmo').find('#cont_th')[0].value;
        cont = cont.replace(/&nbsp;/g,' ');
        cont = cont.replace(/<br>/g,' ');
        cont = cont.replace(/<[^>]*>?/g, '');
        cont = cont.trim();
        stat = elem.parents('#editthmo').find('#inp_edst')[0].checked;
        if (res==false){
            res = true;
            if(cont.length != 0){
                elem.parents('#editthmo').find('.errorus').attr('style','color: #787272;');
                elem.parents('#editthmo').find('.errorus').html('Guardando, por favor espere...');
                $.post('/edit_thign/',{thing:thing, cont:cont, statch:stat}, function(json){
                    if(json.success){
                        elem.parents('#editthmo').find('.errorus').attr('style','color: #1fea21;');
                        elem.parents('#editthmo').find('.errorus').html('Guardado con exito.');
                        things = document.getElementsByName('things');
                        for(var i=0;i<things.length;i++){
                            if ($(things[i]).data('pk') == json.th){
                                if(json.stat){
                                    $(things[i]).find('#card_pr').removeClass().addClass('card border-success mb-3');
                                    $(things[i]).find('#card_bd').removeClass('text-danger').addClass('text-success');
                                    $(things[i]).find('#fech_th').html('<strong>Terminada el: '+ json.fecha +'</strong>');
                                    $(things[i]).find('.chang_stat').attr('title','Terminada');
                                }else{
                                    $(things[i]).find('#card_pr').removeClass().addClass('card border-danger mb-3');
                                    $(things[i]).find('#card_bd').removeClass('text-success').addClass('text-danger');
                                    $(things[i]).find('#fech_th').html('<strong>Creada el: '+ json.fecha +'</strong>');
                                    $(things[i]).find('.chang_stat').attr('title','Pendiente');
                                }
                                var cort = json.cont.slice(0, 23);
                                cont_cort = cort + '...';
                                $(things[i]).find('.card-text').html(cont_cort);
                            }
                        }
                        setTimeout(function (){
                            elem.parents('#editthmo').find('.errorus').html('');
                            elem.attr('disabled',false);
                            res = false;
                            elem.removeClass('btn-danger').addClass('btn-primary');
                            $('#editthmo').find('.close').click();
                        },3000);
                    }else{
                        elem.parents('#editthmo').find('.errorus').removeAttr('style');
                        elem.parents('#editthmo').find('.errorus').html(json.msj);
                        setTimeout(function (){
                            elem.parents('#editthmo').find('.errorus').html('');
                            elem.attr('disabled',false);
                            res = false;
                            elem.removeClass('btn-danger').addClass('btn-primary');
                        },3000);
                    }
                }, 'json');
            }else{
                elem.parents('#editthmo').find('.errorus').html('No puede estar vacio. Debe ingresar un contenido.');
                setTimeout(function (){
                    elem.parents('#editthmo').find('.errorus').html('');
                    elem.attr('disabled',false);
                    res = false;
                    elem.removeClass('btn-danger').addClass('btn-primary');
                },3000); 
            }
        }
    });

    $('body').on('click', '.editar_th', function(){
        var elem = $(this);
        thing = elem.parents('#princ').data('pk');
        modal = $('#editthmo');
        modal.find('#cont_th')[0].value= '';
        modal.find('#cont_th').html('');
        modal.find('#inp_edst').removeAttr('checked');
        $.post('/edit_th/',{thing:thing}, function(json){
            if(json.success){
                document.getElementById("editthmo").dataset.pk=json.th;
                modal.find('#cont_th').html(json.cont);
                modal.find('#cont_th')[0].value = json.cont;
                if(json.stat){
                    stat = '<span class="badge badge-success badge-pill">Completada</span>';
                    modal.find('#inp_edst').attr('checked','');
                    modal.find('#cond_th').html('<strong>Terminada el: '+ json.fecha +'</strong>');
                }else{
                    stat = '<span class="badge badge-danger badge-pill">Pendiente</span>';
                    modal.find('#cond_th').html('<strong>Creada el: '+ json.fecha +'</strong>');
                }
                modal.find('#ststth').html(stat);
                $('#ed_thg').click();
            }else{
                elem.parents('#princ').find('.errorus').html(json.msj);
            }
        }, 'json');
    });

});