//возвращает true, если элемент принадлежит данному классу
function hasClass(elem, className) {
	return new RegExp("(^|\\s)"+
	className +
	"(\\s|$)").test(elem.className)
}

// возвращает cookie с именем name, если есть, если нет, то undefined
function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

//устанавливает куки
function setCookie(name, value, options) {
  options = options || {};

  var expires = options.expires;

  if (typeof expires == "number" && expires) {
    var d = new Date();
    d.setTime(d.getTime() + expires * 1000);
    expires = options.expires = d;
  }
  if (expires && expires.toUTCString) {
    options.expires = expires.toUTCString();
  }

  value = encodeURIComponent(value);

  var updatedCookie = name + "=" + value;

  for (var propName in options) {
    updatedCookie += "; " + propName;
    var propValue = options[propName];
    if (propValue !== true) {
      updatedCookie += "=" + propValue;
    }
  }

  document.cookie = updatedCookie;
}

//Удаляет кукки
function deleteCookie(name) {
  setCookie(name, "", {
    expires: -1
  })
}

//Возвращает массив со всеми ключами cookie
function getCookieList(){
    var mas = document.cookie.split(';')
    var names = [];
    var i = 0;
    var l = mas.length;
    for(;i<l;i++){
        names.push(mas[i].split('=')[0]);
    }
    return names;
}

//Удаляет записи куки о всех шагах, после указанного
function deleteLaterStepsCookies(current_step){
    var cookie_list = getCookieList();
    for (cookie_name in cookie_list){
        if (getPrefixElementId(cookie_list[cookie_name], "step_") > current_step){
            deleteCookie(cookie_list[cookie_name]);
        }
    }
}

//Возвращает id элемента, очищенный от префикса
function getPrefixElementId(element, id_prefix){
    var var_id = element;
    //alert("element = " + var_id);
    var_id = var_id.slice(var_id.indexOf(id_prefix)+id_prefix.length);
    //alert("cleaned elem = " + var_id)
    return var_id;
}

//Перезаполняет текст комментария в зависимости от значения инпутов
function rebuildComment(){
    var current_comment = "";
    var chosen_id = step.chosen_id;

    var variant = $(".b-list-item" + "#variant_"+chosen_id);


    if (variant.hasClass("important_title")){
        current_comment = variant.find(".var-name").text().replace(/\s+/g,' ') + ". ";
    }

    hidden_comment = variant.find(".hidden_comment").text().replace(/\s+/g,' ');

    if (hidden_comment!=""){
        current_comment += hidden_comment + ". ";
    }

    //Вылеояем рамкой выбранный вариант
    var variants_target = $('.b-target').find('.b-list');
    var variants_active_class = 'b-list-item_active';
    var index = variant.index();
    variants_target.children().removeClass(variants_active_class);
    variants_target.children().eq(index).addClass(variants_active_class);

    //Заполняем input_text элементы + генерируем комментарий
    input_text = variant.find("div.text");
    for (textInp in step.inputs.text){
        var input = variant.find(".text"+"#"+textInp);
        current_comment += step.inputs.text[textInp] + ". ";
    }

    for (checkInp in step.inputs.check){
        current_comment += step.inputs.check[checkInp] + ". ";
    }

    input_radio = variant.find("div.radio");
    for (radioInp in step.inputs.radio){
        chosen_variant_id = step.inputs.radio[radioInp];
        radio_input = variant.find("div.radio#"+radioInp)
        radio_title = radio_input.find("span.radio_title").text().replace(/\s+/g,' ');
        radio_value = radio_input.find("input#"+chosen_variant_id).siblings().text().replace(/\s+/g,' ');
        current_comment += radio_title.trim() + ": " + radio_value.trim() +". ";
    }

    step.comment = current_comment;
    $('#comment').val(concatComments());
}

//Проходится по всем step'ам и собирает комментарий.
function concatComments(){
    var result = "";
    for (i = 0; i < count_current_step; i+=1){
        result += JSON.parse(getCookie("step_"+i)).comment;
    }
    result += step.comment;
    return result;
}

//Проходится по всем step'ам и собирает комментарий с BR между вариантами.
function concatBrComments(){
    var result = "";
    for (i = 0; i < count_current_step; i+=1){
        result += JSON.parse(getCookie("step_"+i)).comment;
    }
    result += step.comment + "<br/>";
    return result;
}

//Заполняет выбранные значения состояния по умолчанию для вновь выбранного варианта.
function fillState(){


    step.inputs.text = new Object();
    step.inputs.check = new Object();
    step.inputs.radio = new Object();

    variant = $("li#variant_"+step.chosen_id);

    variant.find("div.text").each(function(){
        var id = $(this).attr("id");
        var pre_text = $(this).find(".pre_text").text().replace(/\s+/g,' ');
        var value = $(this).find("input").val();
        var post_text = $(this).find(".post_text").text().replace(/\s+/g,' ');

        if (value != ""){
            step.inputs.text[id] = pre_text + " " + value + " " + post_text;
        }

    });


    variant.find("div.checkbox").each(function(){
        var id = $(this).attr("id");
        var value = $(this).find("input").val();
        var isChecked = $(this).find("input").prop("checked");

        if (isChecked){
            step.inputs.check[id] = value;
        }
    })


    variant.find("div.radio").each(function(){
        var block_id = $(this).attr("id");
        var radio_id = $(this).find("input").attr("name");
        var title = $(this).find("span.radio_title").text().replace(/\s+/g,' ');
        var variant = $(this).find("input[name="+radio_id+"]:checked").attr("id");
        step.inputs.radio[block_id] = variant;
    })


}

/*Выделяет, раскрывает и отмечает элеент дерева с id = tree_id*/
function setActiveNode(tree_id){

    $("div#file_manager").find("div.b-list-item.tree_cursor").removeClass("tree_cursor");
    tree_elem = $(".b-list-item#tree_"+tree_id);
    tree_elem.addClass("used_tree_elem");
    tree_elem.addClass("tree_cursor");
    tree_elem = tree_elem.parent();
    tree_elem.removeClass("ExpandClosed");
    tree_elem.addClass("ExpandOpen");
    input = $(".b-list-item#tree_"+tree_id).siblings("input");
    input.prop('checked', true);

}

/* Снимает выделение, закрывает и убирает отметку с элемента дерева с id = tree_id */
function setPassiveNode(tree_id){
    tree_elem = $(".b-list-item#tree_"+tree_id);
    tree_elem.removeClass("used_tree_elem");
    tree_elem = tree_elem.parent();
    tree_elem.removeClass("ExpandOpen");
    tree_elem.addClass("ExpandClosed");
    input = $(".b-list-item#tree_"+tree_id).siblings("input");
    input.prop('checked', false);
}

/*Отрисовывает значения инпутов по заданному объекту*/
function recoverInputs(recover_state){
    var variant = $(".section-variants").find(".b-list-item#variant_"+recover_state.chosen_id);

    for (input_text in recover_state.inputs.text){
        var pre_text = variant.find(".pre_text").text();
        var post_text = variant.find(".post_text").text();
        var input_value = recover_state.inputs.text[input_text].replace(pre_text, "").replace(post_text, "").trim();
        variant.find(".text#"+input_text).find("input").val(input_value);
    }

    for (input_check in recover_state.inputs.check){

        variant.find(".checkbox#"+input_check).find("input").prop('checked', true);
    }

    for (input_radio in recover_state.inputs.radio){
        variant.find("[name=radio_"+input_radio+"]#"+recover_state.inputs.radio[input_radio]).prop('checked', true);
    }
}

/*Восстанавливает состояние и отметки из куки, в случае, если файл был закрыт*/
function recoverStateFromCookie(){

    count_current_step = -1;
    var cookie_list = getCookieList();
    for (cookie_name in cookie_list){
        var key = cookie_list[cookie_name].trim();
        if (key.indexOf("step_") == 0){
            var step_id = getPrefixElementId(key, "step_");
            var temp_step = JSON.parse(getCookie("step_"+step_id));

            if (count_current_step < step_id){
                count_current_step = step_id;
            }

            //step_id - номер найденного шага, надо:
            //открыть шаг в дереве, поставить галочку, подсветить шаг
            setActiveNode(temp_step.state_id);
            //заполнить все инпуты соответственно кукам из этого шага
            recoverInputs(temp_step);
        }
    }

    return parseInt(count_current_step)+1;
}

function showOrHideControlButtons(current_state_id){
    if ($(".move_description#state_id_"+current_state_id+" .mode_description_content").text().replace(/\s+/g,' ')==" "){
            $("#question_state_id_"+current_state_id).hide();
        }

        if ($("#tip_parent_"+current_state_id).is(".tip")){
            $(".show_tips img").show();
        } else {
            $(".show_tips img").hide();
        }
}

/*
_________Схема данных:____________

step    - переменная, обозначающая, на каком шагу ведется диагностика.

Каждый шаг представленн элементом step_i , где i - номер шага.
Первый шаг - step
Шаг представляет собой следующий объект:

step:
    state_id;
    chosen_id;
    comment;
    inputs:
        text:
            text_input_id = value or undefined
        check:
            check_input_id = value or undefined
        radio:
            rad_input_id = rad_inp_var_id;


При нажатии на ок, текущий step дозаполняется значениями:
    - chosen_id - id выбранного варианта;
    - inputs - объект inputs;

Затем создается новый step, в котором заполняются:
    - state_id - текущий state
    - comment - значение аналогчнйо переменной step-а + парсинг inputs

Затем меняются атрибуты блоков visible, not_visible и другие, в соответствии с новым шагом
    - также нужно добавить обработчик последнего шага для вывода результата и навигации.

*/
//$(".b-list-item.not_visible").removeClass("not_visible");
    $("input[type='text']").val("");
    $("input[type='checkbox").prop("checked", false);
    if (getCookie("step_0")==undefined){

        $(".go_prev_state img").hide();

        count_current_step = 0;
        var step = new Object();
        step.state_id = getCookie('fist_step_id');
        step.comment = "";
        step.chosen_id = -1;
        step.inputs = new Object();
        step.inputs.text = new Object();
        step.inputs.check = new Object();
        step.inputs.radio = new Object();
        setActiveNode(step.state_id);
        rebuildComment();

        showOrHideControlButtons(step.state_id);

        first_variants = $(".section-variants .b-list-item.parent_state_id_"+step.state_id);
        if (first_variants.size() > 8){
            var n = Math.floor(first_variants.size()/4) + 1;
            var h = 400/n - n*8;
            first_variants.height(h);
        } else {
            first_variants.height(180);
        }

    } else {

        count_current_step = recoverStateFromCookie();
        step = new Object();
        step.state_id = JSON.parse(getCookie("step_"+(count_current_step-1))).chosen_id
        step.comment = "";
        step.chosen_id = -1;
        step.inputs = new Object();
        step.inputs.text = new Object();
        step.inputs.check = new Object();
        step.inputs.radio = new Object();
        setActiveNode(step.state_id);

        rebuildComment();

        $(".section-variants .b-list-item").removeClass("visible");
        $(".section-variants .b-list-item").addClass("not_visible");

        first_variants = $(".section-variants .b-list-item.parent_state_id_"+step.state_id);
        first_variants.addClass("visible").removeClass("not_visible");



        if (first_variants.size() > 8){
            var n = Math.floor((first_variants.size()-1)/4) + 1;
            var h = 400/n - n*8;
            first_variants.height(h);
        } else {
            first_variants.height(180);
        }

        $(".tip.visible").addClass("not_visible").removeClass("visible");
        $(".tip#tip_parent_"+step.state_id).addClass("visible").removeClass("not_visible");


        var temp = $(".move_title_elem.visible");
        temp.removeClass("visible");
        temp.addClass("not_visible");
        temp = $(".move_title_elem#title_"+step.state_id);
        temp.removeClass("not_visible");
        temp.addClass("visible");
        temp = $(".move_description.visible");
        temp.removeClass("visible");
        temp.addClass("not_visible");

        if ($(".section-variants").find("li.b-list-item.visible").size() == 0){
            var title = $(".section-variants-title").find(".move_title_elem.visible").text().replace(/\s+/g,' ');
            $("#diag_result").removeClass("not_visible").addClass("visible");
            $("#diag_result").find(".var-description").html("<h4>"+ title + "</h4>" + concatBrComments());
            $(".confirm-button").addClass("not_visible");
            $("#again").removeClass("not_visible");
        }

        showOrHideControlButtons(step.state_id);
    };

/* Event Listener для выбора варианта */
$('.section-variants .b-list-item').click(function() {
    $(".confirm-button").removeClass('disabled');
    var variants_target = $('.b-target').find('.b-list');
    var variants_active_class = 'b-list-item_active';

    var index = $(this).index();
    variants_target.children().removeClass(variants_active_class);
    variants_target.children().eq(index).addClass(variants_active_class);

    var id_prefix = "variant_";
    element = variants_target.children().eq(index).attr('id');

    if (step.chosen_id != getPrefixElementId(element, id_prefix)){
        step.chosen_id = getPrefixElementId(element, id_prefix);
        fillState();
        rebuildComment();
    }
})

/* Event Listener для File Manager*/
$('div#file_manager').click(function(event){
	event = event || window.event
	var clickedElem = event.target || event.srcElement

	if (!hasClass(clickedElem, 'Expand')) {
		return // клик не там
	}

	// Node, на который кликнули
	var node = clickedElem.parentNode
	if (hasClass(node, 'ExpandLeaf')) {
		return // клик на листе
	}

	// определить новый класс для узла
	var newClass = hasClass(node, 'ExpandOpen') ? 'ExpandClosed' : 'ExpandOpen'
	// заменить текущий класс на newClass
	// регексп находит отдельно стоящий open|close и меняет на newClass
	var re =  /(^|\s)(ExpandOpen|ExpandClosed)(\s|$)/
	node.className = node.className.replace(re, '$1'+newClass+'$3')
})

/*Event Listener для input text */
$('div.text').find('input').change(function(event){
    var parent = event.target.parentNode;
    var value = $(parent).find(".pre_text").text() + " " + event.target.value + " " + $(parent).find(".post_text").text();
    var text_input_id = event.target.parentNode.id;
    if (event.target.value == ""){
        if (text_input_id in step.inputs.text){
            delete step.inputs.text[text_input_id];
            rebuildComment();
        }
    } else {
        if (text_input_id in step.inputs.text){
            if (step.inputs.text[text_input_id] != value){
                step.inputs.text[text_input_id] = value;
                rebuildComment();
            }
        } else {
            step.inputs.text[text_input_id] = value;
            rebuildComment();
        }
    }
})

/*Event Listener для input checkbox */
$('div.checkbox').find('input').change(function(event){

    var value = event.target.value;
    var isChecked = event.target.checked;
    var check_input_id = event.target.parentNode.parentNode.id;

    if (!isChecked){
        if (check_input_id in step.inputs.check){
            delete step.inputs.check[check_input_id];
            rebuildComment();
        }
    } else {
        step.inputs.check[check_input_id] = value;
        rebuildComment();
    }
})

/*Event Listener для input radiobutton */
$('div.radio').find('input').change(function(event){
    var target = event.target;
    var rad_input_var_id = target.id;
    var rad_input_id = target.parentNode.parentNode.id;
    if (step.inputs.radio[rad_input_id] != rad_input_var_id){
        step.inputs.radio[rad_input_id] = rad_input_var_id;
        rebuildComment();
    }

})

/*Event Listener для главной кнопки*/
$(".confirm-button").click(function(){

    if (step.chosen_id == -1){

    } else {
        $(".go_prev_state img").show();

        $(".confirm-button").addClass('disabled');
        var prev_comments = "";
         for (i = 0; i < count_current_step; i+=1){
            prev_comments += JSON.parse(getCookie("step_"+i)).comment;
         }

         //Вычленяем текущий коммента из текст пространства, вырезая все предыдущие комментарии. Проще, чем парсить снова все чекбоксы
        step.comment = $("textarea.form-control").val().replace(prev_comments, "");

        step_state = JSON.stringify(step);
        setCookie("step_"+count_current_step, step_state);
        count_current_step +=1;

        step_state += 1;
        step.state_id = step.chosen_id;
        step.chosen_id = -1;
        step.comment = "";
        step.inputs.text = new Object();
        step.inputs.check = new Object();
        step.inputs.radio = new Object();

        $(".b-list-item_active").removeClass("b-list-item_active");

        $(".section-variants .b-list-item").removeClass("visible");
        $(".section-variants .b-list-item").addClass("not_visible");
        current_variants = $(".section-variants .b-list-item.parent_state_id_"+step.state_id);
        current_variants.removeClass("not_visible").addClass("visible");

        if (current_variants.size() > 8){
            var n = Math.floor((current_variants.size()-1)/4)+1;
            var h = 400/n - n*8;
            current_variants.height(h);
        } else {
            current_variants.height(180);
        }

        $(".tip.visible").addClass("not_visible").removeClass("visible");
        $(".tip#tip_parent_"+step.state_id).addClass("visible").removeClass("not_visible");


        var temp = $(".move_title_elem.visible");
        temp.removeClass("visible");
        temp.addClass("not_visible");
        temp = $(".move_title_elem#title_"+step.state_id);
        temp.removeClass("not_visible");
        temp.addClass("visible");

        showOrHideControlButtons(step.state_id);

        temp = $(".move_description.visible");
        temp.removeClass("visible");
        temp.addClass("not_visible");

        setActiveNode(step.state_id);

        if ($(".section-variants").find("li.b-list-item.visible").size() == 0){

            var title = $(".section-variants-title").find(".move_title_elem.visible").text().replace(/\s+/g,' ');
            $("#diag_result").removeClass("not_visible").addClass("visible");
            $("#diag_result").find(".var-description").html("<h4>"+ title + "</h4>" + concatBrComments());
            $(".confirm-button").addClass("not_visible");
            $("#again").removeClass("not_visible");
        }

    }
})




/*Event Listener для кнопки "Предыдущий шаг"*/
$(".go_prev_state img").click(function(){
        deleteCookie("step_" + (count_current_step-1));
        window.location.reload();
});

/*Event Listener для кнопки "Следующий шаг"*/
$(".go_next_state img").click(function(){
    alert("go next page")
})

/*Event Listener для кнопки тест again*/
$("#again").click(function(){
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
    	var cookie = cookies[i];
    	var eqPos = cookie.indexOf("=");
    	var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    	document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
    window.location.reload();
})

$(".start_again").click(function(){
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
    	var cookie = cookies[i];
    	var eqPos = cookie.indexOf("=");
    	var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    	document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
    window.location.reload();
})

/* Event Listener для всплывающих подсказок */
$('.question').click(function(){

    $(".form-control").addClass("disabled");
    var id = getPrefixElementId( $(this).attr("id"), "question_");
    elem = $(".move_description#"+id);
     if (elem.is(":visible")){
        elem.removeClass("visible");
        elem.addClass("not_visible");
        $('div.main-container').removeClass("main_container_big");
     } else {
        elem.removeClass("not_visible");
        elem.addClass("visible");
        $('div.main-container').addClass("main_container_big");
     }
})



$(".close_move_descriprion").click(function(){
    var elem = $(".move_description.visible");
    elem.removeClass("visible");
    elem.addClass("not_visible");
    $(".form-control").removeClass("disabled");
})
/*
$(".move_description").click(function(){
    var elem = $(".move_description.visible");
    elem.removeClass("visible");
    elem.addClass("not_visible");
    $(".form-control").removeClass("disabled");
})
*/

//-------------------------------------------//


$(".show_tips img").click(function(){

    $(".section-tips").addClass("visible");
    $(".section-tips").removeClass("not_visible");
    $(".form-control").addClass("disabled");
})


$(".close_tips").click(function(){
    var elem = $(".section-tips.visible");
    elem.removeClass("visible");
    elem.addClass("not_visible");
    $(".form-control").removeClass("disabled");
})


/*
$(".section-tips").click(function(){
    var elem = $(".section-tips.visible");
    elem.removeClass("visible");
    elem.addClass("not_visible");
    $(".form-control").removeClass("disabled");
})
*/