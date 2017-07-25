$( document ).ready(function() {

    $('#datetimepicker4').datetimepicker();
    $('#datetimepicker4').datetimepicker();

    var $form = $('#query-form');
    var $schedule =  $('.schedule input:radio[name=schedule]');
    var $repeats = $('.repeats');
    var $repeatsSelect = $('.repeats select');
    var $days = $('.days');
    var $allRepeat = $('.dependent-repeat')
    var $allOnce = $('.dependent-once')

    $schedule.change(
        function() {
            $allRepeat.addClass('hidden')
            $allOnce.addClass('hidden')
            var value = this.value;
            if (value === 'repeat'){
                $allRepeat.removeClass('hidden');
            }
            if (value === 'run-once'){
                $allOnce.removeClass('hidden');
            }
        }
    );

    $repeatsSelect.change(
        function() {
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