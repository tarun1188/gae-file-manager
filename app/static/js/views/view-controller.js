
try{
	if (document.getElementById("path_name"))
	document.getElementById("path_name").innerText = "Index of "+ decodeURI(document.location.pathname);
if(document.location.pathname != "/"){
	var path_directory = document.location.pathname.substr(0, document.location.pathname.lastIndexOf("/"))
	document.getElementById("parent_path").href = path_directory == "" ? "/" : path_directory;
} else
	document.getElementById("parent_directory").style.display = "none";	
}catch(err){
	console.log(err.message);
}

document.getElementById("hostname").innerText = "Google Appengine Server at " +location.host;

function showMessage(element_id, msg){
	$(element_id).html(msg);
}

// $(document).bind("contextmenu", function(event) { 
//     event.preventDefault();
// 	$('.custom-menu').css({top: event.pageY + "px", left: event.pageX + "px"});
// 	$('.custom-menu').show();
// }).bind("click", function(event) {
//     $("div.custom-menu").hide();
//     console.log("hide context menu");
// });

// $('.custom-menu').click(function(){
// 	console.log('create a folder');
// });