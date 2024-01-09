// Constant Declarations
const quizContainer = document.getElementById("quiz-form");
const quizQuestion = document.getElementById("quiz-question");
const quizOptions = document.getElementsByClassName("quiz-options");
const submitBtn = document.getElementById("submit");
const quizOptionsContainer = document.getElementsByClassName("options");
const correctLabel = document.getElementById("correct-label");
const incorrectLabel = document.getElementById("incorrect-label");

const questionCount = 10;
let QUIZ_IDX = 0;
let correct = 0;
let incorrect = 0;
let quizStartTime;

/* Method for randomly shuffling an array */
const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

/* Rendering the Quiz */
const renderQuiz = () => {
  const quizzes = JSON.parse(localStorage.getItem("quizObj"));

  correctLabel.innerText = `Correct: ${correct}`;
  incorrectLabel.innerText = `Incorrect: ${incorrect}`;
  const question = quizzes[QUIZ_IDX];
  quizContainer.reset();

  quizQuestion.innerHTML = `Question ${QUIZ_IDX + 1}: ${question.question}`;
  for (let i = 0; i < 4; i++) quizOptions[i].innerHTML = question.options[i];

  submitBtn.disabled = true;
  if (QUIZ_IDX === quizzes.length - 1) submitBtn.innerText = "Finish";

  quizContainer.style.display = "block";
};

quizContainer.addEventListener("input", () => {
  submitBtn.disabled = false;
});

// On Load, we fetch the quiz and cache it
window.addEventListener("load", async () => {
  fetch(
    `https://opentdb.com/api.php?amount=${questionCount}&difficulty=easy&type=multiple&category=18`
  )
    .then((d) => d.json())
    .then((d) => {
      const quizArray = d.results.map((quiz) => {
        const options = shuffleArray([
          ...quiz.incorrect_answers,
          quiz.correct_answer,
        ]);
        return {
          question: quiz.question,
          options,
          answer: quiz.correct_answer,
        };
      });

      localStorage.setItem("quizObj", JSON.stringify(quizArray));
      renderQuiz();
      const date = new Date();
      quizStartTime = date.getTime();
    });
});

// On submission of quiz, we check the answer. If its last question, then we store the result/stats in cache and redirect to result page
quizContainer.addEventListener("submit", (e) => {
  e.preventDefault();
  const quizzes = JSON.parse(localStorage.getItem("quizObj"));

  const question = quizzes[QUIZ_IDX];
  const selectedOption = document.querySelector('input[name="q1"]:checked');
  const answer = document.querySelector(
    `label[for="${selectedOption.id}"]`
  ).textContent;

  answer === question.answer ? (correct += 1) : (incorrect += 1);

  QUIZ_IDX += 1;

  if (QUIZ_IDX <= quizzes.length - 1) renderQuiz();
  else {
    // Take the backup of the result
    const date = new Date();
    const timeTaken = date.getTime() - quizStartTime;
    fetch("/quiz/result", {
      method: "POST",
      body: JSON.stringify({
        questionCount,
        time: timeTaken,
        correct,
        incorrect,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((d) => d.json())
      .then((d) => {
        localStorage.setItem(
          "result",
          JSON.stringify({ correct, incorrect, time: timeTaken })
        );
        location.replace("/quiz/result");
      });
  }
});
