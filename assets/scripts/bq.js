$( document ).ready(function() {

    var $form = $('#query-form');
    var $schedule =  $('.schedule input:radio[name=schedule]');
    var $repeats = $('.repeats');
    var $repeatsSelect = $('.repeats select');
    var $run =  $('.run-fields');
    var $days = $('.days');
    var $time = $('.time');
    var $all1 = $('.dependent-form1')
    var $all2 = $('.dependent-form2')

    $schedule.change(
        function() {
            $all1.addClass('hidden')
            var value = this.value;
            if (value === 'repeat'){
                $repeats.removeClass('hidden');
            }
            if (value === 'run-once'){
                $run.removeClass('hidden');
            }
        }
    );

    $repeatsSelect.change(
        function() {
            $all2.addClass('hidden')
            var value = this.value;
            if (value === 'daily'){
                $time.removeClass('hidden');
            }
            if (value === 'weekly'){
                $days.removeClass('hidden');
                $time.removeClass('hidden');
            }
            if (value === 'monthly'){
                $monthly.removeClass('hidden');
                $time.removeClass('hidden');
            }
        }
    );

});