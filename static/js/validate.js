function validate(){

	var forename = document.getElementById("forename");
	var surname = document.getElementById("surname");
	var email = document.getElementById("email");
	var username = document.getElementById("username");
	var password = document.getElementById("password");
	var confirm = document.getElementById("confirm");

	user = [forename, surname, email, username, password, confirm];

	console.log("Hello");

	for(var i = 0; i<user.length; i++){
		console.log("Hello2");
		if(user[i].value == "" || user[i].value == " "){
			alert("You have left the " + user[i] + " blank");
			document.register.user[i].focus();
			return False;
		} 
	}

	forename = document.getElementById("forename").value;
	surname = document.getElementById("surname").value;
	email = document.getElementById("email").value;
	username = document.getElementById("username").value;
	password = document.getElementById("password").value;
	confirm = document.getElementById("confirm").value;

	var format = /^[a-zA-Z]{1,}$/;

	if(!String(forename).match(format)){
		//console.log("Hello3");
		alert("The forename field msut contain only characters of the alphabet, e.g. a or A");
		document.register.forename.focus();
		return false;
	}

	if(!String(surname).match(format)){
		//console.log("Hello4");
		alert("The surname field msut contain only characters of the alphabet, e.g. a or A ");
		document.register.surname.focus();
		return false;
	}

	eformat = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;

	if(!String(email).match(eformat)){
		//console.log("Hello5");
		alert("The email field does not match an email format");
		document.register.email.focus();
		return false;
	}

	uformat = /^[a-zA-Z0-9]{5,}$/;

	if(!String(username).match(uformat)){
		//console.log("Hello6");
		alert("The username field msut be at least 5 characters long and contain a lower and upercase letter");
		document.register.username.focus();
		return false;
	}

	var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");

	if(!String(password).match(strongRegex)){
		//console.log("Hello7");
		alert("The password field msut contain be 8 characters long at minimum, contain at least 1 lower case letter, 1 upper case letter, 1 number \
		and 1 special character.");
		document.register.password.focus();
		return false;
	}

	if(password != confirm){
		//console.log("Hello8");
		alert("The confirm field does not match the password field");
		document.register.confirm.focus();
		return false;
	}

	///[^a-zA-Z]+$/

	return true;
}

function forenameValidate(){

	var format = /^[a-zA-Z]{1,}$/;

	var forname = document.getElementById("forename").value;

	if(!String(forname).match(format)){
		document.getElementById('forError').innerHTML="The forename field msut contain only characters of the alphabet, e.g. a or A";
		document.getElementById('forError').style.color = "red";
		//document.getElementById('forError').style.fontSize = "0.8em";
		document.getElementById('forError').style.textAlign = "center";
	}
	else{
		document.getElementById('forError').innerHTML="All Good";
		document.getElementById('forError').style.color = "green";
		document.getElementById('forError').style.textAlign = "center";
	}

}

function surnameValidate(){

	var format = /^[a-zA-Z]{1,}$/;

	var surname = document.getElementById("surname").value;

	if(!String(surname).match(format)){
		document.getElementById('surError').innerHTML="The surname field msut contain only characters of the alphabet, e.g. a or A";
		document.getElementById('surError').style.color = "red";
		//document.getElementById('forError').style.fontSize = "0.8em";
		document.getElementById('surError').style.textAlign = "center";
	}
	else{
		document.getElementById('surError').innerHTML="All Good";
		document.getElementById('surError').style.color = "green";
		document.getElementById('surError').style.textAlign = "center";
	}

}

function emailValidate(){

	var eformat = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$/;

	var email = document.getElementById("email").value;

	if(!String(email).match(eformat)){
		document.getElementById('emError').innerHTML="The email field does not match an email format";
		document.getElementById('emError').style.color = "red";
		document.getElementById('emError').style.textAlign = "center";
	}
	else{
		document.getElementById('emError').innerHTML="All Good";
		document.getElementById('emError').style.color = "green";
		document.getElementById('emError').style.textAlign = "center";
	}
}

function usernameValidate(){

	var format = /^[a-zA-Z0-9]{5,}$/;

	var username = document.getElementById("username").value;

	if(!String(username).match(format)){
		document.getElementById('userError').innerHTML="The username field msut be at least 5 characters long and contain a lower and upercase letter";
		document.getElementById('userError').style.color = "red";
		//document.getElementById('forError').style.fontSize = "0.8em";
		document.getElementById('userError').style.textAlign = "center";
	}
	else{
		document.getElementById('userError').innerHTML="All Good";
		document.getElementById('userError').style.color = "green";
		document.getElementById('userError').style.textAlign = "center";
	}

}

function passwordValidate(){

	var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");

	var password = document.getElementById("password").value;

	if(!String(password).match(strongRegex)){
		document.getElementById('paError').innerHTML="The password field msut contain be 8 characters long at minimum, contain at least 1 lower case letter, 1 upper case letter, 1 number \
		and 1 special character.";
		document.getElementById('paError').style.color = "red";
		document.getElementById('paError').style.fontSize = "0.8em";
		document.getElementById('paError').style.textAlign = "center";
	}
	else{
		document.getElementById('paError').innerHTML="All Good";
		document.getElementById('paError').style.color = "green";
		document.getElementById('paError').style.textAlign = "center";
	}
}

function confirmValidate(){

	var password = document.getElementById("password").value;
	var confirm = document.getElementById("confirm").value;

	if(password != confirm){
		console.log("Hello")
		document.getElementById('conError').innerHTML="The confirm field does not match the password field";
		document.getElementById('conError').style.color = "red";
		document.getElementById('conError').style.textAlign = "center";
	}
	else{
		document.getElementById('conError').innerHTML="All Good";
		document.getElementById('conError').style.color = "green";
		document.getElementById('conError').style.textAlign = "center";
	}

}

function confirmDelete(){
	return confirm("Please confirm you wish to delete this profile, this action is permanet");
}

function confirmUpdate(){
	return confirm("Please confirm you wish to update this profile, this action is permanet");
}