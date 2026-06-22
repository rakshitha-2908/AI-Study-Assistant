import { useEffect, useMemo, useState } from "react";
import { FiArrowRight, FiCheckCircle, FiLoader, FiRefreshCw } from "react-icons/fi";
import { generateQuiz, evaluateQuiz } from "../api/client";
import MarkdownMessage from "./MarkdownMessage";

function parseQuestions(questionsText) {
  const lines = questionsText
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const parsed = [];
  let current = null;
  const prefixRegex = /^\d+[\.)]?\s*/;

  lines.forEach((line) => {
    if (prefixRegex.test(line)) {
      if (current) parsed.push(current);
      current = { text: line.replace(prefixRegex, "") };
    } else if (current) {
      current.text += ` ${line}`;
    } else {
      current = { text: line };
    }
  });

  if (current) {
    parsed.push(current);
  }

  return parsed;
}

function QuizView({ sessionId, topic, difficulty, setQuizAttempts }) {
  const [numQuestions, setNumQuestions] = useState(5);
  const [questionsText, setQuestionsText] = useState("");
  const [answers, setAnswers] = useState([]);
  const [feedback, setFeedback] = useState("");
  const [error, setError] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const questions = useMemo(() => parseQuestions(questionsText), [questionsText]);

  useEffect(() => {
    setAnswers(questions.map(() => ""));
  }, [questionsText]);

  function handleAnswerChange(index, value) {
    setAnswers((prev) => {
      const next = [...prev];
      next[index] = value;
      return next;
    });
  }

  async function handleGenerate() {
    setError(null);
    setFeedback("");
    setIsGenerating(true);

    try {
      const response = await generateQuiz({
        sessionId,
        topic,
        difficulty,
        numQuestions,
      });
      if (!response || !response.trim()) {
        throw new Error("The backend returned no quiz questions.");
      }
      setQuestionsText(response);
    } catch (err) {
      setError(err.message || "Unable to generate quiz. Try again.");
    } finally {
      setIsGenerating(false);
    }
  }

  async function handleSubmit() {
    if (questions.length === 0) return;

    setError(null);
    setFeedback("");
    setIsSubmitting(true);

    try {
      const userAnswers = answers
        .map((answer, index) => `${index + 1}. ${answer.trim()}`)
        .join("\n");

      const evaluation = await evaluateQuiz({
        sessionId,
        topic,
        questions: questionsText,
        userAnswers,
      });

      setFeedback(evaluation || "No feedback was returned.");
      setQuizAttempts((prev) => prev + 1);
    } catch (err) {
      setError(err.message || "Unable to evaluate quiz answers.");
    } finally {
      setIsSubmitting(false);
    }
  }

  const canSubmit = questions.length > 0 && answers.some((answer) => answer.trim());

  return (
    <div className="flex flex-col h-full bg-gray-50/50">
      <div className="border-b border-gray-200 bg-white/90 px-8 py-6 shadow-sm">
        <div className="max-w-6xl mx-auto flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-brand-dark/70 font-semibold mb-2">
              Quiz Mode
            </p>
            <h1 className="text-2xl font-semibold text-gray-900">Practice with a custom quiz</h1>
            <p className="text-sm text-gray-500 max-w-2xl mt-1">
              Generate a short quiz for your current topic and difficulty, then submit answers to get AI feedback.
            </p>
          </div>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div className="rounded-2xl bg-brand-light px-4 py-3 text-sm text-brand-dark shadow-sm">
              Topic: <span className="font-semibold">{topic}</span>
            </div>
            <div className="rounded-2xl bg-gray-50 px-4 py-3 text-sm text-gray-600 shadow-sm">
              Difficulty: <span className="font-semibold text-gray-900">{difficulty}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="max-w-6xl mx-auto px-8 py-8 flex flex-col gap-8">
          <div className="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
            <div className="rounded-3xl bg-white border border-gray-100 p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-gray-900">Generate a quiz</p>
                  <p className="text-sm text-gray-500 mt-1">
                    Choose how many questions you want and request a new quiz from the backend.
                  </p>
                </div>
                <button
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className="inline-flex items-center gap-2 rounded-full bg-brand px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-dark disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isGenerating ? <FiLoader className="animate-spin" /> : <FiRefreshCw />}
                  {isGenerating ? "Generating…" : "Generate Quiz"}
                </button>
              </div>

              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                <label className="text-sm text-gray-500">
                  Number of questions
                  <select
                    value={numQuestions}
                    onChange={(e) => setNumQuestions(Number(e.target.value))}
                    className="mt-2 w-full rounded-2xl border border-gray-200 bg-gray-50 px-3 py-2 text-sm outline-none transition focus:border-brand"
                  >
                    {[3, 5, 7, 10].map((count) => (
                      <option key={count} value={count}>
                        {count}
                      </option>
                    ))}
                  </select>
                </label>
                <div className="rounded-2xl bg-gray-50 p-4">
                  <p className="text-sm text-gray-500">Tip</p>
                  <p className="mt-2 text-sm text-gray-700">
                    Use a clear topic name so the backend generates targeted questions for your study area.
                  </p>
                </div>
              </div>
            </div>

            <div className="rounded-3xl bg-white border border-gray-100 p-6 shadow-sm">
              <p className="text-sm font-semibold text-gray-900">Quick start</p>
              <p className="text-sm text-gray-500 mt-2">
                After generating a quiz, answer each question in the text areas below and submit once you're ready.
              </p>
              <div className="mt-5 rounded-3xl bg-brand-light/70 p-4 text-sm text-brand-dark">
                <div className="font-semibold">Preview</div>
                <div className="mt-3 space-y-2 text-xs text-gray-600">
                  <p>• Quiz questions are generated by the API.</p>
                  <p>• Your answers are submitted together for evaluation.</p>
                  <p>• Feedback is shown below using the same markdown renderer as chat.</p>
                </div>
              </div>
            </div>
          </div>

          {error && (
            <div className="rounded-3xl border border-red-100 bg-red-50 p-4 text-sm text-red-700">
              {error}
            </div>
          )}

          {questions.length === 0 ? (
            <div className="rounded-3xl border border-dashed border-gray-200 bg-white/90 p-10 text-center text-gray-500 shadow-sm">
              <p className="text-lg font-semibold text-gray-900 mb-2">No quiz loaded yet</p>
              <p className="text-sm">Click Generate Quiz to load questions from the backend.</p>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="grid gap-6">
                {questions.map((question, index) => (
                  <div key={index} className="rounded-3xl border border-gray-100 bg-white p-5 shadow-sm">
                    <div className="flex items-start gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-brand-light text-brand-dark font-semibold">
                        {index + 1}
                      </div>
                      <div className="space-y-3">
                        <p className="text-sm font-semibold text-gray-900">Question {index + 1}</p>
                        <p className="text-sm text-gray-600 leading-relaxed">{question.text}</p>
                        <textarea
                          rows={4}
                          value={answers[index] || ""}
                          onChange={(e) => handleAnswerChange(index, e.target.value)}
                          placeholder="Write your answer here..."
                          className="mt-3 w-full min-h-[120px] rounded-3xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 outline-none transition focus:border-brand focus:bg-white"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <button
                  onClick={handleSubmit}
                  disabled={!canSubmit || isSubmitting}
                  className="inline-flex items-center justify-center gap-2 rounded-full bg-brand px-6 py-3 text-sm font-semibold text-white transition hover:bg-brand-dark disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isSubmitting ? <FiLoader className="animate-spin" /> : <FiArrowRight />}
                  {isSubmitting ? "Submitting…" : "Submit answers"}
                </button>
                <p className="text-sm text-gray-500">
                  {questions.length} questions loaded • {answers.filter((a) => a.trim()).length} answered
                </p>
              </div>

              {feedback && (
                <div className="rounded-3xl border border-gray-100 bg-white p-6 shadow-sm">
                  <div className="flex items-center gap-2 text-gray-900 mb-4">
                    <FiCheckCircle className="text-brand" />
                    <span className="text-sm font-semibold">Feedback</span>
                  </div>
                  <MarkdownMessage content={feedback} />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default QuizView;
