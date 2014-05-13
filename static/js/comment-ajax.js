/*$(function(){
        $("table").stupidtable();
    });*/
    $(function(){
      // Helper function to convert a string of the form "Mar 15, 1987" into
      // a Date object.
      var date_from_string = function(str){
        var months = ["Jan.","feb","mar","apr","May","jun","jul",
                      "aug","sep","oct","nov","dec"];
        var pattern = "^([a-zA-Z]{3})\\s*(\\d{2}),\\s*(\\d{4})$";
        var re = new RegExp(pattern);
        var DateParts = re.exec(str).slice(1);

        var Year = DateParts[2];
        var Month = $.inArray(DateParts[0].toLowerCase(), months);
        var Day = DateParts[1];
        return new Date(Year, Month, Day);
      }

      var moveBlanks = function(a, b) {
        if ( a < b ){
          if (a == "")
            return 1;
          else
            return -1;
        }
        if ( a > b ){
          if (b == "")
            return -1;
          else
            return 1;
        }
        return 0;
      };
      var moveBlanksDesc = function(a, b) {
        // Blanks are by definition the smallest value, so we don't have to
        // worry about them here
        if ( a < b )
          return 1;
        if ( a > b )
          return -1;
        return 0;
      };

      var table = $("table").stupidtable({
        "date":function(a,b){
          // Get these into date objects for comparison.

          aDate = date_from_string(a);
          bDate = date_from_string(b);

          return aDate - bDate;
        },
        "moveBlanks": moveBlanks,
        "moveBlanksDesc": moveBlanksDesc,
      });

      table.on("beforetablesort", function (event, data) {
        // data.column - the index of the column sorted after a click
        // data.direction - the sorting direction (either asc or desc)
        $("#msg").text("Sorting index " + data.column)
      });

      table.on("aftertablesort", function (event, data) {
        var th = $(this).find("th");
        th.find(".arrow").remove();
        var dir = $.fn.stupidtable.dir;

        var arrow = data.direction === dir.ASC ? "headerSortUp" : "headerSortDown";
        th.eq(data.column).append('<span class="arrow ' + arrow +'"></span>');
      });

      $("tr").slice(1).click(function(){
        $(".awesome").removeClass("awesome");
        $(this).addClass("awesome");
      });

    });

function getComment(form){
	
  var comment_text = document.getElementById('comments').value;

   $.get('/comment', {_comment: comment_text, _ticket: form}, function(data){
    
        $('#com_list ').html(data);
        clearComment();
   });

}

function clearComment(){
	$('#comments').val('');
}

    