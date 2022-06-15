

function run() {
	Array.from(document.querySelectorAll(".CircleStrokeMeter")).forEach(
		CircleStrokeMeter
	);
}

function CircleStrokeMeter(meterElement) {
	const circle = meterElement.querySelector("svg > circle + circle");
	const numberElement = meterElement.querySelector("svg > text");
	//const score = parseFloat(meterElement.dataset.score);
	const score = (Math.random() * 10).toFixed(2);
	const normaliziedScore = (10 - score) / 10;

	circle.style.strokeDashoffset = 1;

	const transitionEnd = (event) => {
		circle.removeEventListener("transitionend", transitionEnd);
		meterElement.classList.remove("animatable");
	};

	circle.addEventListener("transitionend", transitionEnd);

	setTimeout(() => {
		meterElement.classList.add("animatable");

		let transitionDuration = window.getComputedStyle(circle).transitionDuration;
		transitionDuration =
			parseFloat(transitionDuration) *
			(transitionDuration.indexOf("ms") > -1 ? 1 : 1000);

		increaseNumber(numberElement, score, transitionDuration);
		circle.style.strokeDashoffset = normaliziedScore;
	}, 100);
}

function increaseNumber(numberElement, score, duration) {
	const intElement = numberElement.querySelector("tspan");
	const decimalElement = numberElement.querySelector("tspan + tspan");
	const startTime = Date.now();

	const callback = function () {
		const timePassed = Date.now() - startTime;

		const currentScore = Math.min(score * (timePassed / duration), score);

		let [int, dec] = ("" + currentScore.toFixed(2)).split(".");
		intElement.textContent = int;
		decimalElement.textContent = "." + dec;

		if (timePassed < duration) {
			requestAnimationFrame(callback);
		}
	};

	requestAnimationFrame(callback);
}

run();
