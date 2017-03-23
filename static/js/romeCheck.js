function romeCheck(){
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
		score.value = newScore;
	}

	if(document.getElementById('q2-0').checked){
		newScore++;
		score.value = newScore;
	}

	if(document.getElementById('q3-0').checked && document.getElementById('q3-1').checked){
		newScore++;
		score.value = newScore;
	}

	if(q4 == "Alps" || q4 == "alps"){
		newScore++;
		score.value = newScore;
	}

	if(document.getElementById('q5-0').checked){
		newScore++;
		score.value = newScore;
	}

	if(document.getElementById('q6-1').checked){
		newScore++;
		score.value = newScore;
	}

	if(q7 == "Great" || q7 == "great"){
		newScore++;
		score.value = newScore;
	}

	if(document.getElementById('q8-0').checked && document.getElementById('q8-2').checked){
		newScore++;
		score.value = newScore;
	}

	if(q9 == "Cleopatra" || q9 == "cleopatra"){
		newScore++;
		score.value = newScore;
	}

	if(q10 == "Brutus" || q10 == "brutus"){
		newScore++;
		score.value = newScore;
	}

	return True;

}