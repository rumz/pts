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
