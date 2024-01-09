// Constant Declarations
const username = document.getElementById("username");
const email = document.getElementById("email");
const profileDetails = document.getElementsByClassName("profile-details")[0];
const profilePic = document.getElementsByClassName("user-image")[0];
const numQuiz = document.getElementById("num-quiz");
const avgAccuracy = document.getElementById("average-accuracy");
const avgTime = document.getElementById("average-time");

let quizSummary, profileData;

/* Function to get avg. accuracy for the quiz summary */
const getAvgAccuracy = (summary) => {
  const totalCorrect = summary.reduce((total, quiz) => total + quiz.correct, 0);
  const totalQuestions = summary.reduce(
    (total, quiz) => total + quiz.question_count,
    0
  );

  return ((totalCorrect / totalQuestions) * 100).toFixed(2);
};

/* Function for rendering the profile */
const renderProfile = () => {
  /* Setting the Text Content and then displaying the chunk */
  username.innerText = profileData.name;
  email.innerText = profileData.email;

  numQuiz.innerText = quizSummary.length;
  avgAccuracy.innerText = quizSummary.length
    ? `${getAvgAccuracy(quizSummary)}%`
    : "0%";
  avgTime.innerText = quizSummary.length
    ? `${(
        quizSummary.reduce((total, quiz) => total + quiz.time, 0) / 1000
      ).toFixed(2)} s`
    : 0;

  profileDetails.style.display = "flex";
};

// On Load, we are calling the API and storing the result in respective variables
window.addEventListener("load", () => {
  fetch("/quiz/summary")
    .then((d) => d.json())
    .then((d) => {
      quizSummary = d.data;
      profileData = d.profile;

      renderProfile();
    });
});
