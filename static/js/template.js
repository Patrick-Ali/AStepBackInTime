"use strict"

var clickedTop = false;
var clickedBottom = false;
var clickedEmpire = false;
var clickedLogin = false;
var logg = document.getElementById("arrow");
var topp = document.getElementById("top");
var bottom = document.getElementById("bottom");
var empire = document.getElementById("Empire");

function dropDown(){
	// Function to remove and add class to the top menu so as to make it function like a drop down menu 
	if(clickedTop === false)
	{
		// Show menu
		document.getElementById("navBar").className="showing";
		document.getElementById("menuTop").className="showing";
		topp.innerHTML="Menu &#9650";
		clickedTop = true;
	}
	else if(clickedTop === true)
	{
		// Hide menu
		document.getElementById("menuTop").className=document.getElementById("menuTop").className.replace(/(?:^|\s)showing(?!\S)/g, '');
		document.getElementById("navBar").className = document.getElementById("navBar").className.replace(/(?:^|\s)showing(?!\S)/g, '');
		document.getElementById("menuTop").classList.toggle("hideing");
		document.getElementById("navBar").classList.toggle("hideing");
		topp.innerHTML="Menu &#x25BC";
		clickedTop = false;
	}
}

function dropDownLoggedIn(){
	// Function to toggle the display of the logged in menu
	if(clickedLogin === false)
	{
		// Show menu
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
	// Function to toggle the display of the Empire menu
	if(clickedEmpire === false)
	{
		// Show menu
		document.getElementById("empireList").className="shower";
		empire.innerHTML="Ancient Empires &#9650";
		clickedEmpire = true;
	}
	else if(clickedEmpire === true)
	{
		// Hide menu
		document.getElementById("empireList").className="hidden";
		empire.innerHTML="Ancient Empires &#x25BC";
		clickedEmpire = false;
	}
}

function dropDownBottom(){
	// Function to remove and add class to the bottom menu so as to make it function like a drop down menu
	if(clickedBottom === false)
	{
		// Show menu
		document.getElementById("footer").className="show";
		document.getElementById("menuBottom").className="show";
		bottom.innerHTML="More About Us &#9650";
		clickedBottom = true;
	}
	else if(clickedBottom === true)
	{
		// Hide menu
		document.getElementById("menuBottom").className=document.getElementById("menuBottom").className.replace(/(?:^|\s)show(?!\S)/g, '');
		document.getElementById("footer").className = document.getElementById("footer").className.replace(/(?:^|\s)show(?!\S)/g, '');
		document.getElementById("menuBottom").classList.toggle("hideing");
		document.getElementById("footer").classList.toggle("hideing");
		bottom.innerHTML="More About Us &#x25BC";
		clickedBottom = false;
	}
}