var $t = $('.b-target').find('.b-list');
var active_class = 'b-list-item_active';

$('.b-init').find('.b-list-item').click(function() {
    var index = $(this).index();
    $t.children().removeClass(active_class);
    $t.children().eq(index).addClass(active_class);
})