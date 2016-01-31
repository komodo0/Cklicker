//возвращает true, если элемент принадлежит данному классу
function hasClass(elem, className) {
	return new RegExp("(^|\\s)"+className+"(\\s|$)").test(elem.className)
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


//Возвращает id элемента, очищенный от префикса
function getPrefixElementId(element, id_prefix){
var var_id = element;
var_id = var_id.slice(var_id.indexOf(id_prefix)+id_prefix.length);
return var_id;
}

//Заполняет значения step для построения комментария при переключении варианта
function fillState(){

}

//Перезаполняет текст комментария в зависимости от значения инпутов
function rebuildComment(){
    var current_comment = "";
    var chosen_id = step.chosen_id;

    var variant = $(".b-list-item" + "#variant_"+chosen_id);

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
        radio_title = $(".radio"+"#"+radioInp).find("span.radio_title")
        radio_value = $(".radio"+"#"+radioInp).find("span.radio_value").text()
        alert(radio_value)
    }



    //alert(input_text.text().replace(/\s+/g,' ') + input_check.text().replace(/\s+/g,' ') + input_radio.text().replace(/\s+/g,' '));

    $('#comment').val(step.prev_comment + current_comment);
}

/*
_________Схема данных:____________

current_step    - переменная, обозначающая, на каком шагу ведется диагностика.


Каждый шаг представленн элементом step_i , где i - номер шага.
Первый шаг - step
Шаг представляет собой следующий объект:

step:
    state_id;
    chosen_id;
    prev_comment;
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
    - prev_comment - значение аналогчнйо переменной передыдущего step-а + парсинг inputs

Затем меняются атрибуты блоков visible, not_visible и другие, в соответствии с новым шагом
    - также нужно добавить обработчик последнего шага для вывода результата и навигации.

*/



count_current_step = 0;
var step = new Object();
step.state_id = getCookie('fist_step_id');
step.prev_comment = "";
step.chosen_id = -1;
step.inputs = new Object();
step.inputs.text = new Object();
step.inputs.check = new Object();
step.inputs.radio = new Object();


/* Event Listener для выбора варианта */
$('.b-init').find('.b-list-item').click(function() {
    var variants_target = $('.b-target').find('.b-list');
    var variants_active_class = 'b-list-item_active';

    var index = $(this).index();
    variants_target.children().removeClass(variants_active_class);
    variants_target.children().eq(index).addClass(variants_active_class);

    var id_prefix = "variant_";
    element = variants_target.children().eq(index).attr('id');

    if (step.chosen_id != getPrefixElementId(element, id_prefix)){
        step.chosen_id = getPrefixElementId(element, id_prefix);
        $('#comment').val(step.prev_comment);
        //Заполняет значения step для построения комментария
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

/* Event Listener для всплывающих подсказок */
$('div.question').click(function(){
    var id = getPrefixElementId(this.id, "question_");

    if($.inArray("visible", $('div.move_description#'+id).attr('class').split(' ')) == -1){
        $('div.move_description#'+id).removeClass("not_visible");
        $('div.move_description#'+id).addClass("visible");
        $('div.main-container').addClass("main_container_big");
    } else {
        $('div.move_description#'+id).removeClass("visible");
        $('div.move_description#'+id).addClass("not_visible");
        $('div.main-container').removeClass("main_container_big");
    }
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
    var rad_input_id = target.name;

    if (step.inputs.radio[rad_input_id] != rad_input_var_id){
        step.inputs.radio[rad_input_id] = rad_input_var_id;
        rebuildComment();
    }
})