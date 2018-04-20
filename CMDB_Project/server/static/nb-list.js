// 自定义js匿名函数，属于自动调用，只有内部调用，防止当成插件时的同名冲突
(function (jq) {
    var GLOBAL_DICT={};
     /*
    {
        'device_type_choices': (
                                    (1, '服务器'),
                                    (2, '交换机'),
                                    (3, '防火墙'),
                                )
        'device_status_choices': (
                                    (1, '上架'),
                                    (2, '在线'),
                                    (3, '离线'),
                                    (4, '下架'),
                                )
    }
     */


    // 为字符串创建format方法，用于字符串格式化
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    // {#页面加载时自动发送ajax请求#}
    function initial(url) {
        $.ajax({
            url: url,
            type: 'GET',
            // {#将响应的字符串数据转换成字典格式#}
            dataType: 'JSON',
            success: function (arg) {
                // 将 (1, '服务器')……等数据作成全局常量
                $.each(arg.global_dict, function (k ,v) {
                    GLOBAL_DICT[k] = v
                });
                // {#生成表头字段#}
                initTableHeader(arg.table_config);
                // {#生成表格数据#}
                initTableBody(arg.server_list, arg.table_config);
            }
        })
    }

    // {#生成表头字段#}
    function initTableHeader(tableConfig) {
        // {#循环生成字段表头#}
        $.each(tableConfig, function (k, v) {
            if (v.display) { // 为Ture时需要展示
                var tag = document.createElement('th');
                tag.innerHTML = v.title
                $('#tbHead').find('tr').append(tag);
            }
        })
    }

    // {#生成表格数据信息#}
    function initTableBody(serverList, tableConfig) {

        $.each(serverList, function (k, row) {  // 循环查询出来数据表中所有的数据

            // row: {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-}
            /*
            <tr>
                <td>id</td>
                <td>hostn</td>
                <td>create</td>
            </tr>
            */
            var tr = document.createElement('tr')
            $.each(tableConfig, function (kk, rrow) {
                if (rrow.display) {      // 是否需要展示该字段对应的内容
                    // kk: 1  rrow:{'q':'id','title':'ID'},         // rrow.q = "id"
                    // kk: .  rrow:{'q':'hostname','title':'主机名'},// rrow.q = "hostname"
                    // kk: .  rrow:{'q':'create_at','title':'创建时间'}, // rrow.q = "create_at"
                    var td = document.createElement('td');
                    // rrow['q']
                    // rrow['text']
                    // rrow.text.tpl = "asdf{n1}sdf"
                    // rrow.text.kwargs = {'n1':'@id','n2':'@@123'}
                    var newKwargs = {}; // {'n1':'1','n2':'123'}
                    $.each(rrow.text.kwargs, function (kkk, vvv) {  // 循环字典
                        var av = vvv;
                        if(vvv.substring(0,2) == '@@'){  // 生成数字对应的字符串值
                            var global_dict_key = vvv.substring(2, vvv.length);  // 获得数据表中的字段名 例device_type_choices
                            var nid = row[rrow.q]   // 通过自定义的配置字典，获得数据表中该条数据的id值
                            $.each(GLOBAL_DICT[global_dict_key], function (gk, gv) {
                                if(gv[0] == nid){
                                    av = gv[1]; // av = '服务器'
                                }
                            })
                        }
                        // {#@表示需要进行字符串格式化#}
                        else if (vvv[0] == '@') {
                            // {#进行切分，获得@后面的具体字段名，用于从数据库中取出具体的值 #}
                            av = row[vvv.substring(1, vvv.length)];
                        }
                        newKwargs[kkk] = av;
                    });

                    // {#通过自定义的扩展方法进行字符串格式化#}
                    var newText = rrow.text.tpl.format(newKwargs);
                    td.innerHTML = newText;

                    // 在标签中添加属性
                    $.each(rrow.attrs, function (atkey, atval) {
                        // 如果@
                        if(atval[0] == '@'){
                            td.setAttribute(atkey, row[atval.substring(1, atval.length)]);
                        }else {
                            td.setAttribute(atkey, atval);
                        }
                    });

                    $(tr).append(td)
                }
            });
            $('#tbBody').append(tr);
        })
    }
    
    // 进入编辑模式
    function trIntoEdit($tr) {
        if ($('#inOutEditMode').hasClass('btn-warning')){   // 是否进入了编辑模式
        $tr.find('td[edit-enable="true"]').each(function () {   // 找到tr标签下所有td标签中属性为edit-enable=true的元素，并循环它
            // $(this)  每一个td标签
            var editType = $(this).attr('edit-type');  // 从配置列表中获得编辑类型的值
            if(editType == 'select'){
                // 生成下拉框，找到数据源
                var deviceTypeChoices = GLOBAL_DICT[$(this).attr('global_key')];
                // 生成select下拉框标签
                var selectTag = document.createElement('select');
                var origin = $(this).attr('origin');    // 获得当前标签中的origin属性的值
                $.each(deviceTypeChoices, function (k, v) {  //  v的值为 (1, '服务器'),
                    var option = document.createElement('option');
                    $(option).text(v[1]);  // 为option标签添加文本值
                    $(option).val(v[0]);  // 为option标签添加属性值
                    if(v[0] == origin){
                        // 默认选中原来的值
                        $(option).prop('selected', true);
                    }
                    $(selectTag).append(option);
                });
                $(this).html(selectTag)
            }else {
                 // 获取原来td中的文本内容
                var v1 = $(this).text();
                // 创建input标签，并且内部设置值
                var inp = document.createElement('input');
                $(inp).val(v1);
                // 添加到td标签中
                $(this).html(inp);
            }
        })
    }
    }

    // 退出编辑模式
    function trOutEdit($tr) {
        $tr.find('td[edit-enable="true"]').each(function () {
             // $(this) 每一个td
            var editType = $(this).attr('edit-type');   // 获得标签类型
            if(editType == 'select'){
                var option = $(this).find('select')[0].selectedOptions;  // 将jquery对象转换为DOM对象，调用selectOptions获得select标签中的options标签
                $(this).html($(option).text());
            }else {
                var inputVal = $(this).find('input').val();    // 获得tr标签中所有input标签的值
                $(this).html(inputVal);  // 为当前td标签添加html格式内容
            }
        })

    }



    jq.extend({ // 通过jQuery继承函数xx，可以直接通过$.xx(url)来直接进行调用
        xx: function (url) {
            // {#通过ajax异步请求获得初始化数据#}
            initial(url)

            // 通过js控制，控制标签类型，完成进入编辑模式功能
            // 在tbBody标签范围中为所有checkbox添加click事件
            $('#tbBody').on('click', ':checkbox', function () {
                // 检测多选框是否已经被选中
                var $tr = $(this).parent().parent()   // 通过checkbox标签获得tr标签中的元素
                if ($(this).prop('checked')){   // prop()获得标签属性值
                    // 进入编辑模式
                    trIntoEdit($tr);
                }else {
                    // 退出编辑模式
                    trOutEdit($tr);
                }
            });

            // 为所有按钮绑定事件
            // 为全选按钮绑定事件
            $('#checkAll').click(function () {
                if($('#inOutEditMode').hasClass('btn-warning')){    // 是否进入了编辑模式
                    $('#tbBody').find(':checkbox').each(function () {
                        if(!$(this).prop('checked')){   // 将没有被选中的一起选中
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);    // 进入编辑状态
                            $(this).prop('checked', true)   // 多选框被选中状态
                        }else {
                             $(this).prop('checked',true);
                        }
                    })
                }else {
                    $('#tbBody').find(':checkbox').prop('checked', true)    // 未进入编辑模式，所有不变
                }

            })

            // 为反选按钮绑定事件
            $('#checkReverse').click(function () {
                if($('#inOutEditMode').hasClass('btn-warning')){    // 进入编辑模式
                 $('#tbBody').find(':checkbox').each(function () {
                     var $tr = $(this).parent().parent();
                    if ($(this).prop('checked')){
                        trOutEdit($tr); // 退出编辑状态
                        $(this).prop('checked', false)
                    }else {
                        trIntoEdit($tr);
                        $(this).prop('checked', true);
                    }
                })
                }else {
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')){   // 如果是选中状态
                            $(this).prop('checked', false); // 修改为未选中状态
                        }else {
                            $(this).prop('checked',true);
                        }
                    })
                }
            })

            // 为取消按钮绑定事件
            $('#checkCancel').click(function () {
                if($('#inOutEditMode').hasClass('btn-warning')){
                    $('#tbBody').find(':checkbox').each(function () {
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                        }
                        $(this).prop('checked', false);
                    });
                }else {
                    $('#tbBody').find(':checkbox').prop('checked', false)
                }
            })

            // 为编辑按钮绑定事件
            $('#inOutEditMode').click(function () {
                if ($(this).hasClass('btn-warning')){
                    // 需要退出编辑模式时
                    $(this).removeClass('btn-warning');
                    $(this).text('进入编辑模式');
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')){   // 如果是可编辑状态
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);    // 退出编辑状态
                        }
                    })
                }else {
                    // 进入编辑模式
                    $(this).addClass('btn-warning');
                    $(this).text('退出编辑模式');
                    $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);
                        }
                    });
                }
            })


        }
    });
})(jQuery)  // 传入jQeury对象