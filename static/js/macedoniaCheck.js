function macedoniaCheck(){
	var q1 = document.getElementById('q1');
	var q2 = document.getElementById('q2');
	var q3 = document.getElementById('q3');
	var q4 = document.getElementById('q4');
	var q5 = document.getElementById('q5');
	var q6 = document.getElementById('q6');
	var q7 = document.getElementById('q7');
	var q8 = document.getElementById('q8');
	var q9 = document.getElementById('q9');
	var q10 = document.getElementById('q10');

	var score = document.getElementById('score');
	var newScore = score.value;

	if(document.getElementById('q1-0').checked){
		newScore++;
		console.log("q1 check");
		score.value = newScore;
	}

	if(document.getElementById('q2-0').checked){
		newScore++;
		console.log("q2 check");
		score.value = newScore;
	}

	if(document.getElementById('q3-0').checked && document.getElementById('q3-2').checked){
		newScore++;
		console.log("q3 check");
		score.value = newScore;
	}

	if(q4.value == "Philip" || q4.value == "philip"){
		newScore++;
		console.log("q4 check");
		score.value = newScore;
	}

	if(document.getElementById('q5-0').checked){
		newScore++;
		console.log("q5 check");
		score.value = newScore;
	}

	if(document.getElementById('q6-0').checked){
		newScore++;
		console.log("q6 check");
		score.value = newScore;
	}

	if(q7.value == "King of Asia" || q7.value == "king of Asia"){
		newScore++;
		console.log("q7 check");
		score.value = newScore;
	}

	if(document.getElementById('q8-0').checked && document.getElementById('q8-3').checked){
		newScore++;
		console.log("q8 check");
		score.value = newScore;
	}

	if(q9.value == "Alexander" || q9.value == "alexander" || q9.value == "Alexander IV" || q9.value == "alexander iv"){
		newScore++;
		console.log("q9 check");
		score.value = newScore;
	}

	if(q10.value == "32"){
		newScore++;
		console.log("q10 check");
		score.value = newScore;
	}

	return true;

}