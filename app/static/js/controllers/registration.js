function checkParamsForRegistration(){
	var password = $("#password").val();
	var confirm_password = $("#confirm-password").val();
	if(password != confirm_password){
		event.preventDefault();
		showMessage("#msg-holder", "Passwords do not match, Try again.")
	}
}