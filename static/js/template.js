"use strict"

var clickedTop = false;
var clickedBottom = false;
var clickedEmpire = false;
var clickedLogin = false;
var logg = document.getElementById("arrow");
var test = document.getElementById("top");
var bottom = document.getElementById("bottom");
var empire = document.getElementById("Empire");
test.style.backgroundcolor="white";

function dropDown(){
if(clickedTop === false){
document.getElementById("navBar").className="showing";
document.getElementById("menuTop").className="showing";
test.innerHTML="Menu &#9650";
clickedTop = true;
}
else if(clickedTop === true)
{
document.getElementById("menuTop").className=document.getElementById("menuTop").className.replace(/(?:^|\s)showing(?!\S)/g, '');
document.getElementById("navBar").className = document.getElementById("navBar").className.replace(/(?:^|\s)showing(?!\S)/g, '');
test.innerHTML="Menu &#x25BC";
clickedTop = false;
}
}

function dropDownLoggedIn(){
if(clickedLogin === false){
document.getElementById("logExtra").style.display = "block";
logg.innerHTML="&#9650";
clickedLogin = true;
}
else if(clickedLogin === true)
{
document.getElementById("logExtra").style.display = "none";
logg.innerHTML="&#x25BC";
clickedLogin = false;
}
}

function dropDownEmpire(){
if(clickedEmpire === false){
	console.log("hello");
document.getElementById("empireList").className="shower";
empire.innerHTML="Ancient Empires &#9650";
clickedEmpire = true;
}
else if(clickedEmpire === true)
{
	console.log("hello2");
	document.getElementById("empireList").className="hidden";
empire.innerHTML="Ancient Empires &#x25BC";
clickedEmpire = false;
}
}

function dropDownBottom(){
if(clickedBottom === false){
document.getElementById("footer").className="show";
document.getElementById("menuBottom").className="show";
bottom.innerHTML="More About Us &#9650";
clickedBottom = true;
}
else if(clickedBottom === true)
{
document.getElementById("menuBottom").className=document.getElementById("menuBottom").className.replace(/(?:^|\s)show(?!\S)/g, '');
document.getElementById("footer").className = document.getElementById("footer").className.replace(/(?:^|\s)show(?!\S)/g, '');
bottom.innerHTML="More About Us &#x25BC";
clickedBottom = false;
}
}