'use strict';
const transitionTime = 250;
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".start-button").addEventListener('click', e => fetchQuiz(e));
});
function fetchQuiz(e) {
  const appdiv = e.target.parentElement.parentElement;
  fetch('questions/').then(response => response.json()).then(response => {
    document.querySelector(".index-welcome").style.opacity = '0';
    setTimeout(() => {
      document.querySelector(".index-welcome").style.display = "none";
    }, transitionTime);
    initializeQuiz(response, appdiv);
  });
}
function initializeQuiz(questions, target) {
  const quizWrapper = initializeQuestions(questions);
  target.append(quizWrapper);
  const question_total = questions.questions.length;
  setNextButton(question_total);
  setBackButton();
  document.querySelector(`#question-0`).style.display = "block";
  setTimeout(() => {
    document.querySelector(`#question-0`).style.opacity = '1';
  }, transitionTime);
}
function setBackButton() {
  const prevButtons = document.querySelectorAll(".back-btn");
  prevButtons.forEach(button => {
    button.addEventListener('click', e => {
      const current_question = e.target.parentElement.parentElement;
      const index = Number(current_question.dataset.question_id);
      current_question.style.opacity = '0';
      setTimeout(() => {
        current_question.style.display = "none";
      }, transitionTime);
      if (0 <= index - 1) {
        setTimeout(() => {
          document.querySelector(`#question-${index - 1}`).style.display = 'block';
          document.querySelector(`#question-${index - 1}`).style.opacity = '1';
        }, transitionTime);
      }
    });
  });
}
function setNextButton(question_total) {
  const nextButtons = document.querySelectorAll(".next-btn");
  nextButtons.forEach(button => {
    button.addEventListener('click', e => {
      const current_question = e.target.parentElement;
      const index = Number(current_question.dataset.question_id);
      current_question.style.opacity = '0';
      setTimeout(() => {
        current_question.style.display = "none";
      }, transitionTime);
      if (question_total > index + 1) {
        document.querySelector(`#question-${index + 1}`).style.display = "block";
        setTimeout(() => {
          document.querySelector(`#question-${index + 1}`).style.opacity = '1';
        }, transitionTime);
      } else {
        getResults(question_total);
      }
    });
  });
}
function getResults(question_total) {
  const answers_list = document.querySelectorAll(".selected");
  let answers_obj = {};
  for (let i = 0; i < answers_list.length; i++) {
    if (answers_list[i].dataset.relation === "xor" || answers_list[i].dataset.relation === "img") {
      answers_obj[answers_list[i].dataset.question_type] = answers_list[i].dataset.answer_id;
    } else if (answers_list[i].dataset.relation === "and") {
      if (answers_obj[answers_list[i].dataset.question_type] == undefined) {
        answers_obj[answers_list[i].dataset.question_type] = [answers_list[i].dataset.answer_id];
      } else {
        answers_obj[answers_list[i].dataset.question_type].push(answers_list[i].dataset.answer_id);
      }
    }
  }
  for (const item in answers_obj) {
    if (answers_obj[item] === "false") {
      answers_obj[item] = false;
    }
    if (Array.isArray(answers_obj[item])) {
      if (answers_obj[item].includes("false")) {
        answers_obj[item] = false;
      }
    }
  }
  let csrftoken = getCookie('csrftoken');
  fetch('results', {
    method: 'POST',
    body: JSON.stringify(answers_obj),
    headers: {
      'X-CSRFToken': csrftoken
    },
    mode: 'same-origin'
  }).then(response => response.json()).then(response => {
    document.querySelector('.quiz-wrapper').style.display = 'none';
    if (response.length !== 0) {
      generateResults(response);
    } else {
      const mainApp = document.querySelector("#app");
      const resultsWrapper = document.createElement('div');
      resultsWrapper.className = "quiz-final-wrapper";
      mainApp.append(resultsWrapper);
      const resultsDiv = document.createElement('div');
      resultsDiv.className = "results-wrapper";
      resultsDiv.id = `no-result`;
      const resultsHeader = document.createElement('span');
      resultsHeader.className = "results-wrapper__header";
      resultsHeader.innerHTML = "Sorry, no results found.";
      resultsDiv.append(resultsHeader);
      const resultsText = document.createElement('span');
      resultsText.className = "results-wrapper__text";
      resultsText.innerHTML = "Please try again the quiz with different answers combination";
      resultsDiv.append(resultsText);
      const button = document.createElement('button');
      button.className = "btn btn-secondary btn-lg btn-block";
      button.type = "button";
      button.id = "result-button";
      button.innerHTML = 'Retake quiz <i style="font-size:12px" class="fa fa-refresh" aria-hidden="true"></i>';
      button.addEventListener('click', () => location.reload());
      resultsDiv.append(button);
      resultsDiv.style.display = "none";
      resultsDiv.style.opacity = '0';
      resultsWrapper.append(resultsDiv);
      resultsDiv.style.display = "flex";
      setTimeout(() => {
        resultsDiv.style.opacity = '1';
      }, transitionTime);
    }
  });
}
function generateResults(response) {
  const mainApp = document.querySelector("#app");
  const resultsWrapper = document.createElement('div');
  resultsWrapper.className = "quiz-final-wrapper";
  mainApp.append(resultsWrapper);
  response.forEach((result, index, array) => {
    const element = resultCards(result, index, array);
    resultsWrapper.append(element);
  });
  const firstResult = document.querySelector('.results-wrapper');
  firstResult.style.display = "block";
  setTimeout(() => {
    firstResult.style.opacity = '1';
  }, transitionTime);
  document.querySelectorAll('#result-button').forEach(element => {
    element.addEventListener('click', e => {
      const currentResult = e.target.parentElement;
      const index = Number(currentResult.dataset.index);
      currentResult.style.opacity = '0';
      setTimeout(() => {
        currentResult.style.display = 'none';
      }, transitionTime);
      if (e.target.dataset.last === "true") {
        location.reload();
      } else {
        document.querySelector(`#result-${index + 1}`).style.display = 'block';
        setTimeout(() => {
          document.querySelector(`#result-${index + 1}`).style.opacity = '1';
        }, transitionTime);
      }
    });
  });
}
function resultCards(data, index, array) {
  const resultsDiv = document.createElement('div');
  resultsDiv.className = "results-wrapper";
  resultsDiv.id = `result-${index}`;
  resultsDiv.dataset.index = `${index}`;
  const resultsHeader = document.createElement('span');
  resultsHeader.className = "results-wrapper__header";
  resultsHeader.innerHTML = "Recommended for you:";
  resultsDiv.append(resultsHeader);
  const movieInfo = document.createElement('div');
  movieInfo.className = "results-wrapper__info";
  const moviePosterDiv = document.createElement('div');
  moviePosterDiv.className = "results-wrapper__info__image";
  const moviePosterLink = document.createElement('a');
  moviePosterLink.href = `/movies/${data.id}`;
  moviePosterLink.target = "_blank";
  moviePosterLink.rel = "noopener noreferrer";
  const moviePosterImg = document.createElement('img');
  moviePosterImg.src = data.poster_path;
  moviePosterLink.append(moviePosterImg);
  moviePosterDiv.append(moviePosterLink);
  movieInfo.append(moviePosterDiv);
  const movieContent = document.createElement('div');
  movieContent.className = "results-wrapper__info__content";
  const movieTitleWrapper = document.createElement('span');
  movieTitleWrapper.className = "results-wrapper__info__content__title";
  const movieTitle = document.createElement('a');
  movieTitle.className = "results-wrapper__info__content__title__link";
  movieTitle.innerHTML = data.title;
  movieTitle.href = `/movies/${data.id}`;
  movieTitle.target = "_blank";
  movieTitle.rel = "noopener noreferrer";
  movieTitleWrapper.append(movieTitle);
  movieContent.append(movieTitleWrapper);
  movieInfo.append(movieContent);
  const movieDescriptionWrapper = document.createElement('div');
  movieDescriptionWrapper.className = "results-wrapper__info__overview";
  const movieDescription = document.createElement('span');
  movieDescription.className = "results-wrapper__info__overview_text";
  movieDescription.innerHTML = data.overview;
  movieDescriptionWrapper.append(movieDescription);
  movieContent.append(movieDescriptionWrapper);
  resultsDiv.append(movieInfo);
  const button = document.createElement('button');
  button.className = "btn btn-secondary btn-lg btn-block";
  button.type = "button";
  button.id = "result-button";
  if (index + 1 === array.length) {
    button.innerHTML = '<i style="font-size:12px" class="fa fa-refresh" aria-hidden="true"></i>Retake the quiz';
    button.dataset.last = "true";
  } else {
    button.innerHTML = 'Get another recommendation <i style="font-size:12px" class="fa fa-refresh" aria-hidden="true"></i>';
    button.dataset.last = "false";
  }
  resultsDiv.append(button);
  resultsDiv.style.display = "none";
  resultsDiv.style.opacity = "0";
  return resultsDiv;
}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) == name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function initializeQuestions(questions) {
  const quizWrapper = document.createElement('div');
  quizWrapper.className = "quiz-wrapper";
  questions.questions.forEach((question, index) => {
    const questionBox = document.createElement('div');
    questionBox.className = 'question-box';
    questionBox.id = `question-${index}`;
    questionBox.dataset.question_id = `${index}`;
    questionBox.dataset.question_type = `${question.Type}`;
    const titleWrapper = document.createElement('div');
    titleWrapper.className = 'question-wrapper';
    const title = document.createElement('div');
    title.className = 'question-wrapper__question-title';
    title.innerHTML = `${index + 1}. ${question.Title}`;
    titleWrapper.append(title);
    if (question.Select === "and") {
      const subtitle = document.createElement('div');
      subtitle.className = "question-wrapper__question-subtitle";
      subtitle.innerHTML = "Multiple answers are possible";
      titleWrapper.append(subtitle);
    }
    questionBox.append(titleWrapper);
    const answers = document.createElement('ul');
    if (question.Options.length < 12) {
      answers.className = "option-box";
    } else {
      answers.className = "option-box big";
    }
    answers.dataset.relation = question.Select;
    question.Options.forEach((option, option_index) => {
      const li = document.createElement('li');
      if (question.Select === "img") {
        const divGif = document.createElement('div');
        divGif.className = 'gif-container';
        const imgGif = document.createElement('img');
        imgGif.className = 'gif-container__img';
        imgGif.src = `${option[1]}`;
        imgGif.alt = `GIF of Nicolas Cage in a movie, described expression "${option[0]}"`;
        const spanText = document.createElement('span');
        spanText.className = 'gif-container__title';
        spanText.innerHTML = `${option[0]}`;
        divGif.append(imgGif, spanText);
        li.append(divGif);
      } else {
        const icon = document.createElement('i');
        icon.className = "fa-regular fa-square";
        const textSpan = document.createElement('span');
        textSpan.innerHTML = `${option[1]}`;
        li.append(icon, textSpan);
      }
      li.dataset.answer_id = `${option[0]}`;
      li.dataset.question_id = `${index}`;
      li.dataset.relation = question.Select;
      li.dataset.question_type = question.Type;
      li.className = 'option-box__li unselected';
      li.id = `answer-question-${index}`;
      createAnswers(question, li, index, option_index);
      answers.append(li);
    });
    questionBox.append(answers);
    if (index != 0) {
      const backButton = document.createElement('div');
      backButton.className = "back-btn-wrapper";
      backButton.id = `wrapper-back-btn-${index}`;
      const spanButton = document.createElement('span');
      spanButton.innerHTML = "< Back";
      spanButton.className = "back-btn";
      spanButton.id = `back-btn-${index}`;
      backButton.append(spanButton);
      questionBox.append(backButton);
    }
    ;
    const nextButton = document.createElement('div');
    nextButton.className = "next-btn";
    nextButton.id = `next-btn-${index}`;
    if (index + 1 === questions.questions.length) {
      nextButton.innerHTML = "Check Results";
    } else {
      nextButton.innerHTML = "Next";
    }
    nextButton.style.display = "none";
    nextButton.style.opacity = "0";
    nextButton.dataset.question_id = `${index}`;
    questionBox.append(nextButton);
    questionBox.style.display = "none";
    questionBox.style.opacity = '0';
    quizWrapper.append(questionBox);
  });
  return quizWrapper;
}
function createAnswers(question, li, index, option_index) {
  if (question.Select === "xor") {
    li.addEventListener('click', () => {
      const other_answers = document.querySelectorAll(`#${li.id}`);
      other_answers.forEach(element => {
        element.className = 'option-box__li unselected';
        element.querySelector('i').className = "fa-regular fa-square";
      });
      li.className = 'option-box__li selected';
      li.querySelector('i').className = "fa-regular fa-square-check";
      setTimeout(() => {
        document.querySelector(`#next-btn-${index}`).style.display = "block";
        document.querySelector(`#next-btn-${index}`).style.opacity = '1';
      }, transitionTime / 2);
    });
  } else if (question.Select === "img") {
    li.addEventListener('click', () => {
      const other_answers = document.querySelectorAll(`#${li.id}`);
      other_answers.forEach(element => {
        element.className = 'option-box__li unselected';
      });
      li.className = 'option-box__li selected';
      setTimeout(() => {
        document.querySelector(`#next-btn-${index}`).style.display = "block";
        document.querySelector(`#next-btn-${index}`).style.opacity = '1';
      }, transitionTime / 2);
    });
  } else if (question.Select === "and") {
    li.addEventListener('click', () => {
      if (option_index == 0) {
        const other_answers = document.querySelectorAll(`#${li.id}`);
        other_answers.forEach(element => {
          element.className = 'option-box__li unselected';
          element.querySelector('i').className = "fa-regular fa-square";
        });
      } else {
        document.querySelectorAll(`#${li.id}`)[0].className = 'option-box__li unselected';
        document.querySelectorAll(`#${li.id}`)[0].querySelector('i').className = "fa-regular fa-square";
      }
      if (li.className === 'option-box__li selected') {
        li.className = 'option-box__li unselected';
        li.querySelector('i').className = "fa-regular fa-square";
      } else {
        li.className = 'option-box__li selected';
        li.querySelector('i').className = "fa-regular fa-square-check";
      }
      setTimeout(() => {
        document.querySelector(`#next-btn-${index}`).style.display = "block";
        document.querySelector(`#next-btn-${index}`).style.opacity = '1';
      }, transitionTime / 2);
    });
  }
}
