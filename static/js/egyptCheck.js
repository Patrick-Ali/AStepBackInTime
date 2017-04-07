function eqyptCheck(){
	// Function used to tally the score for the Egypt Quiz
	
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

	if(document.getElementById('q1-1').checked){
		newScore++;
		console.log("q1 check");
		score.value = newScore;
	}

	if(document.getElementById('q2-2').checked){
		newScore++;
		console.log("q2 check");
		score.value = newScore;
	}

	if(document.getElementById('q3-0').checked && document.getElementById('q3-2').checked){
		newScore++;
		console.log("q3 check");
		score.value = newScore;
	}

	if(q4.value == "Nile" || q4.value == "nile"){
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

	if(q7.value == "khamun"){
		newScore++;
		console.log("q7 check");
		score.value = newScore;
	}

	if(document.getElementById('q8-0').checked && document.getElementById('q8-3').checked){
		newScore++;
		console.log("q8 check");
		score.value = newScore;
	}

	if(q9.value == "Valley of the kings" || q9.value == "valley of the kings"){
		newScore++;
		console.log("q9 check");
		score.value = newScore;
	}

	if(q10.value == "Moses" || q10.value == "moses"){
		newScore++;
		console.log("q10 check");
		score.value = newScore;
	}

	return true;

}